#!/usr/bin/env python3
"""
Integration Test Script for Assistant API (Python-Only)
Tests the configuration and dependencies for the self-operating-computer
"""

import sys
import os
import importlib

# Add self-operating-computer to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'self-operating-computer'))

def test_python_dependencies():
    """Test if required Python dependencies are installed"""
    print("\n🔍 Testing Python dependencies...")
    
    required = ["requests", "PIL", "pyautogui", "openai", "dotenv"]
    missing = []
    
    for package in required:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("   Install with: cd self-operating-computer && pip install -r requirements.txt")
        return False
    
    print("✅ All Python dependencies installed")
    return True

def test_openai_configuration():
    """Test if OpenAI API key is configured"""
    print("\n🔍 Testing OpenAI Configuration...")
    
    # Try loading from .env in self-operating-computer
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(__file__), 'self-operating-computer', '.env')
        load_dotenv(env_path)
    except ImportError:
        pass

    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print("✅ OPENAI_API_KEY found in environment")
        return True
    else:
        print("❌ OPENAI_API_KEY not found")
        print("   Please create a .env file in self-operating-computer/ or export the variable")
        return False

def test_adapter_initialization():
    """Test if AssistantAdapter can be initialized"""
    print("\n🔍 Testing AssistantAdapter Initialization...")
    
    try:
        from operate.models.assistant_adapter import AssistantAdapter
        adapter = AssistantAdapter()
        print("✅ AssistantAdapter initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize AssistantAdapter: {e}")
        return False

def test_macos_permissions():
    """Check if running on macOS and provide permission guidance"""
    print("\n🔍 Checking macOS permissions...")
    
    if sys.platform != "darwin":
        print("⚠️  Not running on macOS - skipping permission checks")
        return True
    
    print("⚠️  For self-operating-computer to work on macOS, you need to grant:")
    print("   1. Screen Recording permission")
    print("   2. Accessibility permission")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Self-Operating Computer Integration Test Suite")
    print("=" * 60)
    
    results = {
        "Python Dependencies": test_python_dependencies(),
        "OpenAI Configuration": test_openai_configuration(),
        "Adapter Initialization": test_adapter_initialization(),
        "macOS Permissions": test_macos_permissions(),
    }
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ All tests passed! You're ready to use the integration.")
        print("\nTry running:")
        print("  cd self-operating-computer")
        print("  operate --model=assistant --prompt='open Safari'")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    
    print("=" * 60)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())




