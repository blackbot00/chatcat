from fastapi import Request
from datetime import datetime, timedelta

from app.db.mongo import users_col, payments_col
from app.constants.plans import PREMIUM_PLANS

async def cashfree_webhook(request: Request):
    payload = await request.json()

    if payload.get("order_status") != "PAID":
        return {"ok": True}

    order_id = payload["order_id"]
    payment = payments_col.find_one({"order_id": order_id})

    if not payment:
        return {"ok": True}

    plan = PREMIUM_PLANS[payment["plan"]]
    expiry = datetime.utcnow() + timedelta(days=plan["days"])

    users_col.update_one(
        {"_id": payment["user_id"]},
        {"$set": {
            "premium": True,
            "premium_expiry": expiry.strftime("%d-%m-%Y")
        }}
    )

    payments_col.update_one(
        {"order_id": order_id},
        {"$set": {"status": "PAID"}}
    )

    return {"ok": True}
