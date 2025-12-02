from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analytics, customers, dests, stats


# ---------------------------------------------------------
#   APPLICATION FASTAPI
# ---------------------------------------------------------
app = FastAPI(
    title="PaySim Cassandra API",
    description="API Full-Stack Cassandra + FastAPI pour l’analyse des transactions PaySim",
    version="1.0.0",
)


# ---------------------------------------------------------
#   CORS (autorisations Web)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # autoriser tout (dashboard, sdk, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "API OK",
        "message": "Bienvenue sur l’API PaySim",
        "endpoints": [
            "/analytics/fraud-summary",
            "/analytics/amount-by-type",
            "/customers",
            "/customers/{customer_id}",
            "/dests/{dest_id}",
            "/stats/fraud"
        ]
    }


# ---------------------------------------------------------
#   INCLUSION DES ROUTES
# ---------------------------------------------------------
app.include_router(analytics.router)
app.include_router(customers.router)
app.include_router(dests.router)
app.include_router(stats.router)
