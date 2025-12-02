# 6_API/app/routers/customers_cursor.py

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any
from uuid import UUID
from app.database import get_session

router = APIRouter(prefix="/customers", tags=["Customers - Cursor Pagination"])


@router.get("/{customer_id}/paged")
def get_customer_transactions_cursor(
    customer_id: str,
    limit: int = Query(50, ge=1, le=500),
    last_step: Optional[int] = Query(None),
    last_tx: Optional[UUID] = Query(None)
) -> Dict[str, Any]:

    session = get_session()

    # --- 1️⃣ Construire la requête CQL ---
    if last_step is None:
        # Première page → pas de curseur
        cql = """
            SELECT customer_id, step, transaction_id, type, amount,
                   dest_id, oldbalanceOrg, newbalanceOrg, isFraud
            FROM transactions_by_customer
            WHERE customer_id = %s
            LIMIT %s;
        """
        params = [customer_id, limit]

    else:
        # Pages suivantes → utiliser le curseur (step, transaction_id)
        cql = """
            SELECT customer_id, step, transaction_id, type, amount,
                   dest_id, oldbalanceOrg, newbalanceOrg, isFraud
            FROM transactions_by_customer
            WHERE customer_id = %s
              AND (step, transaction_id) > (%s, %s)
            LIMIT %s;
        """
        params = [customer_id, last_step, last_tx, limit]

    try:
        rows = session.execute(cql, params)
        rows = [dict(r._asdict()) for r in rows]
    except Exception:
        raise HTTPException(status_code=500, detail="Database query failed")

    # --- 2️⃣ Calcul du curseur pour la page suivante ---
    if rows:
        next_cursor = {
            "last_step": rows[-1]["step"],
            "last_tx": rows[-1]["transaction_id"]
        }
    else:
        next_cursor = None

    return {
        "customer_id": customer_id,
        "count": len(rows),
        "limit": limit,
        "next_cursor": next_cursor,
        "results": rows
    }
