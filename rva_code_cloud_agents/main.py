"""
Main module for RVA Code Cloud Agents with loading animation
"""

import sys
import time
import threading
from typing import Literal
from .agents import TextAgent, ImageAgent, PowerPointAgent
from datetime import datetime
import os
import shutil

class AnimationState:
    def __init__(self):
        self.current_frame = 0
        self.last_frame_time = time.time()
        self.response_received = False

def loading_animation(stop_event, state):
    """Create loading animation with realtime counter"""
    frames = ["-", "\\", "|", "/"]
    
    while not stop_event.is_set():
        current_time = time.time()
        elapsed_time = current_time - state.last_frame_time
        
        if state.response_received:
            print("\rResponse received! Processing...      ", end="", flush=True)
        else:
            print(f"\r{frames[state.current_frame]} Generating response... ({elapsed_time:.1f}s)", end="", flush=True)
        
        state.current_frame = (state.current_frame + 1) % len(frames)
        time.sleep(0.1)
    
    print("\r" + " " * 50 + "\r", end="", flush=True)

def run_with_animation(agent_type: Literal["text", "image", "pptx"], prompt: str, **kwargs):
    """Run the generation with a loading animation"""
    start_time = time.time()
    
    stop_animation = threading.Event()
    animation_state = AnimationState()
    animation_thread = threading.Thread(target=loading_animation, args=(stop_animation, animation_state))
    animation_thread.start()
    
    try:
        if agent_type == "text":
            agent = TextAgent()
        elif agent_type == "image":
            agent = ImageAgent()
        else:
            agent = PowerPointAgent()
            
        response = agent.generate(prompt, **kwargs)
        
        animation_state.response_received = True
        time.sleep(0.2)
        
        print(f"\nTotal time: {time.time() - start_time:.2f} seconds")
        return response
        
    finally:
        stop_animation.set()
        animation_thread.join()

def main():
    """Handle command line arguments for different generation types"""
    if len(sys.argv) != 3:
        print("Usage: python -m rva_code_cloud_agents.main [text|image|pptx] 'your prompt here'")
        sys.exit(1)

    generation_type = sys.argv[1]
    prompt = sys.argv[2]

    if generation_type not in ["text", "image", "pptx"]:
        print("Invalid generation type. Use 'text', 'image', or 'pptx'")
        sys.exit(1)

    if generation_type == "text":
        text_response = run_with_animation(
            "text",
            prompt
        )
        print("\nText Generation Response:")
        print("═" * 50)
        print(text_response["content"])
        print("═" * 50)
        print(f"Token Usage: {text_response['usage']}")

    elif generation_type == "image":
        image_response = run_with_animation(
            "image",
            prompt,
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

    elif generation_type == "pptx":
        from datetime import datetime
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Define output directory and create it
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Define source and destination paths for chart files
        chart_files = {
            "support_tickets_business_hours.png": os.path.join(output_dir, "support_tickets_business_hours.png"),
            "support_tickets_categories_business_hours.png": os.path.join(output_dir, "support_tickets_categories_business_hours.png"),
            "support_tickets_advanced_viz.png": os.path.join(output_dir, "support_tickets_advanced_viz.png")
        }
        
        # Copy chart files to output directory
        for source, dest in chart_files.items():
            if os.path.exists(source) and not os.path.exists(dest):
                shutil.copy2(source, dest)
                print(f"Copied {source} to {dest}")
            elif not os.path.exists(source):
                print(f"Warning: Source file {source} not found")
        
        slides_config = [
            {
                "type": "title",
                "text": "Support Tickets Analysis\n\n"
                       f"{current_date}\n"
                       "Generated with AI Agents",
                "text_color": "white"
            },
            {
                "type": "chart",
                "chart_path": chart_files["support_tickets_business_hours.png"]
            },
            {
                "type": "chart",
                "chart_path": chart_files["support_tickets_categories_business_hours.png"]
            },
            {
                "type": "chart",
                "chart_path": chart_files["support_tickets_advanced_viz.png"]
            },
            {
                "type": "insights",
                "title": "Key Insights",
                "points": [
                    "**Authentication/Login Dominates**: Highest ticket volume among all categories, indicating a key issue area.",
                    "**Peak Ticket Hours**: Most tickets are submitted during weekday mornings (10 AM - 12 PM).",
                    "**Weekend Dip**: Significant decline in ticket submissions on weekends.",
                    "**Response Time Bottlenecks**: Delays most evident in \"Integration/API\" and \"Performance/Speed.\"",
                    "**Uniform Response Patterns**: Similar response times across categories, with some outliers in \"Authentication/Login.\""
                ],
                "text_color": "white"
            }
        ]
        
        pptx_response = run_with_animation(
            "pptx",
            prompt,
            slides_config=slides_config,
            output_dir=output_dir
        )
        print("\nPowerPoint Generation Response:")
        print("═" * 50)
        print(f"PowerPoint saved to: {pptx_response['pptx_path']}")
        print(f"Image saved to: {pptx_response['image_path']}")
        print("═" * 50)

    elif generation_type == "pptx-analytics":
        if len(sys.argv) != 4:
            print("Usage: pptx-analytics 'prompt' 'charts_glob_pattern'")
            sys.exit(1)
            
        import glob
        chart_files = glob.glob(sys.argv[3])
        
        slides_config = [
            {
                "type": "title",
                "text": "Analytics Dashboard",
                "text_color": "white"
            }
        ]
        
        # Add each chart as a slide
        for chart_file in chart_files:
            slides_config.append({
                "type": "chart",
                "chart_path": chart_file
            })
        
        pptx_response = run_with_animation(
            "pptx",
            sys.argv[2],  # prompt
            slides_config=slides_config
        )

if __name__ == "__main__":
    main()