"""
Main module for RVA Code Cloud Agents with loading animation
"""

import os
import threading
import time
import sys
from typing import Literal
from .agents import TextAgent, ImageAgent

class AnimationState:
    def __init__(self):
        self.current_frame = 0
        self.response_received = False
        self.last_frame_time = time.time()

def loading_animation(stop_event, state):
    """Create loading animation with realtime counter"""
    # [Previous animation code remains the same...]
    # Note: I've removed it here for brevity but it's the same as before

def run_with_animation(agent_type: Literal["text", "image"], prompt: str, **kwargs):
    """
    Run either text or image generation with loading animation
    
    Args:
        agent_type: "text" or "image"
        prompt: The prompt to send
        **kwargs: Additional arguments for the specific agent
    """
    # Set up and start the animation
    stop_animation = threading.Event()
    animation_state = AnimationState()
    animation_thread = threading.Thread(target=loading_animation, args=(stop_animation, animation_state))
    animation_thread.start()
    
    try:
        # Create appropriate agent and generate response
        if agent_type == "text":
            agent = TextAgent()
        else:
            agent = ImageAgent()
            
        response = agent.generate(prompt, **kwargs)
        
        # Signal that response was received
        animation_state.response_received = True
        time.sleep(0.8)  # Give time for animation to finish
        
        return response
        
    finally:
        # Stop the animation
        stop_animation.set()
        animation_thread.join()
        
        # Clear screen one last time
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Example usage of both agents"""
    # Example text generation
    text_response = run_with_animation(
        "text",
        "What are three interesting facts about Richmond, Virginia?"
    )
    print("\nText Generation Response:")
    print("═" * 50)
    print(text_response["content"])
    print("═" * 50)
    print(f"Token Usage: {text_response['usage']}")
    
    # Example image generation
    image_response = run_with_animation(
        "image",
        "A beautiful sunset over Richmond, Virginia skyline with the James River in the foreground",
        size="1792x1024",
        quality="standard"
    )
    print("\nImage Generation Response:")
    print("═" * 50)
    print(f"Image URL: {image_response['urls'][0]}")
    print(f"Size: {image_response['size']}")
    print(f"Quality: {image_response['quality']}")
    print("═" * 50)
    print("Opening image in browser...")

if __name__ == "__main__":
    main()