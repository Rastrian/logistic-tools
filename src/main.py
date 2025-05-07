import typer
from typing import List
import asyncio
from commands.invoice_commands import reissue_invoices, update_invoices_with_error, update_and_reissue_invoices, deny_invoices, finish_sales_order, issue_sales_order_invoice, finish_and_issue_invoice, check_pending_invoices
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from commands.tanaporta_commands import cancel_tanaporta_order

app = typer.Typer()
console = Console()

def show_menu():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")
    table.add_row("reissue <invoice_ids...>", "Reissue one or more invoices")
    table.add_row("error <invoice_ids...>", "Update invoices with error status")
    table.add_row("update-and-reissue <invoice_ids...>", "Update and reissue invoices")
    table.add_row("deny <invoice_ids...>", "Change invoice status to denied")
    table.add_row("finish <sales_order_id>", "Change sales order status to finish")
    table.add_row("issue-invoice <sales_order_id>", "Issue invoice for a sales order")
    table.add_row("finish-and-issue <sales_order_id>", "Finish sales order and issue invoice")
    table.add_row("check-pending <invoice_ids...>", "Check pending status of invoices")
    table.add_row("cancel-tanaporta <order_id>", "Cancel Tanaporta order")
    table.add_row("help", "Show this help message")
    table.add_row("exit", "Exit the application")
    console.print(table)

def interactive_mode():
    console.print("[bold blue]Welcome to Invoice Management Tool v1.0[/bold blue]")
    console.print("[yellow]Type 'help' to see available commands or 'exit' to quit[/yellow]\n")
    
    while True:
        try:
            command = Prompt.ask("[bold green]invoice-tool>[/bold green]").strip()
            
            if command.lower() == 'exit':
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif command.lower() == 'help':
                show_menu()
                continue
            
            # Parse the command
            parts = command.split()
            if not parts:
                continue
                
            cmd, *args = parts
            
            if cmd == 'reissue':
                if not args:
                    console.print("[red]Error: Please provide invoice IDs[/red]")
                    continue
                asyncio.run(reissue_invoices(args))
                
            elif cmd == 'error':
                if not args:
                    console.print("[red]Error: Please provide invoice IDs[/red]")
                    continue
                message = Prompt.ask("Error message", default="Fail to process order on SAP: Invoice retry stuck")
                asyncio.run(update_invoices_with_error(args, message))
                
            elif cmd == 'update-and-reissue':
                if not args:
                    console.print("[red]Error: Please provide invoice IDs[/red]")
                    continue
                message = Prompt.ask("Error message", default="Fail to process order on SAP: Invoice retry stuck")
                delay = int(Prompt.ask("Delay (seconds)", default="15"))
                asyncio.run(update_and_reissue_invoices(args, message, delay))
                
            elif cmd == 'deny':
                if not args:
                    console.print("[red]Error: Please provide invoice IDs[/red]")
                    continue
                asyncio.run(deny_invoices(args))
                
            elif cmd == 'finish':
                if not args:
                    console.print("[red]Error: Please provide a sales order ID[/red]")
                    continue
                asyncio.run(finish_sales_order(args[0]))
                
            elif cmd == 'issue-invoice':
                if not args:
                    console.print("[red]Error: Please provide a sales order ID[/red]")
                    continue
                asyncio.run(issue_sales_order_invoice(args[0]))
                
            elif cmd == 'finish-and-issue':
                if not args:
                    console.print("[red]Error: Please provide a sales order ID[/red]")
                    continue
                delay = int(Prompt.ask("Delay (seconds)", default="15"))
                asyncio.run(finish_and_issue_invoice(args[0], delay))
                
            elif cmd == 'check-pending':
                if not args:
                    console.print("[red]Error: Please provide invoice IDs[/red]")
                    continue
                asyncio.run(check_pending_invoices(args))
                
            elif cmd == 'cancel-tanaporta':
                if not args:
                    console.print("[red]Error: Please provide an order ID[/red]")
                    continue
                asyncio.run(cancel_tanaporta_order(args[0]))
                
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
                console.print("[yellow]Type 'help' to see available commands[/yellow]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' command to quit[/yellow]")
            continue
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    interactive_mode()
