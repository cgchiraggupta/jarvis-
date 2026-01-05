# Usage Guide: Self-Operating Computer + Assistant Integration

This guide provides practical examples and workflows for using the integrated system.

## 🎬 Quick Start

### 1. Start the Assistant API

```bash
# From project root
./start_assistant.sh
```

Wait for confirmation messages:
```
✅ Servers started successfully!
WebSocket server running at ws://localhost:4000/Assistant
🚀 Assistant HTTP API Server running on port 4001
```

### 2. Run Your First Command

In a new terminal:

```bash
cd self-operating-computer
source venv/bin/activate  # if using virtual environment
operate --model=assistant --prompt="open Safari"
```

## 📖 Usage Patterns

### Pattern 1: Simple Application Launch

**Goal**: Open applications on your Mac

```bash
# Open web browser
operate --model=assistant --prompt="open Safari"
operate --model=assistant --prompt="launch Chrome"

# Open development tools
operate --model=assistant --prompt="open VS Code"
operate --model=assistant --prompt="open Terminal"

# Open productivity apps
operate --model=assistant --prompt="open Notes"
operate --model=assistant --prompt="launch Slack"
```

**How it works**:
1. AI sees your desktop
2. Identifies the application icon or uses Spotlight
3. Clicks to launch or uses keyboard shortcut (Cmd+Space)

### Pattern 2: Web Navigation

**Goal**: Navigate to websites

```bash
# Direct URL
operate --model=assistant --prompt="open google.com in Safari"
operate --model=assistant --prompt="go to github.com"

# Search and navigate
operate --model=assistant --prompt="open YouTube and search for Python tutorials"
operate --model=assistant --prompt="go to Gmail"
```

**Example Flow**:
```
User: "open github.com"
  ↓
AI: Click Safari icon → Type "github.com" → Press Enter
  ↓
Result: GitHub opens in browser
```

### Pattern 3: Search Tasks

**Goal**: Perform web searches

```bash
# Google search
operate --model=assistant --prompt="search Google for weather forecast"
operate --model=assistant --prompt="find restaurants near me"

# Specific searches
operate --model=assistant --prompt="search for Python documentation"
operate --model=assistant --prompt="look up how to center a div in CSS"
```

### Pattern 4: File Management

**Goal**: Navigate and manage files

```bash
# Open Finder
operate --model=assistant --prompt="open Finder and go to Documents"
operate --model=assistant --prompt="show me my Downloads folder"

# Create folders (via Terminal)
operate --model=assistant --prompt="open Terminal and create a new folder called Projects"
```

### Pattern 5: Multi-Step Workflows

**Goal**: Complete complex tasks requiring multiple actions

```bash
# Research workflow
operate --model=assistant --prompt="open Safari, go to Wikipedia, and search for quantum computing"

# Development setup
operate --model=assistant --prompt="open VS Code and Terminal side by side"

# Communication
operate --model=assistant --prompt="open Mail and compose a new message"
```

**Example Multi-Step Flow**:
```
User: "open Safari and search for cats"
  ↓
AI Step 1: Click Safari icon (or Cmd+Space → type Safari)
AI Step 2: Wait for Safari to open
AI Step 3: Click address bar
AI Step 4: Type "google.com/search?q=cats"
AI Step 5: Press Enter
AI Step 6: Mark as done
  ↓
Result: Safari shows Google search results for "cats"
```

## 🎯 Interactive Mode

For exploratory tasks, use interactive mode without `--prompt`:

```bash
operate --model=assistant
```

You'll be prompted to enter your objective:
```
[Self-Operating Computer | assistant]
What would you like me to do?

[User]
> open Notes and create a new note
```

The AI will then:
1. Capture your screen
2. Determine the next action
3. Execute it
4. Repeat until the objective is complete (or 10 iterations)

## 🎤 Voice Mode (Optional)

If you installed voice dependencies:

```bash
# Install voice requirements
pip install -r requirements-audio.txt

# Use voice mode
operate --model=assistant --voice
```

