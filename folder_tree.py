import os

EXCLUDED = {'.venv', '.git'}  # Add more folder names here to exclude

def print_tree(root, prefix=""):
    for item in sorted(os.listdir(root)):
        if item in EXCLUDED:
            continue
        path = os.path.join(root, item)
        if os.path.isdir(path):
            print(f"{prefix}├── {item}")
            print_tree(path, prefix + "│   ")

print_tree(".")
