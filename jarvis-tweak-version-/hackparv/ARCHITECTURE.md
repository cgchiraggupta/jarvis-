# Architecture Overview

## System Design

This is a **pure Python** AI-powered computer automation system that uses GPT-4 Vision to understand and control your macOS desktop.

## High-Level Architecture

```
┌─────────────────────────────────────────────┐
│  User Input (CLI)                           │
│  "open Safari and search for Python"        │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  operate.py (Main Loop)                     │
│  • Captures screenshot                      │
│  • Calls AI model                           │
│  • Executes actions                         │
│  • Maintains conversation history           │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  AssistantAdapter (AI Integration)          │
│  • Compresses screenshots (JPEG, 1080p)     │
│  • Formats messages with history            │
│  • Calls OpenAI API (with retries)          │
│  • Parses JSON responses                    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  OpenAI GPT-4o Vision API                   │
│  • Analyzes screenshot                      │
│  • Understands context from history         │
│  • Returns action plan (JSON)               │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  OperatingSystem (Action Executor)          │
│  • Validates actions (safety checks)        │
│  • Controls mouse (click, drag)             │
│  • Controls keyboard (type, shortcuts)      │
│  • Executes on macOS via PyAutoGUI          │
└─────────────────────────────────────────────┘
```

## Data Flow

### 1. Screenshot Capture
```python
# operate.py
screenshot = capture_screen_with_cursor("screenshot.png")
```

### 2. Image Optimization
```python
# assistant_adapter.py
# Resize to max 1920x1080
# Convert to JPEG (85% quality)
# Encode to base64
optimized_image = encode_screenshot(screenshot)
```

### 3. Message Formatting
```python
# assistant_adapter.py
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    # ... previous conversation history ...
    {
        "role": "user",
        "content": [
            {"type": "text", "text": f"Objective: {objective}"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}
        ]
    }
]
```

### 4. API Call (with Retry)
```python
# assistant_adapter.py
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_api(messages):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message.content
```

### 5. Response Parsing
```python
# Example response from GPT-4o:
[
    {
        "operation": "click",
        "x": 150,
        "y": 300,
        "thought": "Clicking the Safari icon"
    }
]
```

### 6. Safety Validation
```python
# operating_system.py
def validate_action(action_type, content):
    dangerous_patterns = [r'rm\s+-rf', r'mkfs', r'dd\s+if=']
    for pattern in dangerous_patterns:
        if re.search(pattern, content):
            print("[Security Block] Prevented dangerous command")
            return False
    return True
```

### 7. Action Execution
```python
# operating_system.py
if operation == "click":
    pyautogui.click(x, y)
elif operation == "write":
    if validate_action("write", content):
        pyautogui.write(content)
elif operation == "press":
    pyautogui.hotkey(*keys)
```

## Key Components

### 1. **operate.py** (Orchestrator)
- Main control loop
- Manages session state
- Coordinates between components

### 2. **assistant_adapter.py** (AI Interface)
- Direct OpenAI integration
- Image compression (70-80% size reduction)
- Retry logic (3 attempts, exponential backoff)
- Conversation history management

### 3. **operating_system.py** (Action Layer)
- Safety validation
- Mouse/keyboard control via PyAutoGUI
- macOS-specific implementations

### 4. **config.py** (Configuration)
- Environment variable loading
- API key management
- Client initialization

## Security Features

### Safety Validation
Blocks dangerous commands before execution:
- `rm -rf` (recursive delete)
- `mkfs` (disk formatting)
- `dd if=` (direct disk write)
- Fork bombs
- System-critical operations

### Permissions Required
- **Screen Recording** - To capture screenshots
- **Accessibility** - To control mouse/keyboard

## Performance Optimizations

### Image Compression
- **Before**: ~5-10 MB PNG screenshots
- **After**: ~0.5-1 MB JPEG (85% quality, max 1080p)
- **Savings**: 70-80% reduction in API costs and latency

### Retry Logic
- Automatic retry on network failures
- Exponential backoff (4s, 8s, 16s)
- Prevents session crashes from transient errors

### Conversation History
- Maintains context across actions
- AI remembers previous steps
- More coherent multi-step workflows

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.x |
| AI Model | OpenAI GPT-4o Vision |
| Screen Capture | mss, PIL |
| Mouse/Keyboard | PyAutoGUI |
| Retry Logic | tenacity |
| Environment | python-dotenv |

## Project Structure

```
hackparv/
├── self-operating-computer/
│   ├── operate/
│   │   ├── main.py              # CLI entry point
│   │   ├── operate.py           # Main orchestration loop
│   │   ├── config.py            # Configuration management
│   │   ├── models/
│   │   │   ├── assistant_adapter.py  # OpenAI integration
│   │   │   ├── apis.py          # Model routing
│   │   │   └── prompts.py       # System prompts
│   │   └── utils/
│   │       ├── operating_system.py   # Action execution
│   │       ├── screenshot.py    # Screen capture
│   │       └── style.py         # Terminal styling
│   └── requirements.txt         # Python dependencies
│
├── examples/                    # Example workflows
├── README.md                    # Main documentation
├── QUICKSTART.md               # Setup guide
├── USAGE_GUIDE.md              # Usage examples
├── test_integration.py         # Integration tests
└── verify_code.py              # Code verification
```

## Comparison: Before vs After

| Aspect | Before (Node.js) | After (Pure Python) |
|--------|------------------|---------------------|
| **Dependencies** | Python + Node.js | Python only |
| **API Calls** | Python → Node.js → OpenAI | Python → OpenAI |
| **Memory** | Stateless (no history) | Full conversation history |
| **Image Size** | ~5-10 MB PNG | ~0.5-1 MB JPEG |
| **Reliability** | No retries | 3 retries with backoff |
| **Safety** | None | Command validation |
| **Setup** | Complex (2 servers) | Simple (1 command) |
| **Debugging** | Multi-language | Single language |

## API Usage

### Cost Estimation
With image compression:
- **Input**: ~1000 tokens per screenshot (vs ~3000 before)
- **Output**: ~200 tokens per response
- **Cost per action**: ~$0.01-0.02 (GPT-4o pricing)

### Rate Limits
- Handled automatically by retry logic
- Exponential backoff prevents API abuse
- Graceful degradation on failures

## Future Enhancements

Potential improvements:
- [ ] Multi-monitor support
- [ ] Windows/Linux compatibility
- [ ] Action recording/replay
- [ ] Cost tracking dashboard
- [ ] Session persistence
- [ ] Web interface
- [ ] Voice control integration
