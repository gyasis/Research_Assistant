#!/bin/bash

# Prompt the user to enter the API key
read -p "Enter your API key: " api_key

# Set the API key as an environment variable
export OPENAI_API_KEY="$api_key"

# Save the API key to a file for future use
echo "export OPENAI_API_KEY=$api_key" > api_key.env

echo "API key set and saved."
