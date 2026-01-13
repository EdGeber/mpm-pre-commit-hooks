import io
import sys
import argparse
from typing import Sequence, Dict

import os

def reset_yaml_defaults(file_path: str) -> int:
    """
    Reads a file, replaces 'currentValue' and 'newValue' blocks with the 
    'defaultValue' block structure, and saves the result.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    target_keys = ["defaultValue", "currentValue", "newValue", "raiseIfEqual"]
    indices: Dict[str, int] = {}

    for i, line in enumerate(lines):
        stripped = line.strip()
        for key in target_keys:
            if stripped.startswith(key):
                indices[key] = i
                break
    
    if len(indices) < 4:
        return 0

    idx_default = indices["defaultValue"]
    idx_current = indices["currentValue"]
    idx_new = indices["newValue"]
    idx_raise = indices["raiseIfEqual"]

    if not (idx_default < idx_current < idx_new < idx_raise):
        return 0

    part_a = lines[:idx_default]
    
    block_default = lines[idx_default:idx_current]
    block_current = lines[idx_current:idx_new]
    block_new = lines[idx_new:idx_raise]
    
    part_e = lines[idx_raise:]
    
    content_default = '\n'.join(block_default)
    content_current = '\n'.join(block_current)
    content_new = '\n'.join(block_new)
    
    if (
        content_default == content_current.replace("currentValue", "defaultValue", 1) and 
        content_default == content_new.replace("newValue", "defaultValue", 1)
    ):
        return 0
    
    if "&id" in block_default[0]:
        i = block_default.index('&')
        block_default[0] = block_default[0][:i]
    
    block_current = block_default.copy()
    block_current[0] = block_current[0].replace("defaultValue", "currentValue", 1)

    block_new = block_default.copy()
    block_new[0] = block_new[0].replace("defaultValue", "newValue", 1)

    new_content = part_a + block_default + block_current + block_new + part_e

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content)

    return 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args(argv)
    
    verbose: bool = args.verbose

    retval = 0
    
    for filename in args.filenames:
        try:
            retval |= reset_yaml_defaults(filename)
        except Exception as e:
            if verbose:
                print(f"Error processing {filename}: {e}")

    return retval

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
