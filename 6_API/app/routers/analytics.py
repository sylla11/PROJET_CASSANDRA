from fastapi import APIRouter
from cassandra.cluster import Cluster

router = APIRouter(prefix="/analytics", tags=["Analytics - Cassandra Only"])

# Connexion Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect("paysim_ks")


# -------------------------------------------------------
# 1) Résumé Fraude
# -------------------------------------------------------
@router.get("/fraud-summary")
def fraud_summary():

    q1 = "SELECT COUNT(*) FROM transactions_by_customer"
    q2 = "SELECT SUM(isFraud) FROM transactions_by_customer"

    total_tx = session.execute(q1).one()[0]
    total_fraud = session.execute(q2).one()[0]

    rate = (total_fraud / total_tx) * 100 if total_tx > 0 else 0

    return {
        "total_transactions": total_tx,
        "frauds": total_fraud,
        "fraud_rate_percent": round(rate, 4)
    }


# -------------------------------------------------------
# 2) Total montant groupé par type (Cassandra compatible)
# -------------------------------------------------------
@router.get("/amount-by-type")
def amount_by_type():

    q = "SELECT type, amount FROM transactions_by_customer"

    rows = session.execute(q)

    totals = {}

    for r in rows:
        if r.type not in totals:
            totals[r.type] = 0.0
        totals[r.type] += float(r.amount)

    result = [
        {"type": t, "total_amount": total}
        for t, total in sorted(totals.items(), key=lambda x: x[1], reverse=True)
    ]

    return result
