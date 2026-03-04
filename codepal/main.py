import typer
from rich import print
from codepal import scanner, ai

app = typer.Typer()

@app.command()
def ask(question:str):
    """Ask a question about your codebase."""
    print(f"[bold green]You asked:[/bold green] {question}")
    print(f"[yellow]Thinking...[/yellow]")
    answer = ai.ask_ai(question)
    print(f"[bold white]Answer:[/bold white] {answer}")

@app.command()
def scan(path: str = typer.Argument(".", help="Path to scan")):
    """Scan a folder and show files found."""
    files = scanner.get_files(path)
    print(f"[bold blue]Found {len(files)} files in {path}:[/bold blue]")
    for file in files:
        print(f" [green]{file}[/green]")

if __name__ == "__main__":
    app()
