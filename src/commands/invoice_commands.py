from typing import List
import asyncio
from services.invoice_service import InvoiceService
from services.sales_order_service import SalesOrderService
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

async def deny_invoices(invoice_ids: List[str]):
    with Progress() as progress:
        task = progress.add_task("[cyan]Denying invoices...", total=len(invoice_ids))
        try:
            await InvoiceService.deny_invoices(invoice_ids)
            console.print("[green]Successfully denied invoices")
        except Exception as e:
            console.print(f"[red]Error denying invoices: {str(e)}")
        finally:
            progress.advance(task)

async def finish_sales_order(sales_order_id: str):
    try:
        await SalesOrderService.finish_sales_order(sales_order_id)
        console.print(f"[green]Successfully finished sales order {sales_order_id}")
    except Exception as e:
        console.print(f"[red]Error finishing sales order: {str(e)}")

async def issue_sales_order_invoice(sales_order_id: str):
    try:
        await InvoiceService.issue_sales_order_invoice(sales_order_id)
        console.print(f"[green]Successfully issued invoice for sales order {sales_order_id}")
    except Exception as e:
        console.print(f"[red]Error issuing invoice: {str(e)}")

async def finish_and_issue_invoice(sales_order_id: str, delay: int = 15):
    console.print("[bold cyan]Step 1: Finishing sales order[/bold cyan]")
    try:
        await finish_sales_order(sales_order_id)
        console.print(f"[yellow]Waiting {delay} seconds before issuing invoice...[/yellow]")
        await asyncio.sleep(delay)
        
        console.print("[bold cyan]Step 2: Issuing invoice[/bold cyan]")
        await issue_sales_order_invoice(sales_order_id)
        
        console.print("[bold green]✓ Complete: All operations finished successfully[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Operation failed: {str(e)}[/bold red]")

async def check_pending_invoices(invoice_ids: List[str]):
    with Progress() as progress:
        task = progress.add_task("[cyan]Checking pending invoices...", total=len(invoice_ids))
        try:
            result = await InvoiceService.check_pending_invoices(invoice_ids)
            console.print("[green]Successfully checked pending invoices")
            console.print(result)
        except Exception as e:
            console.print(f"[red]Error checking pending invoices: {str(e)}")
        finally:
            progress.advance(task)