Speak your command instead of typing.

## 📊 Understanding the Process

### What Happens Behind the Scenes

```
[User Command] → "open Safari"
       ↓
[Screenshot] → Captures current desktop state
       ↓
[Encode] → Converts to base64
       ↓
[HTTP POST] → Sends to Assistant API at localhost:4001/analyze
       ↓
[GPT-4 Vision] → AI analyzes the screenshot
       ↓
[Response] → Returns JSON actions:
       [
         {
           "operation": "click",
           "x": 156,
           "y": 234,
           "thought": "Clicking Safari icon in dock"
         }
       ]
       ↓
[Execute] → Performs mouse click at (156, 234)
       ↓
[Screenshot] → Captures new state
       ↓
[Repeat] → Until objective complete or max iterations
       ↓
[Done] → Task completed!
```

### Verbose Mode

See exactly what's happening:

```bash
operate --model=assistant --verbose --prompt="open Safari"
```

Output includes:
```
[Self-Operating Computer][get_next_action] model assistant
[call_assistant_with_vision]
[call_assistant_with_vision] Sending request to Assistant
[call_assistant_with_vision] Objective: open Safari
[AssistantAdapter] Calling API at http://localhost:4001/analyze
[call_assistant_with_vision] Received response: {...}
[call_assistant_with_vision] Parsed operations: [...]
[Self Operating Computer][operate] operation click
[Self Operating Computer][operate] operate_type click
```

## 🎨 Advanced Examples

### Example 1: Research Workflow

```bash
operate --model=assistant --prompt="open Safari, go to scholar.google.com, and search for machine learning papers from 2024"
```

**AI Actions**:
1. Click Safari icon or use Spotlight
2. Wait for browser to open
3. Click address bar
4. Type "scholar.google.com"
5. Press Enter
6. Wait for page load
7. Find search box
8. Click search box
9. Type "machine learning 2024"
10. Press Enter
11. Done

### Example 2: Development Setup

```bash
operate --model=assistant --prompt="open iTerm2, create a new window, and navigate to my Documents folder"
```

**AI Actions**:
1. Open Spotlight (Cmd+Space)
2. Type "iTerm"
3. Press Enter
4. Wait for iTerm to open
5. Type "cd ~/Documents"
6. Press Enter
7. Done

### Example 3: Communication

```bash
operate --model=assistant --prompt="open Slack and go to the general channel"
```

**AI Actions**:
1. Identify Slack in dock or use Spotlight
2. Click to open
3. Wait for Slack to load
4. Look for "general" channel in sidebar
5. Click on "general"
6. Done

## 🛠️ Customization

### Custom System Prompts

Edit `self-operating-computer/operate/models/assistant_adapter.py`:

```python
def prepare_prompt(self, objective, is_first_message=False):
    if is_first_message:
        return f"""Custom instructions here...
        
Objective: {objective}

Your custom format and rules...
"""
    else:
        return "Continue with the next action..."
```

### Adjusting Max Iterations

Edit `self-operating-computer/operate/operate.py`:

```python
loop_count = 0

while True:
    # ... existing code ...
    
    loop_count += 1
    if loop_count > 20:  # Changed from 10 to 20
        break
```

### Custom Actions

To add a new action type (e.g., "scroll"):

**1. Update Assistant API** (`jarvis/server/http_server.js`):
```javascript
const systemPrompt = `...
Available operations:
- scroll: Scroll the screen {"operation": "scroll", "direction": "down", "amount": 3, "thought": "scrolling"}
...`;
```

**2. Update Python Adapter** (`operate/models/assistant_adapter.py`):
```python
# In parse_response method
if operation_type == "scroll":
    if "direction" not in op:
        continue
    if "amount" not in op:
        op["amount"] = 1
```

**3. Update Operate Handler** (`operate/operate.py`):
```python
# In operate function
elif operate_type == "scroll":
    direction = operation.get("direction")
    amount = operation.get("amount", 1)
    operate_detail = f"{direction} {amount}"
    # Implement scroll logic using PyAutoGUI
    import pyautogui
    if direction == "down":
        pyautogui.scroll(-amount * 100)
    elif direction == "up":
        pyautogui.scroll(amount * 100)
```

