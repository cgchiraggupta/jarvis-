
"""
Assistant API Adapter for Self-Operating Computer

This module provides an adapter to integrate OpenAI's GPT-4 Vision directly,
replacing the external Node.js server. It manages conversation history
to allow for stateful computer control.
"""

import base64
import json
import os
import time
import traceback
import io
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

from operate.config import Config
from operate.utils.screenshot import capture_screen_with_cursor
from operate.utils.style import ANSI_BRIGHT_MAGENTA, ANSI_GREEN, ANSI_RED, ANSI_RESET

# Load configuration
config = Config()

SYSTEM_PROMPT = """You are an AI assistant that helps control a computer by analyzing screenshots and providing precise instructions.

When given a screenshot and an objective, you should:
1. Analyze the current screen state carefully
2. Determine the next logical action to achieve the objective
3. Respond with a JSON array of operations

Available operations:
- click: Click at specific coordinates {"operation": "click", "x": 100, "y": 200, "thought": "clicking the button"}
- write: Type text {"operation": "write", "content": "text to type", "thought": "entering text"}
- press: Press keyboard keys {"operation": "press", "keys": ["cmd", "space"], "thought": "opening spotlight"}
- done: Mark task complete {"operation": "done", "summary": "task completed", "thought": "objective achieved"}

Coordinates should be in pixels from the top-left corner (0,0).
Always provide a "thought" field explaining your reasoning.

Respond ONLY with a valid JSON array. Example:
[{"operation": "click", "x": 150, "y": 300, "thought": "Clicking the Safari icon to open browser"}]"""

class AssistantAdapter:
    """
    Adapter for communicating directly with OpenAI's API.
    """

    def __init__(self):
        self.client = config.initialize_openai()

    def encode_screenshot(self, screenshot_path):
        """
        Encode a screenshot as base64 with compression to reduce token usage.
        """
        MAX_SIZE = (1920, 1080)
        QUALITY = 85
        
        try:
            with Image.open(screenshot_path) as img:
                # resize to max dims if larger
                img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                
                # convert to RGB (remove alpha) for JPEG compression
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=QUALITY)
                return base64.b64encode(buffer.getvalue()).decode("utf-8")
        except Exception as e:
            if config.verbose:
                print(f"[AssistantAdapter] Optimization failed, falling back to raw: {e}")
            
            with open(screenshot_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")

    def format_messages(self, messages, objective, screenshot_base64):
        """
        Format messages for the OpenAI API, including history and the new screenshot.
        """
        openai_messages = []
        
        # Add system prompt
        openai_messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

        # Rebuild history
        # Skip the original system prompt from operate.py
        start_index = 1 if len(messages) > 0 and messages[0].get("role") == "system" else 0
        
        for msg in messages[start_index:]:
            openai_messages.append(msg)

        # Create the new user message with image
        user_content = [
            {
                "type": "text", 
                "text": f"Objective: {objective}. Based on this screenshot, what should I do next?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{screenshot_base64}",
                },
            }
        ]
        
        openai_messages.append({
            "role": "user",
            "content": user_content
        })
        
        return openai_messages

    def parse_response(self, response_content):
        """
        Parse the JSON response from the model.
        """
        try:
            cleaned = response_content.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            operations = json.loads(cleaned)
            
            if not isinstance(operations, list):
                operations = [operations]
                
            return operations
        except json.JSONDecodeError as e:
            if config.verbose:
                print(f"[AssistantAdapter] JSON decode error: {e}")
                print(f"[AssistantAdapter] Response was: {response_content}")
            return [{
                "operation": "done", 
                "summary": "Failed to parse AI response", 
                "thought": "The AI response was not valid JSON."
            }]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def call_api(self, messages):
        """
        Call OpenAI API with retry logic.
        """
        try:
            if config.verbose:
                print("[AssistantAdapter] Calling OpenAI GPT-4 Vision...")

            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"{ANSI_RED}[AssistantAdapter] API call failed, retrying... ({str(e)}){ANSI_RESET}")
            raise


async def call_assistant_with_vision(messages, objective, model):
    """
    Main function to call the Assistant API (now direct OpenAI).
    """
    if config.verbose:
        print("[call_assistant_with_vision]")

    try:
        adapter = AssistantAdapter()

        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        screenshot_filename = os.path.join(screenshots_dir, "screenshot.png")
        capture_screen_with_cursor(screenshot_filename)
        
        # Optimize and Encode
        screenshot_base64 = adapter.encode_screenshot(screenshot_filename)
        
        api_messages = adapter.format_messages(messages, objective, screenshot_base64)

        response_text = adapter.call_api(api_messages)
        
        if config.verbose:
            print(f"[call_assistant_with_vision] Response: {response_text}")

        operations = adapter.parse_response(response_text)
        
        # Update history
        user_msg = {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Objective: {objective}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{screenshot_base64}"}}
            ]
        }
        messages.append(user_msg)
        
        assistant_msg = {
            "role": "assistant", 
            "content": response_text
        }
        messages.append(assistant_msg)

        return operations

    except Exception as e:
        print(f"{ANSI_RED}Error in assistant call: {e}{ANSI_RESET}")
        traceback.print_exc()
        raise
