from pynput import keyboard
from datetime import datetime
import argparse
import os
import sys

def readable_key(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            return key.char
        else:
            return f'[{key.name}]'
    except Exception:
        return f'[{str(key)}]'

def main(output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    try:
        logfile = open(output_path, 'a', encoding='utf-8')
    except Exception as e:
        print(f"Failed to open log file: {e}")
        sys.exit(1)
    print(f"Recording keys to: {output_path}")
    print("Press ESC to stop.")

    def on_press(key):
        s = readable_key(key)
        s = s.replace('\n', '\\n').replace('\r', '\\r')
        timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
        logfile.write(f"{timestamp}\t{s}\n")
        logfile.flush()

    def on_release(key):
        if key == keyboard.Key.esc:
            print("ESC pressed — stopping.")
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    logfile.close()
    print("Stopped. Log saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transparent keystroke recorder for personal use.")
    parser.add_argument(
        "-o", "--output",
        default="keystrokes_log.txt"
    )
    args = parser.parse_args()
    main(args.output)
