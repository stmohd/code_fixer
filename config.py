import os
from dotenv import load_dotenv

load_dotenv()

load_dotenv(dotenv_path="./.env.example")
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

