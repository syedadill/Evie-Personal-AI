from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Check if the API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"API Key Loaded: {api_key[:5]}... (truncated for security)")
else:
    print("Error: OPENAI_API_KEY is not loaded.")