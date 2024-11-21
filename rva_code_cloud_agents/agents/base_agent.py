"""Base agent class with shared functionality"""

from openai import OpenAI
import os
from dotenv import load_dotenv

class BaseAgent:
    def __init__(self):
        """Initialize the base agent with OpenAI client"""
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)

    def generate(self, *args, **kwargs):
        """Abstract method to be implemented by child classes"""
        raise NotImplementedError("Subclasses must implement generate()") 