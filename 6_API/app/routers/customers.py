from fastapi import APIRouter
from app.db import get_session

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/")
def list_customers(limit: int = 100, offset: int = 0):
    session = get_session()
    q = f"SELECT customer_id, step, amount, dest_id FROM transactions_by_customer LIMIT {limit}"
    rows = session.execute(q)
    return [dict(r._asdict()) for r in rows]


@router.get("/{customer_id}")
def get_customer(customer_id: str):
    session = get_session()
    q = f"SELECT * FROM transactions_by_customer WHERE customer_id = '{customer_id}' LIMIT 20"
    rows = session.execute(q)
    return [dict(r._asdict()) for r in rows]
