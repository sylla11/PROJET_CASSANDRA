from fastapi import APIRouter
from app.db import get_session

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/fraud")
def fraud_stats():
    session = get_session()
    q = "SELECT SUM(isFraud) AS frauds, COUNT(*) AS total FROM transactions_by_customer"
    row = session.execute(q).one()
    return {
        "total": row.total,
        "frauds": row.frauds,
        "fraud_rate": (row.frauds / row.total) * 100
    }
