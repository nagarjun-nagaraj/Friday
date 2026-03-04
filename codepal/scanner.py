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

def read_files(files: list[str]) -> str:
    """Read contents of files and return as a single context string."""
    context = ""

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                context = f.read()
                context += f"\n\n--- File: {file_path} ---\n{context}"
        except Exception as e:
            context += f"\n\n--- File:{file_path} --- (could not read: {e}"

    return context

