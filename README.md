# Research Assistant

Research Assistant is a program that utilizes a Language Model (LLM) to chat with users over one or multiple documents. It is built using OpenAI's powerful GPT-based language model, enabling interactive and context-aware conversations.

## Overview

Research Assistant is designed to assist users in obtaining information, answering questions, and engaging in natural language conversations. By leveraging the capabilities of the Language Model, it can provide insightful responses and context-specific information based on the given documents.

## Requirements

To use Research Assistant, you need the following:

- Python 3.x
- OpenAI API Key

## Usage

1. Install the required dependencies by running the following command:
   `pip install -r requirements.txt`
2. Set your OpenAI API key as an environment variable:
   'export OPENAI_API_KEY=your_api_key'
   modifying the `config.py` file.
3. Alternatively, you can set the API key in the code itself by running the shell script `set_api_key.sh` (remember to chmod +x the script) to set the API key:

`./set_api_key.sh`

5. Follow the instructions prompted by the program to have a conversation with Research Assistant.

## Features

- Interactive conversation mode with Research Assistant
- Ability to provide one or multiple documents for context
- Context-aware responses based on the given documents

## References

- [OpenAI GPT](https://openai.com/)
- [OpenAI API Documentation](link-to-api-documentation)

## Author

Your Name

## License

This project is licensed under the License Name. Please see the [license.txt](license.txt) file for more information.
