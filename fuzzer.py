import json
import os
from rich.console import Console
from rich.table import Table

from src.llm_client import LLMClient
from src.evaluator import SecurityEvaluator
from src.guardrails import GuardrailFilter

console = Console()

def run_fuzzer():
    console.print("[bold cyan]=== AUTOMATED PROMPT INJECTION BENCHMARK SUITE ===[/bold cyan]\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "data", "targets.json")) as f:
        targets = json.load(f)
    with open(os.path.join(base_dir, "data", "payloads.json")) as f:
        payloads = json.load(f)

    llm = LLMClient()
    evaluator = SecurityEvaluator()
    guardrail = GuardrailFilter(sensitivity="medium")

    table = Table(title="Security Audit Results")
    table.add_column("Target Level", style="yellow")
    table.add_column("Payload ID", style="cyan")
    table.add_column("Guardrail Filter", style="magenta")
    table.add_column("Exploit Status", style="bold")

    audit_results = []

    for target in targets:
        for payload in payloads:
            prompt_text = payload["prompt"]
            is_blocked, reason, _ = guardrail.inspect_prompt(prompt_text)
            
            if is_blocked:
                status = "[green]BLOCKED BY FILTER[/green]"
                leaked = False
            else:
                response = llm.query_with_history(target["system_prompt"], [{"user": prompt_text, "assistant": ""}], 0)
                leaked = evaluator.is_flag_leaked(target["secret_flag"], response)
                status = "[red]EXPLOITED (FLAG LEAKED)[/red]" if leaked else "[green]DEFENDED BY LLM[/green]"

            table.add_row(
                target["target_name"],
                payload["id"],
                "BLOCKED" if is_blocked else "PASSED",
                status
            )

            audit_results.append({
                "target": target["target_name"],
                "payload_id": payload["id"],
                "filter_blocked": is_blocked,
                "flag_leaked": leaked
            })

    console.print(table)

    # Save report
    with open("audit_report.json", "w") as f:
        json.dump(audit_results, f, indent=2)
    console.print("\n[bold green]✔ Audit report saved to audit_report.json[/bold green]")

if __name__ == "__main__":
    run_fuzzer()
