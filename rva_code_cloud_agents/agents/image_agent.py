"""Image generation agent using OpenAI"""

from .base_agent import BaseAgent
from typing import Dict, Any, Literal
import os
import requests
from PIL import Image
import io

class ImageAgent(BaseAgent):
    def generate(self,
                prompt: str,
                model: str = "dall-e-3",
                size: Literal["1024x1024", "1792x1024", "1024x1792"] = "1792x1024",
                quality: Literal["standard", "hd"] = "standard",
                output_dir: str = "output",
                n: int = 1,
                **kwargs) -> Dict[str, Any]:
        """
        Generate images using OpenAI's DALL-E API and save locally
        
        Args:
            prompt: The image description to generate from
            model: The DALL-E model to use
            size: Image size (1024x1024, 1792x1024, or 1024x1792)
            quality: Image quality (standard or hd)
            output_dir: Directory to save the image
            n: Number of images to generate
            **kwargs: Additional arguments for image generation
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        image_path = os.path.join(output_dir, "generated_image.png")
        
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
            **kwargs
        )
        
        # Download and save the image
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        image.save(image_path)
        
        return {
            "urls": [image.url for image in response.data],
            "size": size,
            "quality": quality,
            "model": model,
            "image_path": image_path
        } 