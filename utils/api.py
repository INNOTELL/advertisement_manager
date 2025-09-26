import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get base URL from environment variable, fallback to default
base_url = os.getenv("BACKEND_BASE_URL", "https://advertisement-management-api-c2jb.onrender.com")

# Get AI API key from environment variable
ai_api_key = os.getenv("AI_API_KEY", "")