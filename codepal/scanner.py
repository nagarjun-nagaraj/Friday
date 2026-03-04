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

MAX_CONTEXT_CHARS = 8000

def read_files(files: list[str]) -> tuple[str, int, int]:
    """Read contents of files up to a character limit."""
    context = ""
    included = 0
    skipped = 0

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                chunk = f"\n\n--- File: {file_path} ---\n{content}"

                if len(context) + len(chunk) > MAX_CONTEXT_CHARS:
                    skipped += 1
                    continue

                context += chunk
                included += 1

        except Exception as e:
            context += f"\n\n--- File: {file_path} --- (could not read: {e})"
            skipped += 1

    return context, included, skipped