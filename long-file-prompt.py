#!/usr/bin/env python3
"""
chatgpt-long-file-prompting.py

A Python utility to analyze long files by sending chunks of their content to ChatGPT.
Allows users to provide custom prompts, refines these prompts for chunked processing,
retrieves partial analysis results in real-time, and compiles a comprehensive report upon completion.

Author: Your Name
License: MIT
"""

import argparse
import os
import sys
import logging
import time
from typing import List, Tuple
import openai
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configure logging
logger = logging.getLogger(__name__)

def setup_logging(verbose: bool, prompt_log_path: str, result_log_path: str):
    """
    Sets up the logging configuration.
    
    Args:
        verbose (bool): If True, set logging level to DEBUG, else INFO.
        prompt_log_path (str): Path to the file where prompts will be logged.
        result_log_path (str): Path to the file where results will be logged.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # Stream handler for console output
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File handler for prompts
    prompt_handler = logging.FileHandler(prompt_log_path)
    prompt_handler.setLevel(logging.DEBUG)
    prompt_handler.setFormatter(formatter)
    prompt_handler.addFilter(lambda record: 'PROMPT' in record.getMessage())
    logger.addHandler(prompt_handler)

    # File handler for results
    result_handler = logging.FileHandler(result_log_path)
    result_handler.setLevel(logging.DEBUG)
    result_handler.setFormatter(formatter)
    result_handler.addFilter(lambda record: 'RESULT' in record.getMessage())
    logger.addHandler(result_handler)

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Analyze a long file by sending its content to ChatGPT with custom prompts."
    )
    parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the target file to be analyzed.'
    )
    parser.add_argument(
        '--prompt',
        type=str,
        required=True,
        help='Custom prompt to guide ChatGPT\'s analysis.'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=1000,
        help='Number of lines per chunk. Default is 1000.'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='analysis_report.txt',
        help='Path to save the final analysis report. Default is analysis_report.txt.'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging.'
    )
    return parser.parse_args()

def read_file_in_chunks(file_path: str, chunk_size: int) -> List[str]:
    """
    Reads a file and yields chunks of lines.
    
    Args:
        file_path (str): Path to the file.
        chunk_size (int): Number of lines per chunk.
    
    Yields:
        List[str]: A chunk of lines from the file.
    """
    logger.debug(f"Opening file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            chunk = []
            for line_number, line in enumerate(file, start=1):
                chunk.append(line)
                if line_number % chunk_size == 0:
                    logger.debug(f"Yielding chunk ending at line {line_number}")
                    yield ''.join(chunk)
                    chunk = []
            if chunk:
                logger.debug(f"Yielding final chunk with {len(chunk)} lines")
                yield ''.join(chunk)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        sys.exit(1)

def get_openai_api_key() -> str:
    """
    Retrieves the OpenAI API key from environment variables.
    
    Returns:
        str: OpenAI API key.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)
    return api_key

def refine_prompt(user_prompt: str, engine: str = "gpt-4") -> Tuple[str, str]:
    """
    Refines the user-provided prompt to work effectively with chunked processing.
    
    Args:
        user_prompt (str): The original prompt provided by the user.
        engine (str): The OpenAI model to use.
    
    Returns:
        Tuple[str, str]: Refined chunk prompt and compilation instructions.
    """
    system_message = "You are an assistant that helps refine prompts for analyzing large files by splitting them into manageable chunks."
    user_message = (
        f"The user wants to analyze a large file using the following prompt:\n\n\"{user_prompt}\"\n\n"
        "Refine this prompt so that it can be effectively used to analyze individual chunks of the file. "
        "Provide a modified prompt suitable for chunk analysis and additional instructions on how to compile the final report from the chunk analyses."
    )

    try:
        logger.debug(f"PROMPT Refining Prompt:\n{user_message}")
        response = client.chat.completions.create(model=engine,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=1000,
        n=1,
        stop=None)
        refined_content = response.choices[0].message.content.strip()
        logger.debug(f"PROMPT Refined Content:\n{refined_content}")

        # Split the refined content into chunk prompt and compilation instructions
        # Assuming the assistant returns two clearly separated sections
        split_marker = "\n\n---\n\n"
        if split_marker in refined_content:
            chunk_prompt, compilation_instructions = refined_content.split(split_marker, 1)
        else:
            # If no clear split, assume entire content is chunk prompt
            chunk_prompt = refined_content
            compilation_instructions = "Please compile the analysis results from all chunks into a final comprehensive report."

        logger.debug(f"PROMPT Chunk Prompt:\n{chunk_prompt}")
        logger.debug(f"PROMPT Compilation Instructions:\n{compilation_instructions}")
        return chunk_prompt, compilation_instructions
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error during prompt refinement: {e}")
        sys.exit(1)

