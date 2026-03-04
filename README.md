# FRIDAY 🤖

A CLI tool that uses AI to answer questions about your codebase.

## What it does

Point Friday at any codebase and ask questions in plain English:
```bash
python main.py ask "what does this project do?" -p .
python main.py ask "how does the scanner work?" -p .
python main.py ask "what files are in this project?" -p .
```

## Tech Stack

- **Python** — core language
- **Typer** — CLI framework
- **Groq** — free, fast AI API (LLaMA 70B)
- **Rich** — beautiful terminal output

## Setup

1. Clone the repo
```bash
git clone https://github.com/yourusername/friday.git
cd friday
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add your Groq API key
```bash
cp .env.example .env
# edit .env and add your GROQ_API_KEY
# get a free key at https://console.groq.com
```

5. Run it
```bash
python main.py ask "what is this project?"
python main.py ask "explain the AI integration" -p .
```

## Commands

| Command | Description |
|---------|-------------|
| `ask "question"` | Ask a general coding question |
| `ask "question" -p .` | Ask a question about your codebase |
| `scan .` | Scan and list all code files in a directory |

## How it works

1. Scans your codebase for code files
2. Reads file contents up to a safe context limit
3. Sends your question + code context to Groq's LLaMA model
4. Returns a clear, concise answer