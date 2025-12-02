# 6_API/app/routers/dests.py
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any
from app.database import get_session

router = APIRouter(prefix="/dests", tags=["Destinations"])


def _build_where_clause(
    dest_id: str,
    tx_type: Optional[str],
    is_fraud: Optional[int],
    step_min: Optional[int],
    step_max: Optional[int]
) -> (str, list):

    conditions = ["dest_id = %s"]
    params = [dest_id]

    if tx_type is not None:
        conditions.append("type = %s")
        params.append(tx_type)

    if is_fraud is not None:
        conditions.append("isFraud = %s")
        params.append(is_fraud)

    if step_min is not None:
        conditions.append("step >= %s")
        params.append(step_min)

    if step_max is not None:
        conditions.append("step <= %s")
        params.append(step_max)

    return " AND ".join(conditions), params


@router.get("/{dest_id}")
def get_transactions_by_dest(
    dest_id: str,
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    tx_type: Optional[str] = Query(None),
    is_fraud: Optional[int] = Query(None, ge=0, le=1),
    step_min: Optional[int] = Query(None, ge=0),
    step_max: Optional[int] = Query(None, ge=0)
) -> Dict[str, Any]:

    session = get_session()

    where_clause, params = _build_where_clause(
        dest_id, tx_type, is_fraud, step_min, step_max
    )

    # LIMIT index = offset + limit
    cql = f"""
        SELECT step, transaction_id, type, amount, customer_id,
               oldbalanceDest, newbalanceDest, isFraud
        FROM transactions_by_dest
        WHERE {where_clause}
        LIMIT %s ALLOW FILTERING;
    """

    cql_params = params + [offset + limit]

    try:
        rows = session.execute(cql, cql_params)
    except Exception:
        raise HTTPException(status_code=500, detail="Database query failed")

    results = [dict(r._asdict()) for r in rows]

    paginated = results[offset: offset + limit]

    return {
        "dest_id": dest_id,
        "returned": len(paginated),
        "limit": limit,
        "offset": offset,
        "filters": {
            "type": tx_type,
            "isFraud": is_fraud,
            "step_min": step_min,
            "step_max": step_max
        },
        "results": paginated
    }
