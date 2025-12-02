# 6_API/app/routers/dests_cursor.py

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any
from uuid import UUID
from app.database import get_session

router = APIRouter(prefix="/dests", tags=["Destinations - Cursor Pagination"])


@router.get("/{dest_id}/paged")
def get_dest_transactions_cursor(
    dest_id: str,
    limit: int = Query(50, ge=1, le=500),
    last_step: Optional[int] = Query(None),
    last_tx: Optional[UUID] = Query(None)
) -> Dict[str, Any]:

    session = get_session()

    if last_step is None:
        cql = """
            SELECT dest_id, step, transaction_id, type, amount,
                   customer_id, oldbalanceDest, newbalanceDest, isFraud
            FROM transactions_by_dest
            WHERE dest_id = %s
            LIMIT %s;
        """
        params = [dest_id, limit]

    else:
        cql = """
            SELECT dest_id, step, transaction_id, type, amount,
                   customer_id, oldbalanceDest, newbalanceDest, isFraud
            FROM transactions_by_dest
            WHERE dest_id = %s
              AND (step, transaction_id) > (%s, %s)
            LIMIT %s;
        """
        params = [dest_id, last_step, last_tx, limit]

    try:
        rows = session.execute(cql, params)
        rows = [dict(r._asdict()) for r in rows]
    except Exception:
        raise HTTPException(status_code=500, detail="Database query failed")

    if rows:
        next_cursor = {
            "last_step": rows[-1]["step"],
            "last_tx": rows[-1]["transaction_id"]
        }
    else:
        next_cursor = None

    return {
        "dest_id": dest_id,
        "count": len(rows),
        "limit": limit,
        "next_cursor": next_cursor,
        "results": rows
    }
