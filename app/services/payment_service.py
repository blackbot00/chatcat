import httpx
import uuid
from datetime import datetime, timedelta

from app.config import CASHFREE_APP_ID, CASHFREE_SECRET_KEY

CASHFREE_ORDER_URL = "https://api.cashfree.com/pg/orders"

async def create_cashfree_order(user_id: int, amount: int):
    order_id = f"CD_{user_id}_{uuid.uuid4().hex[:6]}"

    headers = {
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": str(user_id),
            "customer_phone": "9999999999"
        }
    }

    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(CASHFREE_ORDER_URL, json=payload, headers=headers)
        res.raise_for_status()
        return res.json()
