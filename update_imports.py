#!/usr/bin/env python3
"""Update all imports from airas to tradegraph."""

import os
import re

def update_imports_in_file(filepath):
    """Update imports in a single file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Update imports
        updated = content
        updated = re.sub(r'from airas\.', 'from tradegraph.', updated)
        updated = re.sub(r'import airas\.', 'import tradegraph.', updated)
        updated = re.sub(r'from \.\.\.\.airas', 'from ....tradegraph', updated)
        updated = re.sub(r'from \.\.\.airas', 'from ...tradegraph', updated)
        updated = re.sub(r'from \.\.airas', 'from ..tradegraph', updated)
        updated = re.sub(r'from \.airas', 'from .tradegraph', updated)
        
        if updated != content:
            with open(filepath, 'w') as f:
                f.write(updated)
            print(f"Updated: {filepath}")
            return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
    return False

def main():
    """Update all Python files."""
    updated_count = 0
    
    # Walk through all Python files
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if update_imports_in_file(filepath):
                    updated_count += 1
    
    print(f"\nTotal files updated: {updated_count}")

if __name__ == "__main__":
    main()