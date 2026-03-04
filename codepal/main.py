import typer
from rich import print
from codepal import scanner, ai

app = typer.Typer()

@app.command()
def ask(
    question: str,
    path: str = typer.Option(None, "--path", "-p", help="Path to codebase to scan")
):
    """Ask a question about your codebase."""
    print(f"[bold green]You asked:[/bold green] {question}")

    context = ""
    if path:
        print(f"[yellow]Scanning {path} for context...[/yellow]")
        files = scanner.get_files(path)
        if files:
            print(f"[yellow]Reading {len(files)} files...[/yellow]")
            context = scanner.read_files(files)
        else:
            print(f"[red]No code files found in {path}[/red]")

    print(f"[yellow]Thinking...[/yellow]")
    answer = ai.ask_ai(question, context)
    print(f"\n[bold white]Answer:[/bold white] {answer}")


@app.command()
def scan(path: str = typer.Argument(".", help="Path to scan")):
    """Scan a folder and show files found."""
    files = scanner.get_files(path)
    print(f"[bold blue]Found {len(files)} files in {path}:[/bold blue]")
    for file in files:
        print(f" [green]{file}[/green]")

if __name__ == "__main__":
    app()
