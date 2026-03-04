import os

IGNORED = {"venv", "__pycache__","git","node_modules", ".env"}

def get_files(path: str) -> list[str]:
    """Walk through a folder and return all code files."""
    files = []

    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORED]

        for filename in filenames:
            if filename.endswith((".py",".js",".ts",".html",".css")):
                full_path = os.path.join(root, filename)
                files.append(full_path)

    return files

