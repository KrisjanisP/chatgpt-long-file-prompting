# 📄 ChatGPT Long File Prompting 🔍✨

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-green.svg)

## 🚀 Overview

**ChatGPT Long File Prompting** is a powerful Python utility designed to analyze exceptionally long files by intelligently splitting them into manageable chunks and leveraging ChatGPT for comprehensive analysis. This tool ensures that large files are processed efficiently without being hindered by context length limitations of language models. Ideal for developers, data analysts, and researchers aiming to extract detailed insights from extensive documents, codebases, logs, and more.

## 🌟 Features

- **🔧 Command-Line Interface (CLI):** Easily specify the target file, custom prompts, and configure settings via command-line arguments.
- **📝 Custom Prompt Support:** Allows users to input their own prompts for tailored analysis.
- **🛠️ Prompt Refinement:** Automatically refines user-provided prompts to ensure effective chunked processing.
- **📂 Chunked Processing:** Efficiently handles large files by reading and processing them in manageable chunks.
- **⏱️ Real-Time Analysis:** Retrieves and displays partial analysis results as the file is being processed.
- **📄 Comprehensive Summary:** Compiles all partial results into a final, cohesive analysis report.
- **📝 Logging:** Provides detailed logs for monitoring and debugging purposes.
- **🔐 Configuration:** Supports environment variables for sensitive information like API keys.
- **💡 Flexible Output:** Allows users to choose the format and location of the analysis report.
- **🔄 Retry Mechanism:** Implements robust retry logic to handle API rate limits and transient errors gracefully.

## 📥 Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/chatgpt-long-file-prompting.git
   cd chatgpt-long-file-prompting
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the project root and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   *Alternatively, you can export the environment variable directly:*

   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🛠️ Usage

```bash
python chatgpt-long-file-prompting.py --file path/to/your/file.txt --prompt "Your custom prompt here" --chunk-size 1000 --output analysis_report.txt --verbose
```

### 📋 Arguments

- `--file` (required): Path to the target file to be analyzed.
- `--prompt` (required): Custom prompt to guide the language model's analysis.
- `--chunk-size` (optional): Number of lines per chunk. Default is `1000`.
- `--output` (optional): Path to save the final analysis report. Default is `analysis_report.txt`.
- `--verbose` (optional): Enable verbose logging.

### 💡 Example

```bash
python chatgpt-long-file-prompting.py --file sample_code.cpp --prompt "Analyze the exit codes and their usage in the following code." --chunk-size 500 --output report.txt --verbose
```

## 📂 Project Structure

```
chatgpt-long-file-prompting/
├── .env
├── chatgpt-long-file-prompting.py
├── requirements.txt
├── README.md
└── LICENSE
```

## 🧰 Dependencies

Ensure your `requirements.txt` includes the necessary dependencies:

```txt
openai==0.27.0
python-dotenv==1.0.0
```

*Note: Ensure you have the latest versions or specify the versions compatible with your environment.*

## 🔍 Detailed Code Explanation

### 1. **Imports and Environment Setup**

- **Standard Libraries:**
  - `argparse`: For parsing command-line arguments.
  - `os`, `sys`: For operating system interactions and system-specific parameters.
  - `logging`: For logging information, warnings, and errors.
  - `time`: For handling delays between retries.
  - `typing.List, Tuple`: For type hinting.

- **Third-Party Libraries:**
  - `openai`: OpenAI's Python library for API interactions.
  - `dotenv.load_dotenv`: For loading environment variables from a `.env` file.

### 2. **Logging Configuration**

The `setup_logging` function configures the logging level based on the `--verbose` flag. It ensures that debug information is available when needed.

### 3. **Argument Parsing**

The `parse_arguments` function utilizes `argparse` to handle command-line arguments, making the tool flexible and user-friendly. It includes a required `--prompt` argument for custom prompts.

### 4. **File Reading**

The `read_file_in_chunks` generator function reads the target file in specified chunk sizes (number of lines) to efficiently handle large files without exhausting system memory.

### 5. **OpenAI API Interaction**

- **API Key Retrieval:**

  The `get_openai_api_key` function fetches the OpenAI API key from environment variables, ensuring that sensitive information is not hard-coded.

- **Prompt Refinement:**

  The `refine_prompt` function takes the user-provided prompt and refines it to work effectively with chunked processing. It sends a request to ChatGPT to generate a modified prompt suitable for analyzing individual chunks and provides instructions for compiling the final report.

- **Chunk Analysis:**

  The `analyze_chunk` function sends each chunk to ChatGPT using the refined prompt. It includes retry logic to handle rate limits and transient errors gracefully.

- **Final Report Compilation:**

  The `compile_final_report` function takes all partial analysis results and uses ChatGPT to compile them into a final comprehensive report based on the compilation instructions obtained during prompt refinement.

### 6. **Main Orchestration**

The `main` function orchestrates the entire process:

1. **Initialization:**
   - Parses arguments.
   - Sets up logging.
   - Retrieves the API key.

2. **Prompt Refinement:**
   - Refines the user-provided prompt for effective chunked analysis.

3. **Processing:**
   - Reads the file in chunks.
   - Sends each chunk for analysis using the refined prompt.
   - Collects partial results.

4. **Compilation:**
   - Compiles all partial analyses into a final report using ChatGPT.

5. **Output:**
   - Writes the final report to the specified output file.

6. **Error Handling:**
   - Gracefully handles file I/O errors and API issues.

## 💡 Enhancements and Best Practices

- **🔍 Custom Prompt Support:** Allows users to input their own prompts, making the tool highly customizable.
- **🛠️ Prompt Refinement:** Automatically refines user-provided prompts to ensure they work effectively with chunked processing, enhancing the quality and coherence of the final report.
- **🔐 Environment Variables:** Utilizes `.env` files and environment variables to manage sensitive data securely.
- **📝 Logging:** Implements a robust logging system to aid in monitoring and debugging.
- **🔄 Retry Logic:** Incorporates retry mechanisms to handle API rate limits and transient errors, enhancing reliability.
- **🧩 Modular Design:** Breaks down functionality into discrete, reusable functions for better maintainability.
- **🖥️ Command-Line Interface:** Provides a user-friendly CLI with helpful descriptions and defaults.
- **📚 Documentation:** Includes comprehensive docstrings and comments for clarity.
- **💾 Flexible Output Options:** Allows users to specify the format and destination of the analysis report.
- **🧪 Testing:** Encourages the inclusion of unit tests to ensure the reliability and correctness of the tool.

## 🤝 Contributing

Contributions are welcome! 🎉 Please open an issue or submit a pull request for any enhancements, bug fixes, or feature requests.

## 📄 License

This project is licensed under the [MIT License](LICENSE). 📝

## 🛡️ Disclaimer

Ensure that you comply with OpenAI's [usage policies](https://platform.openai.com/docs/usage-policies) when using this tool. The developer is not responsible for any misuse of the program.

## 📬 Contact

For any inquiries or support, please contact [your.email@example.com](mailto:your.email@example.com). 📧

---

## 📝 Final Notes

**ChatGPT Long File Prompting** provides a robust foundation for integrating advanced language models into file analysis workflows with customizable prompts. It emphasizes clarity, robustness, and ease of use, making it an excellent candidate for sharing on GitHub and collaborating with the developer community.

By allowing users to input their own prompts and intelligently refining them for chunked processing, the tool becomes highly adaptable to a wide range of analysis tasks, ensuring that the limitations of context length do not hinder the depth and quality of insights derived from large files.

Happy Analyzing! 🎉
```
