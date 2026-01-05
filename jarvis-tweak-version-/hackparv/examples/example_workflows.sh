#!/bin/bash
# Example Workflows for Self-Operating Computer + Assistant
# Collection of useful automation commands

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "================================================"
echo "🤖 Self-Operating Computer Example Workflows"
echo "================================================"
echo ""
echo "Choose an example to run:"
echo ""
echo "1. Open Applications"
echo "2. Web Browsing"
echo "3. Search Tasks"
echo "4. Development Setup"
echo "5. Productivity"
echo "6. Custom Command"
echo "0. Exit"
echo ""

read -p "Enter your choice (0-6): " choice

case $choice in
  1)
    echo -e "${BLUE}Opening Applications Examples${NC}"
    echo ""
    echo "a. Open Safari"
    echo "b. Open VS Code"
    echo "c. Open Terminal"
    echo ""
    read -p "Choose (a-c): " sub
    case $sub in
      a) operate --model=assistant --prompt="open Safari" ;;
      b) operate --model=assistant --prompt="open VS Code" ;;
      c) operate --model=assistant --prompt="open Terminal" ;;
    esac
    ;;
    
  2)
    echo -e "${BLUE}Web Browsing Examples${NC}"
    echo ""
    echo "a. Open GitHub"
    echo "b. Open Google"
    echo "c. Open YouTube"
    echo ""
    read -p "Choose (a-c): " sub
    case $sub in
      a) operate --model=assistant --prompt="open Safari and go to github.com" ;;
      b) operate --model=assistant --prompt="open Safari and go to google.com" ;;
      c) operate --model=assistant --prompt="open Safari and go to youtube.com" ;;
    esac
    ;;
    
  3)
    echo -e "${BLUE}Search Tasks${NC}"
    read -p "What would you like to search for? " query
    operate --model=assistant --prompt="search Google for ${query}"
    ;;
    
  4)
    echo -e "${BLUE}Development Setup${NC}"
    echo ""
    echo "a. Open VS Code and Terminal"
    echo "b. Open iTerm and navigate to Documents"
    echo "c. Open GitHub in browser"
    echo ""
    read -p "Choose (a-c): " sub
    case $sub in
      a) operate --model=assistant --prompt="open VS Code and Terminal" ;;
      b) operate --model=assistant --prompt="open iTerm and go to Documents folder" ;;
      c) operate --model=assistant --prompt="open Safari and go to github.com" ;;
    esac
    ;;
    
  5)
    echo -e "${BLUE}Productivity Examples${NC}"
    echo ""
    echo "a. Open Notes and create new note"
    echo "b. Open Mail"
    echo "c. Open Calendar"
    echo ""
    read -p "Choose (a-c): " sub
    case $sub in
      a) operate --model=assistant --prompt="open Notes and create a new note" ;;
      b) operate --model=assistant --prompt="open Mail" ;;
      c) operate --model=assistant --prompt="open Calendar" ;;
    esac
    ;;
    
  6)
    echo -e "${BLUE}Custom Command${NC}"
    read -p "Enter your command: " custom
    operate --model=assistant --prompt="${custom}"
    ;;
    
  0)
    echo "Goodbye!"
    exit 0
    ;;
    
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac

echo ""
echo -e "${GREEN}✅ Workflow completed!${NC}"




