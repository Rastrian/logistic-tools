import requests
from typing import List
from utils.config import Config

class InvoiceService:
    @staticmethod
    async def reissue_invoice(invoice_id: str) -> dict:
        url = f"{Config.API_BASE_URL}/invoices/reissue"
        response = requests.post(
            url,
            headers=Config.get_headers(),
            json={"id": invoice_id}
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def update_invoices_error(invoice_ids: List[str], error_message: str) -> dict:
        url = f"{Config.API_BASE_URL}/invoices/error"
        response = requests.post(
            url,
            headers=Config.get_headers(),
            json={
                "invoice_ids": invoice_ids,
                "error_message": error_message
            }
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def deny_invoices(invoice_ids: List[str]) -> dict:
        url = f"{Config.API_BASE_URL}/invoices/issued_denied"
        response = requests.post(
            url,
            headers=Config.get_headers(),
            json={"invoice_ids": invoice_ids}
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    async def issue_sales_order_invoice(sales_order_id: str) -> dict:
        url = f"{Config.API_BASE_URL}/invoices/issue_sales_order_invoice"
        response = requests.post(
            url,
            headers=Config.get_headers(),
            json={"sales_order_id": sales_order_id}
        )
        response.raise_for_status()
        return response.json()
