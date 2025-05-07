from typing import List
from services.tanaporta_service import TanaportaService
from rich.console import Console

console = Console()

async def cancel_tanaporta_order(order_id: str):
    tanaporta = TanaportaService()
    
    # Authenticate
    console.print("[cyan]Authenticating with Tanaporta...[/cyan]")
    if not tanaporta.authenticate():
        console.print("[red]Authentication failed[/red]")
        return
    
    # Show current order status
    console.print(f"[cyan]Order {order_id}:[/cyan]")
    status = tanaporta.get_order_status(order_id)
    console.print(status)
    
    # Cancel the order
    console.print(f"[cyan]-- Cancellation:[/cyan]")
    result = tanaporta.cancel_order(order_id)
    if result:
        console.print(result)
    else:
        console.print("[red]Cancellation failed[/red]") 