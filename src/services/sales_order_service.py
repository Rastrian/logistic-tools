import requests
from utils.config import Config

class SalesOrderService:
    @staticmethod
    async def finish_sales_order(sales_order_id: str) -> dict:
        url = f"{Config.API_BASE_URL}/sales_orders/finish"
        response = requests.post(
            url,
            headers=Config.get_headers(),
            json={"sales_order_id": sales_order_id}
        )
        response.raise_for_status()
        return response.json() 