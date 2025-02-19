from typing import List
import asyncio
from services.invoice_service import InvoiceService
from rich.console import Console
from rich.progress import Progress

console = Console()

async def reissue_invoices(invoice_ids: List[str]):
    with Progress() as progress:
        task = progress.add_task("[cyan]Reissuing invoices...", total=len(invoice_ids))
        
        for invoice_id in invoice_ids:
            try:
                await InvoiceService.reissue_invoice(invoice_id)
                console.print(f"[green]Successfully reissued invoice {invoice_id}")
            except Exception as e:
                console.print(f"[red]Error reissuing invoice {invoice_id}: {str(e)}")
            finally:
                progress.advance(task)

async def update_invoices_with_error(invoice_ids: List[str], error_message: str):
    try:
        await InvoiceService.update_invoices_error(invoice_ids, error_message)
        console.print("[green]Successfully updated invoices with error status")
    except Exception as e:
        console.print(f"[red]Error updating invoices: {str(e)}")

async def update_and_reissue_invoices(invoice_ids: List[str], error_message: str, delay: int = 5):
    console.print("[bold cyan]Step 1: Updating invoices with error status[/bold cyan]")
    try:
        await update_invoices_with_error(invoice_ids, error_message)
        console.print(f"[yellow]Waiting {delay} seconds before reissuing...[/yellow]")
        await asyncio.sleep(delay)
        
        console.print("[bold cyan]Step 2: Reissuing invoices[/bold cyan]")
        await reissue_invoices(invoice_ids)
        
        console.print("[bold green]✓ Complete: All operations finished successfully[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Operation failed: {str(e)}[/bold red]")
