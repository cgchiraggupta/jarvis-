import pyautogui
import platform
import time
import math
import re

from operate.utils.misc import convert_percent_to_decimal
from operate.utils.style import ANSI_RED, ANSI_RESET

class OperatingSystem:
    def validate_action(self, action_type, content=None):
        """
        Validate actions to prevent dangerous operations.
        """
        if action_type == "write" and content:
            dangerous_patterns = [
                r'rm\s+-rf',  # Recursive delete
                r'mkfs',      # Format filesystem
                r'>\s*/dev/sd', # Overwrite device
                r'dd\s+if=',  # Direct disk write
                r':\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\};\s*:', # Fork bomb
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    print(f"{ANSI_RED}[Security Block] Prevented execution of dangerous pattern: {pattern}{ANSI_RESET}")
                    return False
        return True

    def write(self, content):
        if not self.validate_action("write", content):
            return

        try:
            content = content.replace("\\n", "\n")
            for char in content:
                pyautogui.write(char)
        except Exception as e:
            print("[OperatingSystem][write] error:", e)

    def press(self, keys):
        try:
            for key in keys:
                pyautogui.keyDown(key)
            time.sleep(0.1)
            for key in keys:
                pyautogui.keyUp(key)
        except Exception as e:
            print("[OperatingSystem][press] error:", e)

    def mouse(self, click_detail):
        try:
            x = convert_percent_to_decimal(click_detail.get("x"))
            y = convert_percent_to_decimal(click_detail.get("y"))

            if click_detail and isinstance(x, float) and isinstance(y, float):
                self.click_at_percentage(x, y)

        except Exception as e:
            print("[OperatingSystem][mouse] error:", e)

    def click_at_percentage(
        self,
        x_percentage,
        y_percentage,
        duration=0.2,
        circle_radius=50,
        circle_duration=0.5,
    ):
        try:
            screen_width, screen_height = pyautogui.size()
            x_pixel = int(screen_width * float(x_percentage))
            y_pixel = int(screen_height * float(y_percentage))

            pyautogui.moveTo(x_pixel, y_pixel, duration=duration)

            start_time = time.time()
            while time.time() - start_time < circle_duration:
                angle = ((time.time() - start_time) / circle_duration) * 2 * math.pi
                x = x_pixel + math.cos(angle) * circle_radius
                y = y_pixel + math.sin(angle) * circle_radius
                pyautogui.moveTo(x, y, duration=0.1)

            pyautogui.click(x_pixel, y_pixel)
        except Exception as e:
            print("[OperatingSystem][click_at_percentage] error:", e)
