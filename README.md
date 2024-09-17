# 📄 ChatGPT Long File Prompting 🔍✨

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-green.svg)

## 🚀 Overview

A Python utility designed to analyze exceptionally long files by intelligently splitting them into manageable chunks and leveraging ChatGPT for comprehensive analysis. This tool ensures that large files are processed efficiently without being hindered by context length limitations of language models. Ideal for developers, data analysts, and researchers aiming to extract detailed insights from extensive documents, codebases, logs, and more.

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
   git clone https://github.com/yourusername/long-file-prompt.git
   cd long-file-prompt
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
python long-file-prompt.py --file path/to/your/file.txt --prompt "Your custom prompt here" --chunk-size 1000 --output analysis_report.txt --verbose
```

### 📋 Arguments

- `--file` (required): Path to the target file to be analyzed.
- `--prompt` (required): Custom prompt to guide the language model's analysis.
- `--chunk-size` (optional): Number of lines per chunk. Default is `1000`.
- `--output` (optional): Path to save the final analysis report. Default is `analysis_report.txt`.
- `--verbose` (optional): Enable verbose logging.


## 📄 License

This project is licensed under the [MIT License](LICENSE). 📝
