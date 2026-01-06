# AI Agent Systems: Industrial-Grade Documentation

A comprehensive repository containing two production-ready AI agent systems: a **real-time conversational assistant** (Assistant-main) and a **self-operating computer automation framework** (Jarvis). This documentation provides complete setup, usage, and integration guidelines for both systems.

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Assistant-main Setup](#assistant-main-setup)
  - [Jarvis Setup](#jarvis-setup)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Assistant-main Usage](#assistant-main-usage)
  - [Jarvis Usage](#jarvis-usage)
- [Technical Deep Dive](#technical-deep-dive)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Integration Guide](#integration-guide)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

### Assistant-main: Real-Time Conversational AI

**Type**: Web-based conversational AI assistant  
**Tech Stack**: Node.js + Next.js + WebSocket  
**Purpose**: Real-time voice/text chat with AI using OpenAI's Realtime API  
**Interaction**: Browser-based UI, talks to users  
**Capabilities**: Conversational responses, audio streaming, report explanations

### Jarvis: Self-Operating Computer

**Type**: Desktop automation agent  
**Tech Stack**: Python + Vision AI + OS Control  
**Purpose**: Autonomous computer control using GPT-4 Vision  
**Interaction**: CLI commands, operates your Mac directly  
**Capabilities**: Screen understanding, mouse/keyboard control, multi-step workflows

---

## System Architecture

### Assistant-main Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │◄───────►│  Node Server │◄───────►│   OpenAI    │
│  (Next.js)  │ WebSocket│  (index.js)  │ WebSocket│  Realtime   │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              │ Audio Processing
                              ▼
                        ┌──────────────┐
                        │ audiofunctions│
                        │    .js       │
                        └──────────────┘
```

**Flow**:
1. Browser connects to WebSocket server (`ws://localhost:4000/Assistant`)
2. Server creates connection to OpenAI Realtime API
3. Messages relayed bidirectionally with audio conversion
4. Real-time audio streaming (PCM → WAV conversion)

### Jarvis Architecture

```
┌─────────────┐
│   User CLI  │
│  (operate)  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Control Loop   │
│  (operate.py)   │
└──────┬──────────┘
       │
       ├──► Screenshot Capture
       ├──► Vision AI (GPT-4/Claude/Gemini)
       ├──► Operation Generation
       └──► OS Execution (mouse/keyboard)
```

**Flow**:
1. User provides objective via CLI
2. System captures screenshot
3. Vision AI analyzes screen + history
4. AI generates operations (click/press/write/done)
5. Operations executed on macOS
6. Loop repeats until objective complete

---

## Prerequisites

### Assistant-main Requirements

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **OpenAI API Key**: Valid API key with Realtime API access
- **Operating System**: macOS, Linux, or Windows

### Jarvis Requirements

- **Python**: 3.9 or higher
- **macOS**: Required (uses macOS Accessibility APIs)
- **API Keys**: At least one of the following:
  - OpenAI API key (for GPT-4 Vision/Assistants)
  - Google API key (for Gemini Vision)
  - Anthropic API key (for Claude 3)
  - Qwen API key (for Qwen Vision)
  - Ollama (local installation, optional)
- **System Permissions**:
  - Screen Recording permission
  - Accessibility permission

---

## Installation

### Assistant-main Setup

#### Step 1: Clone and Navigate

```bash
cd Assistant-main
```

#### Step 2: Install Server Dependencies

```bash
cd server
npm install
```

#### Step 3: Install Client Dependencies

```bash
cd ../client
npm install
```

#### Step 4: Configure Environment

Create a `.env` file in the `server/` directory:

```bash
cd ../server
touch .env
```

Add your OpenAI API key:

```env
KEY=your_openai_api_key_here
```

#### Step 5: Verify Installation

```bash
# Test server
node index.js
# Should see: "WebSocket server is listening on ws://localhost:4000/Assistant"
```

### Jarvis Setup

#### Step 1: Navigate to Jarvis Directory

```bash
cd jarvis-tweak-version-/hackparv/self-operating-computer
```

#### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

For voice mode (optional):

```bash
pip install -r requirements-audio.txt
```

#### Step 4: Configure Environment

Create a `.env` file in the `self-operating-computer/` directory:

```bash
touch .env
```

Add your API keys (at least one required):

```env
# OpenAI (for GPT-4 Vision/Assistants)
OPENAI_API_KEY=your_openai_key_here

# Google (for Gemini Vision, optional)
GOOGLE_API_KEY=your_google_key_here

# Anthropic (for Claude 3, optional)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Qwen (optional)
QWEN_API_KEY=your_qwen_key_here

# Ollama (optional, for local models)
OLLAMA_HOST=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llava:7b
```

#### Step 5: Grant macOS Permissions

1. Open **System Settings** → **Privacy & Security**
2. Add **Terminal** (or your terminal app) to:
   - **Screen Recording**
   - **Accessibility**

#### Step 6: Verify Installation

```bash
# Test with a simple command
operate --model=assistant --prompt="open Safari" --verbose
```

---

## Configuration

### Assistant-main Configuration

**Environment Variables** (`server/.env`):

| Variable | Description | Required |
|----------|-------------|----------|
| `KEY` | OpenAI API key | Yes |

**Server Configuration** (`server/index.js`):

- **Port**: Default `4000` (modify in `server.listen()`)
- **WebSocket Path**: `/Assistant` (modify in `server.on("upgrade")`)
- **Model**: `gpt-4o-realtime-preview-2024-10-01` (hardcoded, modify in WebSocket URL)

**Client Configuration** (`client/`):

- Modify `src/pages/index.js` to customize UI
- Update `next.config.mjs` for Next.js settings

### Jarvis Configuration

**Environment Variables** (`.env`):

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | For OpenAI models |
| `GOOGLE_API_KEY` | Google API key | For Gemini models |
| `ANTHROPIC_API_KEY` | Anthropic API key | For Claude models |
| `QWEN_API_KEY` | Qwen API key | For Qwen models |
| `OLLAMA_HOST` | Ollama server URL | For Ollama models |
| `OLLAMA_DEFAULT_MODEL` | Default Ollama model | Optional |

**Model Selection**:

Available models:
- `assistant` - OpenAI Assistants API (recommended)
- `gpt-4-with-ocr` - GPT-4 with OCR
- `gpt-4.1-with-ocr` - GPT-4.1 with OCR
- `gemini-pro-vision` - Google Gemini Vision
- `claude-3` - Anthropic Claude 3
- `qwen-vl` - Qwen Vision Language
- `ollama:model:name` - Local Ollama models

**Configuration Class** (`operate/config.py`):

The `Config` class automatically:
- Loads environment variables
- Validates required keys per model
- Prompts for missing keys via GUI dialog
- Saves keys to `.env` file

---

## Usage

### Assistant-main Usage

#### Starting the Server

```bash
cd Assistant-main/server
node index.js
```

Expected output:
```
WebSocket server is listening on ws://localhost:4000/Assistant
```

#### Starting the Client

In a new terminal:

```bash
cd Assistant-main/client
npm run dev
```

Open `http://localhost:3000` in your browser.

#### WebSocket Connection

Connect from your frontend:

```javascript
const ws = new WebSocket('ws://localhost:4000/Assistant');

ws.onopen = () => {
  console.log('Connected to assistant server');
  // Send session start event
  ws.send(JSON.stringify({
    type: 'session.update',
    session: {
      modalities: ['text', 'audio'],
      instructions: 'You are a helpful assistant.'
    }
  }));
};

ws.onmessage = (event) => {
  if (event.data instanceof Blob) {
    // Audio data (WAV format)
    const audioUrl = URL.createObjectURL(event.data);
    const audio = new Audio(audioUrl);
    audio.play();
  } else {
    // JSON event
    const data = JSON.parse(event.data);
    console.log('Received:', data);
  }
};
```

### Jarvis Usage

#### Basic Command

```bash
operate --model=assistant --prompt="open Safari"
```

#### Interactive Mode

```bash
operate --model=assistant
# Will prompt for objective
```

#### Voice Mode

```bash
operate --model=assistant --voice
# Will listen from microphone
```

#### Verbose Mode (Debugging)

```bash
operate --model=assistant --prompt="open Safari" --verbose
```

#### Using Different Models

```bash
# OpenAI Assistant (recommended)
operate --model=assistant --prompt="open Safari"

# Gemini Vision
operate --model=gemini-pro-vision --prompt="open Safari"

# Claude 3
operate --model=claude-3 --prompt="open Safari"

# Ollama (local)
operate --model=ollama:llava:7b --prompt="open Safari"
```

#### Ollama Model Management

```bash
# List available Ollama models
operate --list-models

# Set default Ollama model
operate --set-default=llava:7b
```

#### Example Workflows

```bash
# Open application
operate --model=assistant --prompt="open Safari and navigate to apple.com"

# File management
operate --model=assistant --prompt="create a folder called 'reports' on Desktop"

# Development tasks
operate --model=assistant --prompt="open VS Code and create a new file called test.js"

# Multi-step workflow
operate --model=assistant --prompt="open Chrome, search for 'Python tutorials', and open the first result"
```

---

## Technical Deep Dive

### Assistant-main: How It Works

#### 1. Server Initialization

The server creates two WebSocket connections:
- **Client WebSocket**: Browser ↔ Server
- **OpenAI WebSocket**: Server ↔ OpenAI Realtime API

```javascript
// Server setup
const wss = new WebSocket.Server({ noServer: true });
const gptClient = new WebSocket(openaiUrl, {
  headers: {
    Authorization: `Bearer ${gptKey}`,
    "OpenAI-Beta": "realtime=v1"
  }
});
```

#### 2. Message Queue System

Messages from the browser are queued until OpenAI connection is ready:

```javascript
const messageQueue = [];
let gptClientReady = false;

// Queue messages if not ready
if (!gptClientReady) {
  messageQueue.push(JSON.stringify(event));
}
```

#### 3. Audio Processing

Audio chunks from OpenAI are converted from PCM to WAV:

```javascript
if (parsedData.type === "response.audio.delta") {
  const pcmData = helper.base64ToArrayBuffer(parsedData.delta);
  const header = helper.createWavHeader(24000, pcmData.byteLength);
  const finalAudioBuffer = helper.concatenateWavHeaderAndData(header, pcmData);
  ws.send(finalAudioBuffer);
}
```

### Jarvis: How It Works

#### 1. Command-Line Entry (`operate/main.py`)

Parses arguments and routes to main control loop:

```python
parser.add_argument("-m", "--model", help="Model to use")
parser.add_argument("--prompt", help="Direct objective")
parser.add_argument("--voice", help="Voice input mode")
parser.add_argument("--verbose", help="Verbose logging")
```

#### 2. Control Loop (`operate/operate.py`)

The main loop follows this pattern:

```python
while True:
    # 1. Get next action from AI
    operations, session_id = asyncio.run(
        get_next_action(model, messages, objective, session_id)
    )
    
    # 2. Execute operations
    stop = operate(operations, model)
    
    # 3. Check if done
    if stop:
        break
```

#### 3. Operation Execution

Operations are executed via `OperatingSystem` class:

- **Click**: `operating_system.mouse({"x": x, "y": y})`
- **Press**: `operating_system.press(["cmd", "space"])`
- **Write**: `operating_system.write("text content")`
- **Done**: Returns `True` to stop loop

#### 4. Vision AI Integration

Screenshot → Encode → Send to Vision Model → Parse Operations:

```python
# Capture screenshot
screenshot = capture_screen()

# Send to AI with history
response = vision_model.analyze(
    image=screenshot,
    history=messages,
    objective=objective
)

# Parse operations
operations = parse_operations(response)
```

---

## API Reference

### Assistant-main WebSocket API

**Endpoint**: `ws://localhost:4000/Assistant`

**Connection**:
```javascript
const ws = new WebSocket('ws://localhost:4000/Assistant');
```

**Events Sent to Server**:

```javascript
// Start session
{
  type: 'session.update',
  session: {
    modalities: ['text', 'audio'],
    instructions: 'You are a helpful assistant.'
  }
}

// Send user input
{
  type: 'input_audio_buffer.append',
  audio: base64EncodedAudio
}

// Or text input
{
  type: 'conversation.item.create',
  item: {
    type: 'message',
    role: 'user',
    content: [{ type: 'input_text', text: 'Hello' }]
  }
}
```

**Events Received from Server**:

```javascript
// Audio response
Blob (WAV format) - Play directly in Audio element

// Text/JSON response
{
  type: 'response.audio_transcript.done',
  transcript: 'Hello, how can I help you?'
}
```

### Jarvis CLI API

**Command Structure**:
```bash
operate [OPTIONS]
```

**Options**:

| Option | Description | Example |
|--------|-------------|---------|
| `-m, --model` | AI model to use | `--model=assistant` |
| `--prompt` | Direct objective | `--prompt="open Safari"` |
| `--voice` | Voice input mode | `--voice` |
| `--verbose` | Verbose logging | `--verbose` |
| `--list-models` | List Ollama models | `--list-models` |
| `--set-default` | Set default Ollama model | `--set-default=llava:7b` |

**Operation Types** (returned by AI):

```json
{
  "operation": "click",
  "x": 123,
  "y": 456,
  "thought": "Clicking Safari icon"
}

{
  "operation": "press",
  "keys": ["cmd", "space"],
  "thought": "Opening Spotlight"
}

{
  "operation": "write",
  "content": "Hello World",
  "thought": "Typing text"
}

{
  "operation": "done",
  "summary": "Task completed successfully"
}
```

---

## Troubleshooting

### Assistant-main Issues

#### Server Won't Start

**Problem**: Port 4000 already in use

**Solution**:
```bash
# Find process using port 4000
lsof -i :4000

# Kill process or change port in index.js
server.listen(3001, ...)  # Use different port
```

#### WebSocket Connection Fails

**Problem**: Connection refused or timeout

**Solutions**:
1. Verify server is running: `node index.js`
2. Check firewall settings
3. Verify OpenAI API key in `.env`
4. Check network connectivity

#### Audio Not Playing

**Problem**: Audio chunks received but no sound

**Solutions**:
1. Verify browser audio permissions
2. Check WebSocket message type (should be Blob for audio)
3. Verify audio format (should be WAV)
4. Check browser console for errors

### Jarvis Issues

#### Permission Denied Errors

**Problem**: "Permission denied" when trying to control system

**Solution**:
1. Grant Screen Recording permission:
   - System Settings → Privacy & Security → Screen Recording
   - Add Terminal (or your terminal app)
2. Grant Accessibility permission:
   - System Settings → Privacy & Security → Accessibility
   - Add Terminal (or your terminal app)
3. Restart terminal after granting permissions

#### Model Not Recognized

**Problem**: `ModelNotRecognizedException`

**Solution**:
1. Verify model name spelling
2. Check if API key is set for that model
3. For Ollama: verify Ollama is running (`ollama serve`)
4. List available models: `operate --list-models`

#### API Key Not Found

**Problem**: Prompted for API key repeatedly

**Solution**:
1. Verify `.env` file exists in `self-operating-computer/` directory
2. Check `.env` file format: `OPENAI_API_KEY=your_key_here`
3. Ensure no extra spaces or quotes
4. Restart terminal after adding keys

#### Screenshot Capture Fails

**Problem**: Cannot capture screen

**Solution**:
1. Verify Screen Recording permission (see above)
2. Check if running in headless mode (not supported)
3. Verify display is available
4. Try with `--verbose` for detailed error messages

#### Operations Not Executing

**Problem**: AI returns operations but nothing happens

**Solution**:
1. Check Accessibility permission (see above)
2. Verify `OperatingSystem` class is working
3. Run with `--verbose` to see operation details
4. Check if operations are being blocked by system

---

## Security Considerations

### Assistant-main Security

1. **API Key Protection**:
   - Never commit `.env` files to version control
   - Use environment variables in production
   - Rotate API keys regularly

2. **WebSocket Security**:
   - Add authentication for production use
   - Use WSS (WebSocket Secure) in production
   - Implement rate limiting

3. **Input Validation**:
   - Validate all WebSocket messages
   - Sanitize user input
   - Implement message size limits

### Jarvis Security

1. **Dangerous Command Blocking**:
   - System automatically blocks: `rm -rf`, `mkfs`, `dd`, fork bombs
   - Validation layer prevents destructive operations
   - Warnings shown before risky actions

2. **API Key Management**:
   - Store keys in `.env` (gitignored)
   - Use separate keys for development/production
   - Never log API keys

3. **System Access**:
   - Only grants minimal required permissions
   - Screen Recording + Accessibility only
   - No root/admin access required

4. **Network Security**:
   - All API calls use HTTPS
   - Screenshots processed locally before sending
   - No persistent data storage

---

## Performance Optimization

### Assistant-main Optimization

1. **Audio Streaming**:
   - Current: Real-time WAV conversion
   - Optimization: Consider Web Audio API for better performance
   - Buffer management for smooth playback

2. **WebSocket Management**:
   - Connection pooling for multiple clients
   - Message batching for high-frequency events
   - Connection timeout handling

3. **Frontend Optimization**:
   - Code splitting in Next.js
   - Lazy loading for audio components
   - Efficient state management

### Jarvis Optimization

1. **Screenshot Compression**:
   - Automatic: Resize to 1920×1080, JPEG 85%
   - **70-80% reduction** in token usage
   - Faster API response times

2. **Retry Logic**:
   - Exponential backoff: 4s → 8s → 16s
   - Up to 3 retry attempts
   - Network resilience

3. **Cost Control**:
   - Screenshot optimization reduces API costs
   - Conversation history management
   - Model selection based on task complexity

4. **Loop Management**:
   - Maximum 10 iterations per session
   - Early termination on "done" operation
   - Session ID reuse for context

---

## Integration Guide

### Combining Assistant-main and Jarvis

#### Architecture

```
┌─────────────┐
│   Browser   │
│ (Assistant) │
└──────┬──────┘
       │
       ▼
┌─────────────┐         ┌─────────────┐
│ Node Server │────────►│   Jarvis    │
│ (Bridge)    │  HTTP   │   (Python)  │
└─────────────┘         └─────────────┘
```

#### Implementation Example

**1. Add Jarvis API Endpoint to Assistant Server**

```javascript
// In server/index.js
const { exec } = require('child_process');

// Add HTTP endpoint for Jarvis commands
server.on('request', (req, res) => {
  if (req.url === '/api/jarvis' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      const { prompt, model } = JSON.parse(body);
      
      // Execute Jarvis command
      exec(`operate --model=${model} --prompt="${prompt}"`, (error, stdout, stderr) => {
        if (error) {
          res.writeHead(500);
          res.end(JSON.stringify({ error: error.message }));
          return;
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ output: stdout }));
      });
    });
  }
});
```

**2. Call from Frontend**

```javascript
// In client
async function executeJarvisCommand(prompt) {
  const response = await fetch('http://localhost:4000/api/jarvis', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: prompt,
      model: 'assistant'
    })
  });
  return await response.json();
}

// Usage
ws.onmessage = async (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'response.text.done' && data.text.includes('open')) {
    // User wants to open something - use Jarvis
    const result = await executeJarvisCommand(data.text);
    console.log('Jarvis result:', result);
  }
};
```

### Industrial Data Integration

#### Adding Data File Support to Assistant-main

**1. Create Data Directory**

```bash
mkdir Assistant-main/server/data
```

**2. Add Data Endpoint**

```javascript
// In server/index.js
const fs = require('fs');
const path = require('path');

server.on('request', (req, res) => {
  if (req.url === '/api/data' && req.method === 'GET') {
    const dataPath = path.join(__dirname, 'data', 'industrial_measures.json');
    const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  }
});
```

**3. Data File Format** (`data/industrial_measures.json`)

```json
{
  "metrics": [
    {
      "name": "Temperature",
      "value": 75.5,
      "unit": "°C",
      "equation": "T = (R - R0) / (α * R0)",
      "description": "Temperature calculation using resistance"
    }
  ]
}
```

**4. Frontend Integration**

```javascript
// Fetch and display data
async function loadIndustrialData() {
  const response = await fetch('http://localhost:4000/api/data');
  const data = await response.json();
  // Display in UI and let assistant explain
}
```

---

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- **JavaScript**: Follow ESLint configuration
- **Python**: Follow PEP 8 style guide
- **Documentation**: Update README for new features

### Testing

- Test both systems independently
- Test integration scenarios
- Verify security measures
- Check performance impact

---

## License

[Specify your license here - e.g., MIT, Apache 2.0, etc.]

---

## Support

For issues, questions, or contributions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Include system information, error messages, and steps to reproduce

---

## Acknowledgments

- **Assistant-main**: Built on OpenAI Realtime API
- **Jarvis**: Based on [self-operating-computer](https://github.com/OthersideAI/self-operating-computer) framework
- Enhanced with additional features and documentation

---

**Last Updated**: [Current Date]  
**Version**: 1.0.0
