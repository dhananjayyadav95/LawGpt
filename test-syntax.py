#!/usr/bin/env python3
"""
Quick syntax check for server.py
"""

import sys
import ast

def check_syntax():
    """Check if server.py has valid Python syntax"""
    try:
        with open('backend/server.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Try to parse the code
        ast.parse(code)
        print("✅ server.py syntax is valid!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error in server.py:")
        print(f"   Line {e.lineno}: {e.text}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error checking syntax: {e}")
        return False

if __name__ == "__main__":
    success = check_syntax()
    sys.exit(0 if success else 1)