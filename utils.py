import os
import sys

def read_code(source):
    """
    Read code from path or treat as pasted code.
    """
    if os.path.exists(source):
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()
    return source

def write_code(path, code):
    """
    Write fixed code to path (if provided).
    """
    if path:
        dir_path = os.path.dirname(path) or '.'
        os.makedirs(dir_path, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
        return f'Fixed code written to {path}'
    return 'Fixed code generated (no path provided for write).'