def analyze_chunk(chunk: str, chunk_prompt: str, engine: str = "gpt-4") -> str:
    """
    Sends a chunk of text to ChatGPT for analysis using the refined chunk prompt and returns the response.
    
    Args:
        chunk (str): The text chunk to analyze.
        chunk_prompt (str): The refined prompt for chunk analysis.
        engine (str): The OpenAI model to use.
    
    Returns:
        str: The analysis result from ChatGPT.
    """
    max_retries = 5
    backoff_factor = 2
    for attempt in range(1, max_retries + 1):
        try:
            prompt_content = f"{chunk_prompt}\n\nText:\n{chunk}"
            logger.debug(f"PROMPT Sending Chunk Prompt:\n{prompt_content}")
            response = client.chat.completions.create(model=engine,
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes provided text based on the given prompt."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.5,
            max_tokens=1500,
            n=1,
            stop=None)
            analysis = response.choices[0].message.content.strip()
            logger.debug(f"RESULT Analysis Result:\n{analysis}")
            return analysis
        except openai.RateLimitError:
            wait_time = backoff_factor ** attempt
            logger.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            break
    logger.error("Failed to retrieve analysis from ChatGPT after multiple attempts.")
    return "Analysis not available due to API errors."

def compile_final_report(partial_results: List[str], compilation_instructions: str, engine: str = "gpt-4") -> str:
    """
    Compiles all partial analysis results into a final comprehensive report using the compilation instructions.
    
    Args:
        partial_results (List[str]): List of partial analysis results.
        compilation_instructions (str): Instructions on how to compile the final report.
        engine (str): The OpenAI model to use.
    
    Returns:
        str: The final compiled report.
    """
    system_message = "You are an assistant that compiles individual analysis reports into a comprehensive final report."
    user_message = (
        f"The user has provided the following compilation instructions:\n\n\"{compilation_instructions}\"\n\n"
        "Here are the individual analysis results from each chunk:\n\n" +
        "\n\n".join(partial_results) +
        "\n\nPlease compile them into a final comprehensive report."
    )

    try:
        logger.debug(f"PROMPT Compilation Prompt:\n{user_message}")
        response = client.chat.completions.create(model=engine,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=2000,
        n=1,
        stop=None)
        final_report = response.choices[0].message.content.strip()
        logger.debug(f"RESULT Final Compiled Report:\n{final_report}")
        return final_report
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error during final compilation: {e}")
        return "Final report compilation failed due to API errors."

def save_logs(prompt_log_path: str, result_log_path: str):
    """
    Ensures that prompt and result log files are properly closed.
    
    Args:
        prompt_log_path (str): Path to the prompt log file.
        result_log_path (str): Path to the result log file.
    """
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)

def main():
    """
    Main function to orchestrate the file analysis with custom prompt refinement.
    """
    args = parse_arguments()

    # Define paths for prompt and result logs
    prompt_log_path = 'prompts.log'
    result_log_path = 'results.log'

    # Setup logging with separate log files for prompts and results
    setup_logging(args.verbose, prompt_log_path, result_log_path)

    logger.info(f"Starting analysis of file: {args.file}")
    logger.info(f"Using custom prompt: {args.prompt}")
    logger.info(f"Chunk size: {args.chunk_size} lines")
    logger.info(f"Output will be saved to: {args.output}")
    logger.info(f"Prompt logs will be saved to: {prompt_log_path}")
    logger.info(f"Result logs will be saved to: {result_log_path}")

    # Step 1: Refine the user-provided prompt for chunked processing
    chunk_prompt, compilation_instructions = refine_prompt(args.prompt)

    logger.debug(f"Refined Chunk Prompt:\n{chunk_prompt}")
    logger.debug(f"Compilation Instructions:\n{compilation_instructions}")

    partial_results = []
    total_chunks = 0

    # Step 2: Process the file in chunks and analyze each chunk
    for chunk in read_file_in_chunks(args.file, args.chunk_size):
        total_chunks += 1
        logger.info(f"Analyzing chunk {total_chunks}")
        analysis = analyze_chunk(chunk, chunk_prompt)
        partial_results.append(f"--- Analysis for Chunk {total_chunks} ---\n{analysis}\n")
        logger.info(f"Completed analysis for chunk {total_chunks}")

    logger.info("All chunks have been processed. Compiling final report.")

    # Step 3: Compile all partial results into the final report
    final_report = compile_final_report(partial_results, compilation_instructions)

    # Step 4: Save the final report to the specified output file
    try:
        with open(args.output, 'w', encoding='utf-8') as output_file:
            output_file.write("ChatGPT Long File Analysis Report\n")
            output_file.write("=================================\n\n")
            output_file.write(final_report)
        logger.info(f"Analysis report saved to {args.output}")
    except Exception as e:
        logger.error(f"Failed to write analysis report: {e}")
        sys.exit(1)
    finally:
        # Ensure all log handlers are properly closed
        save_logs(prompt_log_path, result_log_path)

if __name__ == "__main__":
    main()
