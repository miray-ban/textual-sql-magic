import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# List available models
models = genai.list_models()

# Inspect model object attributes
for model in models:
    print(f"Model Object: {model}")
    print(f"Available attributes and methods: {dir(model)}")
