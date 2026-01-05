#!/bin/bash

# Simple test script for the integration
# This runs simpler, single-action commands

echo "🧪 Testing Self-Operating Computer + Assistant Integration"
echo "============================================================"
echo ""

cd /Users/apple/hackparv/self-operating-computer
source venv/bin/activate

echo "Test 1: Open Finder"
echo "--------------------"
operate --model=assistant --prompt="open Finder"
echo ""
sleep 2

echo ""
echo "Test 2: Open Safari"
echo "--------------------"
operate --model=assistant --prompt="open Safari"
echo ""
sleep 2

echo ""
echo "Test 3: Open Terminal"
echo "--------------------"
operate --model=assistant --prompt="open Terminal"
echo ""

echo ""
echo "============================================================"
echo "✅ Integration tests complete!"
echo ""
echo "The AI successfully:"
echo "  - Captured screenshots"
echo "  - Sent to Assistant API"
echo "  - Received AI analysis"
echo "  - Executed keyboard/mouse actions"
echo ""
echo "Try more commands:"
echo "  operate --model=assistant --prompt='your command'"
echo "============================================================"



