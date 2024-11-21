"""
OpenAI agents for text and image generation
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import webbrowser
from typing import Literal, Optional, Union, Dict
import json

class OpenAIAgent:
    """Base class for OpenAI interactions"""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=self.api_key)

class TextAgent(OpenAIAgent):
    """Agent for text generation using GPT models"""
    
    def __init__(self, model: str = "gpt-4o"):
        super().__init__()
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> Dict:
        """
        Generate text response from prompt
        
        Args:
            prompt: The text prompt
            **kwargs: Additional arguments for OpenAI API
            
        Returns:
            Dict containing response content and metadata
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": self.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }

class ImageAgent(OpenAIAgent):
    """Agent for image generation using DALL-E"""
    
    def __init__(self, model: str = "dall-e-3"):
        super().__init__()
        self.model = model
    
    def generate(
        self, 
        prompt: str,
        size: Literal["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"] = "1792x1024",
        quality: Literal["standard", "hd"] = "standard",
        n: int = 1,
        **kwargs
    ) -> Dict:
        """
        Generate image from prompt
        
        Args:
            prompt: The image description
            size: Image size (default: "1792x1024" - best for widescreen/PowerPoint)
            quality: Image quality (default: "standard")
            n: Number of images (default: 1)
            **kwargs: Additional arguments for OpenAI API
            
        Returns:
            Dict containing image URL and metadata
        """
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
            **kwargs
        )
        
        result = {
            "urls": [img.url for img in response.data],
            "model": self.model,
            "size": size,
            "quality": quality
        }
        
        # Automatically open image in browser
        if result["urls"]:
            webbrowser.open(result["urls"][0])
            
        return result