#!/usr/bin/env python3
import os
import sys
import json

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    new_path = sys.argv[1]
    config_path = os.path.expanduser("~/.config/tide-island/userconfig.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            config['wallpaperPath'] = new_path
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error updating config: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
