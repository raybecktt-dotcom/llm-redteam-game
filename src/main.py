import json
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from src.llm_client import LLMClient
from src.evaluator import SecurityEvaluator
from src.guardrails import GuardrailFilter

console = Console()

def run_game():
    console.print(Panel.fit("[bold green]PROTOCOL: ROGUE AI[/bold green]\n[dim]LLM Red-Team & Blue-Team Defense Simulator[/dim]"))

    # Ask the user if they want to enable Blue-Team Guardrails
    enable_defense = Confirm.ask("Enable Blue-Team Guardrail Filter (Defense Mode)?", default=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "data", "targets.json"), "r") as f:
        targets = json.load(f)

    llm = LLMClient()
    evaluator = SecurityEvaluator()
    guardrail = GuardrailFilter(sensitivity="medium")

    for target in targets:
        console.print(f"\n[bold yellow]--- LEVEL {target['level']}: {target['target_name']} ---[/bold yellow]")
        console.print(f"[cyan]Role:[/cyan] {target['role']}")
        console.print(f"[dim]Defense Filter: {'[green]ACTIVE[/green]' if enable_defense else '[red]DISABLED[/red]'}[/dim]\n")

        passed = False
        attempts = 0

        while not passed and attempts < 5:
            attempts += 1
            user_input = Prompt.ask(f"[bold white]Prompt ({attempts}/5)[/bold white]")

            # 🛡️ BLUE-TEAM GUARDRAIL CHECK
            if enable_defense:
                is_blocked, reason, meta = guardrail.inspect_prompt(user_input)
                if is_blocked:
                    console.print(f"[bold red]🛡️ BLUE-TEAM FILTER BLOCKED PROMPT![/bold red] Reason: {reason}")
                    console.print(f"[dim]Metadata: {meta}[/dim]\n")
                    continue  # Skip LLM query on block

            # Send to LLM if prompt passes filter
            with console.status("[bold green]Querying AI Guardrails...[/bold green]"):
                response = llm.query(target["system_prompt"], user_input)

            console.print(f"\n[bold magenta]{target['target_name']}:[/bold magenta] {response}\n")

            if evaluator.is_flag_leaked(target["secret_flag"], response):
                console.print(f"[bold green]✔ PROMPT INJECTION SUCCESSFUL![/bold green] Secret flag '{target['secret_flag']}' extracted!")
                passed = True
            else:
                console.print("[bold red]✘ Injection Failed.[/bold red] Target guardrails intact.")

if __name__ == "__main__":
    run_game()
