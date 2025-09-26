import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv('BACKEND_BASE_URL', 'https://advertisement-management-api-c2jb.onrender.com')
ai_api_key = os.getenv('AI_API_KEY', '')

