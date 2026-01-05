# Quick Start Guide

Get up and running with the Self-Operating Computer + Assistant integration in 5 minutes!

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 min)

```bash
# Terminal 1: Install Python dependencies
cd self-operating-computer
pip install -r requirements.txt

# Terminal 2: Install Node.js dependencies
cd jarvis/server
npm install
```

### Step 2: Configure API Key (1 min)

```bash
# In jarvis/server directory
cp config.example .env
nano .env  # Add your OpenAI API key
```

Add this line (replace with your actual key):
```
KEY=sk-proj-your-openai-api-key-here
```

Save and exit (Ctrl+X, then Y, then Enter in nano).

### Step 3: Grant Permissions (1 min)

1. Open **System Settings** → **Privacy & Security**
2. Add **Terminal** to:
   - **Screen Recording**
   - **Accessibility**
3. Restart Terminal

### Step 4: Start Servers (30 sec)

```bash
# From project root
chmod +x start_assistant.sh
./start_assistant.sh
```

### Step 5: Test It! (30 sec)

Open a **new terminal**:

```bash
cd self-operating-computer
operate --model=assistant --prompt="open Safari"
```

## ✅ Verification

If everything works, you should see:
1. A screenshot being captured
2. API communication messages
3. Safari opening automatically
4. Success message

## 🎯 Next Commands to Try

```bash
# Open apps
operate --model=assistant --prompt="open VS Code"

# Browse web
operate --model=assistant --prompt="open google.com"

# Search
operate --model=assistant --prompt="search Google for Python tutorials"
```

## 🆘 Troubleshooting

**Problem**: Can't connect to API
```bash
# Check if servers are running
curl http://localhost:4001/health
# If not, run: ./start_assistant.sh
```

**Problem**: Permission denied
```
# Re-check System Settings → Privacy & Security
# Make sure Terminal has both permissions
```

**Problem**: Import errors
```bash
# Reinstall dependencies
cd self-operating-computer
pip install -r requirements.txt
```

## 📖 Full Documentation

- **Complete Setup**: See `INTEGRATION_README.md`
- **Usage Examples**: See `USAGE_GUIDE.md`
- **Troubleshooting**: Run `python3 test_integration.py`

---

**That's it!** You're ready to use AI-powered computer control! 🚀




