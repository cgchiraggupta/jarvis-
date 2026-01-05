#!/usr/bin/env python3
"""
Example API Usage for Assistant Integration

This script demonstrates how to use the Assistant API programmatically
without going through the full self-operating-computer framework.
"""

import requests
import base64
import json
import sys
from PIL import Image, ImageDraw, ImageFont
import io


def create_sample_screenshot():
    """Create a sample desktop screenshot for testing"""
    # Create a fake desktop screenshot
    img = Image.new('RGB', (1920, 1080), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple desktop with some icons
    # Safari icon (blue circle)
    draw.ellipse([50, 950, 150, 1050], fill='#0066CC', outline='white', width=3)
    draw.text((85, 990), "Safari", fill='white')
    
    # VS Code icon (blue square)
    draw.rectangle([200, 950, 300, 1050], fill='#007ACC', outline='white', width=3)
    draw.text((220, 990), "Code", fill='white')
    
    # Terminal icon (black square)
    draw.rectangle([350, 950, 450, 1050], fill='#000000', outline='white', width=3)
    draw.text((355, 990), "Terminal", fill='white')
    
    # Menu bar
    draw.rectangle([0, 0, 1920, 30], fill='#333333')
    draw.text((10, 5), "  Finder  File  Edit  View  Go  Window  Help", fill='white')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def test_assistant_api(image_base64, objective):
    """
    Send a request to the Assistant API and get back actions
    
    Args:
        image_base64: Base64-encoded screenshot
        objective: What you want to accomplish
        
    Returns:
        List of operations to perform
    """
    url = "http://localhost:4001/analyze"
    
    payload = {
        "image": image_base64,
        "prompt": f"Help me achieve this: {objective}",
        "objective": objective,
        "format": "json"
    }
    
    print(f"🔍 Sending request to Assistant API...")
    print(f"   Objective: {objective}")
    print(f"   Image size: {len(image_base64)} bytes")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✅ Received response from Assistant")
        print(f"   Model: {data.get('model', 'unknown')}")
        print(f"   Operations: {len(data.get('operations', []))}")
        
        return data.get('operations', [])
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Assistant API at http://localhost:4001")
        print("   Make sure the server is running: ./start_assistant.sh")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def display_operations(operations):
    """Pretty print the operations"""
    if not operations:
        print("No operations returned")
        return
    
    print("\n" + "="*60)
    print("📋 Planned Operations:")
    print("="*60)
    
    for i, op in enumerate(operations, 1):
        op_type = op.get('operation', 'unknown')
        thought = op.get('thought', 'No explanation provided')
        
        print(f"\n{i}. {op_type.upper()}")
        print(f"   💭 {thought}")
        
        if op_type == 'click':
            print(f"   📍 Coordinates: ({op.get('x')}, {op.get('y')})")
        elif op_type == 'write':
            print(f"   ⌨️  Content: {op.get('content')}")
        elif op_type == 'press':
            print(f"   🔘 Keys: {op.get('keys')}")
        elif op_type == 'done':
            print(f"   ✅ Summary: {op.get('summary')}")
    
    print("\n" + "="*60)


def main():
    """Main example script"""
    print("="*60)
    print("🤖 Assistant API Example Usage")
    print("="*60)
    print()
    
    # Check if server is running
    try:
        health = requests.get("http://localhost:4001/health", timeout=2)
        if health.status_code == 200:
            print("✅ Assistant API is running")
        else:
            print("⚠️  Assistant API returned unexpected status")
    except:
        print("❌ Assistant API is not running")
        print("   Start it with: ./start_assistant.sh")
        sys.exit(1)
    
    print()
    
    # Example 1: Using a sample screenshot
    print("Example 1: Testing with sample screenshot")
    print("-" * 60)
    
    sample_img = create_sample_screenshot()
    objective = "open Safari"
    
    operations = test_assistant_api(sample_img, objective)
    if operations:
        display_operations(operations)
    
    print()
    
    # Example 2: Using a real screenshot (if mss is available)
    try:
        import mss
        import mss.tools
        
        print("\nExample 2: Testing with real screenshot")
        print("-" * 60)
        
        with mss.mss() as sct:
            # Capture the primary monitor
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            real_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            objective = input("\nEnter your objective (or press Enter for 'open Safari'): ").strip()
            if not objective:
                objective = "open Safari"
            
            operations = test_assistant_api(real_img, objective)
            if operations:
                display_operations(operations)
    
    except ImportError:
        print("\nℹ️  Install 'mss' to test with real screenshots: pip install mss")
    
    print("\n" + "="*60)
    print("Example script completed!")
    print("="*60)


if __name__ == "__main__":
    main()




