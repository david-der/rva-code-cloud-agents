"""Text generation agent using OpenAI"""

from .base_agent import BaseAgent
from typing import Optional, Dict, Any

class TextAgent(BaseAgent):
    def generate(self, 
                prompt: str,
                model: str = "gpt-4-turbo-preview",
                temperature: float = 0.7,
                max_tokens: Optional[int] = None,
                **kwargs) -> Dict[str, Any]:
        """
        Generate text using OpenAI's API
        
        Args:
            prompt: The text prompt to generate from
            model: The OpenAI model to use
            temperature: Controls randomness (0.0-2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments for completion
        
        Returns:
            dict: Response containing generated text and usage statistics
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return {
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        } 