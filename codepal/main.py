import json
import typer
from pathlib import Path
from rich import print
from rich.table import Table
from rich.console import Console
from codepal import scanner, ai

app = typer.Typer()

HISTORY_FILE = Path.home() / ".friday_history.json"

AVAILABLE_MODELS = [
    {"id": "llama-3.3-70b-versatile",  "description": "Default — best all-rounder"},
    {"id": "llama-3.1-8b-instant",     "description": "Fast and lightweight"},
    {"id": "qwen-qwq-32b",             "description": "Reasoning — great for code"},
    {"id": "llama3-8b-8192",           "description": "Stable, widely tested"},
]


DEFAULT_MODEL = ai.DEFAULT_MODEL


def load_history() -> list:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history: list):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


@app.command()
def ask(
    question: str,
    path: str = typer.Option(None, "--path", "-p", help="Path to codebase to scan"),
    model: str = typer.Option(DEFAULT_MODEL, "--model", "-m", help="Groq model to use")
):
    """Ask a question about your codebase."""
    print(f"[bold green]You asked:[/bold green] {question}")
    print(f"[dim]Model: {model}[/dim]")

    context = ""
    if path:
        print(f"[yellow]Scanning {path} for context...[/yellow]")
        files = scanner.get_files(path)
        if files:
            context, included, skipped = scanner.read_files(files)
            print(f"[yellow]Reading {included} files as context...[/yellow]")
            if skipped > 0:
                print(f"[red]Skipped {skipped} files (context limit reached)[/red]")
        else:
            print(f"[red]No code files found in {path}[/red]")

    history = load_history()
    print(f"[yellow]Thinking...[/yellow]")
    answer, updated_history = ai.ask_ai(question, context, history, model)
    save_history(updated_history)

    print(f"\n[bold white]Answer:[/bold white] {answer}")


@app.command()
def models():
    """List available Groq models."""
    console = Console()
    table = Table(title="Available Models", show_header=True, header_style="bold cyan")
    table.add_column("Model ID", style="green")
    table.add_column("Description")

    for m in AVAILABLE_MODELS:
        model_id = m["id"]
        if model_id == DEFAULT_MODEL:
            model_id += " [bold yellow](default)[/bold yellow]"
        table.add_row(model_id, m["description"])

    console.print(table)
    console.print("\n[dim]Usage: friday ask \"your question\" --model <model-id>[/dim]")


@app.command()
def history():
    """Show chat history."""
    chat_history = load_history()
    if not chat_history:
        print("[yellow]No history yet. Ask something first![/yellow]")
        return

    for message in chat_history:
        if message["role"] == "user":
            print(f"\n[bold green]You:[/bold green] {message['content']}")
        else:
            print(f"[bold white]Friday:[/bold white] {message['content']}")


@app.command()
def clear():
    """Clear chat history."""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
        print("[bold red]History cleared.[/bold red]")
    else:
        print("[yellow]No history to clear.[/yellow]")


@app.command()
def scan(path: str = typer.Argument(".", help="Path to scan")):
    """Scan a folder and show files found."""
    files = scanner.get_files(path)
    print(f"[bold blue]Found {len(files)} files in {path}:[/bold blue]")
    for file in files:
        print(f" [green]{file}[/green]")


if __name__ == "__main__":
    app()