## 📈 Performance Tips

### 1. Use Specific Prompts

❌ Bad: "do something with Safari"
✅ Good: "open Safari and go to github.com"

### 2. Break Down Complex Tasks

Instead of:
```bash
operate --model=assistant --prompt="open Safari, search for Python tutorials, click the first result, copy the code example, open VS Code, create a new file, and paste the code"
```

Use multiple commands:
```bash
operate --model=assistant --prompt="open Safari and search for Python tutorials"
# Then manually copy what you need
operate --model=assistant --prompt="open VS Code and create a new Python file"
# Then manually paste
```

### 3. Use Verbose Mode for Debugging

When things don't work as expected:
```bash
operate --model=assistant --verbose --prompt="your command"
```

### 4. Check Permissions First

Before running complex workflows:
```bash
python3 test_integration.py
```

## 🔍 Monitoring and Debugging

### Check API Health

```bash
curl http://localhost:4001/health
```

Expected response:
```json
{"status":"ok","service":"Assistant API","version":"1.0.0"}
```

### Test API Directly

```bash
# Create a test image
python3 -c "
from PIL import Image
import base64, io
img = Image.new('RGB', (100, 100), 'red')
buf = io.BytesIO()
img.save(buf, format='PNG')
print(base64.b64encode(buf.getvalue()).decode())
" > /tmp/test_img.txt

# Test the API
curl -X POST http://localhost:4001/analyze \
  -H "Content-Type: application/json" \
  -d "{\"image\":\"$(cat /tmp/test_img.txt)\",\"prompt\":\"What do you see?\",\"objective\":\"test\"}"
```

### View Screenshots

Screenshots are saved in `self-operating-computer/screenshots/`:
```bash
cd self-operating-computer/screenshots
ls -lah
open screenshot.png  # View the latest screenshot
```

### Check Logs

**Assistant API**:
- Logs appear in the terminal where you ran `start_assistant.sh`
- Look for `[Assistant API]` prefixed messages

**Self-Operating Computer**:
- Use `--verbose` flag to see detailed logs
- Errors appear in red with `[Error]` prefix

## 🚫 Common Pitfalls

### 1. Forgetting to Start Assistant API

**Error**: "Could not connect to Assistant API"

**Solution**:
```bash
./start_assistant.sh
```

### 2. Incorrect API Key

**Error**: "Invalid API key" or 401 errors

**Solution**:
```bash
cd jarvis/server
nano .env  # Check KEY and OPENAI_API_KEY
```

### 3. Permission Issues

**Error**: Screenshot capture fails or clicks don't register

**Solution**: Grant Screen Recording and Accessibility permissions (see INTEGRATION_README.md)

### 4. Port Already in Use

**Error**: "EADDRINUSE: address already in use :::4001"

**Solution**:
```bash
# Find process using port 4001
lsof -i :4001

# Kill it
kill -9 <PID>

# Or use different port
export HTTP_PORT=4002
```

### 5. Outdated Dependencies

**Error**: Module import errors

**Solution**:
```bash
# Python
cd self-operating-computer
pip install --upgrade -r requirements.txt

# Node.js
cd jarvis/server
npm install
```

## 📚 Next Steps

1. **Experiment**: Try different commands and see what works
2. **Customize**: Modify prompts and actions for your needs
3. **Extend**: Add new operation types or integrate with other services
4. **Share**: Document your use cases and improvements

## 🎓 Learning Resources

- **Self-Operating Computer**: https://github.com/OthersideAI/self-operating-computer
- **OpenAI Vision API**: https://platform.openai.com/docs/guides/vision
- **PyAutoGUI Docs**: https://pyautogui.readthedocs.io/
- **Express.js**: https://expressjs.com/

---

**Need more help?** Check `INTEGRATION_README.md` for detailed documentation.

**Happy automating!** 🎉




