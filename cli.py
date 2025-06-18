 
from core.llm_interface import query_llm
from rich.console import Console

console = Console()

def main():
    console.print("[bold green]Welcome to Jarvis CLI Assistant[/bold green]")
    console.print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You > ").strip()
            if user_input.lower() in ["exit", "quit"]:
                break

            response = query_llm(user_input)

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    main()