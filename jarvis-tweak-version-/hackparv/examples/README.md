# Examples Directory

This directory contains example scripts and workflows for using the Self-Operating Computer + Assistant integration.

## 📁 Files

### `example_workflows.sh`
Interactive menu-driven script with common automation tasks.

**Usage**:
```bash
cd examples
./example_workflows.sh
```

**Features**:
- Pre-configured common tasks
- Interactive menu
- Categories: Apps, Web, Search, Development, Productivity
- Custom command option

### `example_api_usage.py`
Python script demonstrating direct API usage without the full framework.

**Usage**:
```bash
cd examples
./example_api_usage.py
```

**Features**:
- Tests Assistant API connection
- Demonstrates API request/response format
- Shows how to parse operations
- Works with sample or real screenshots

## 🚀 Quick Examples

### Open Applications
```bash
# Using the framework
operate --model=assistant --prompt="open Safari"
operate --model=assistant --prompt="open VS Code"
operate --model=assistant --prompt="open Terminal"
```

### Web Browsing
```bash
operate --model=assistant --prompt="open Safari and go to github.com"
operate --model=assistant --prompt="open google.com and search for Python"
```

### Development Tasks
```bash
operate --model=assistant --prompt="open VS Code and Terminal side by side"
operate --model=assistant --prompt="open iTerm and navigate to Documents"
```

### Productivity
```bash
operate --model=assistant --prompt="open Notes and create a new note"
operate --model=assistant --prompt="open Mail and check inbox"
```

## 💡 Creating Your Own Scripts

### Python Script Template

```python
#!/usr/bin/env python3
import requests
import base64

def my_automation_task():
    # 1. Prepare your screenshot (base64 encoded)
    with open('screenshot.png', 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # 2. Define your objective
    objective = "open Safari and go to github.com"
    
    # 3. Call the API
    response = requests.post('http://localhost:4001/analyze', json={
        'image': img_base64,
        'prompt': f'Help me: {objective}',
        'objective': objective
    })
    
    # 4. Process the response
    operations = response.json()['operations']
    
    # 5. Execute or log operations
    for op in operations:
        print(f"Operation: {op['operation']}")
        print(f"Thought: {op['thought']}")
        # Execute using pyautogui or other automation library

if __name__ == '__main__':
    my_automation_task()
```

### Bash Script Template

```bash
#!/bin/bash

# Your automation workflow
operate --model=assistant --prompt="step 1: open Safari"
sleep 2
operate --model=assistant --prompt="step 2: navigate to github.com"
sleep 2
operate --model=assistant --prompt="step 3: search for python projects"
```

## 🎯 Common Patterns

### Pattern: Sequential Tasks
Execute multiple steps in sequence:

```bash
#!/bin/bash
operate --model=assistant --prompt="open Finder"
sleep 3
operate --model=assistant --prompt="navigate to Documents folder"
sleep 3
operate --model=assistant --prompt="create a new folder called Projects"
```

### Pattern: Conditional Execution
Execute based on conditions:

```python
#!/usr/bin/env python3
import subprocess
import sys

def run_command(cmd):
    result = subprocess.run(
        ['operate', '--model=assistant', '--prompt', cmd],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

# Try to open Safari, fallback to Chrome if it fails
if not run_command("open Safari"):
    print("Safari failed, trying Chrome...")
    run_command("open Chrome")
```

### Pattern: Looping Tasks
Repeat tasks:

```python
#!/usr/bin/env python3
import subprocess
import time

tasks = [
    "open Safari",
    "go to github.com",
    "search for python projects"
]

for task in tasks:
    print(f"Executing: {task}")
    subprocess.run(['operate', '--model=assistant', '--prompt', task])
    time.sleep(3)  # Wait between tasks
```

## 📊 Monitoring Results

Add verbose mode to see what's happening:

```bash
operate --model=assistant --verbose --prompt="your command"
```

Check the screenshots:
```bash
ls -lah ../self-operating-computer/screenshots/
open ../self-operating-computer/screenshots/screenshot.png
```

## 🐛 Debugging Examples

### Test API Connectivity
```python
#!/usr/bin/env python3
import requests

try:
    r = requests.get('http://localhost:4001/health', timeout=2)
    print(f"API Status: {r.json()}")
except Exception as e:
    print(f"API Error: {e}")
```

### Test Screenshot Capture
```python
#!/usr/bin/env python3
import sys
sys.path.append('../self-operating-computer')
from operate.utils.screenshot import capture_screen_with_cursor

capture_screen_with_cursor('test_screenshot.png')
print("Screenshot saved to test_screenshot.png")
```

### Test Action Execution
```python
#!/usr/bin/env python3
import pyautogui
import time

# Test mouse movement
pyautogui.moveTo(100, 100, duration=1)
time.sleep(1)

# Test click
pyautogui.click()
time.sleep(1)

# Test keyboard
pyautogui.typewrite('Hello World', interval=0.1)
```

## 📚 Additional Resources

- **Full Documentation**: See `../INTEGRATION_README.md`
- **Usage Guide**: See `../USAGE_GUIDE.md`
- **Quick Start**: See `../QUICKSTART.md`

## 🤝 Contributing Examples

Have a useful automation script? Add it to this directory!

1. Create your script
2. Make it executable: `chmod +x your_script.sh`
3. Add documentation to this README
4. Test it thoroughly
5. Share with the community

---

**Happy automating!** 🚀




