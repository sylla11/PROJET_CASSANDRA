#%% ----------------------------------------------------
# INITIALISATION — Import + création du client
print(">>> Importing PaySimClient")

from paysim_sdk import PaySimClient

client = PaySimClient("http://127.0.0.1:8000")

print("Client initialized:", client)
#%% ----------------------------------------------------
# TEST 1 : Health check
print(">>> TEST 1 — Health check")

try:
    r = client.health()
    print("OK ✓ Health:", r)
except Exception as e:
    print("ERROR:", e)
#%% ----------------------------------------------------
# TEST 2 : Fraud summary (analytics)
print(">>> TEST 2 — analytics.fraud_summary")

try:
    r = client.analytics.fraud_summary()
    print("Fraud Summary ✓", r)
except Exception as e:
    print("ERROR:", e)
#%% ----------------------------------------------------
# TEST 3 : Amount by type
print(">>> TEST 3 — analytics.amount_by_type")

try:
    r = client.analytics.amount_by_type()
    print("Amount by type ✓", r[:5], "...")  # affiche les 5 premières lignes
except Exception as e:
    print("ERROR:", e)
#%% ----------------------------------------------------
# TEST 4 : Customers — list
print(">>> TEST 4 — customers.list")

try:
    r = client.customers.list(limit=5)
    print("Customers list ✓", r)
except Exception as e:
    print("ERROR:", e)
#%% ----------------------------------------------------
# TEST 5 : Customers — get
print(">>> TEST 5 — customers.get")

try:
    # prends un ID existant dans ta base
    sample = client.customers.list(limit=1)
    cid = sample[0]["customer_id"]
    print("Testing customer:", cid)

    r = client.customers.get(cid)
    print("Customer ✓", r)
except Exception as e:
    print("ERROR:", e)
#%% ----------------------------------------------------
# TEST 6 : Destinations — get
print(">>> TEST 6 — dests.get")

try:
    tx = client.customers.list(limit=1)[0]
    did = tx.get("dest_id", None)

    if did:
        r = client.dests.get(did)
        print("Destination ✓", r)
    else:
        print("No dest_id found in sample transaction.")
except Exception as e:
    print("ERROR:", e)
#%% ----------------------------------------------------
# TEST 7 : Fraud stats (simple)
print(">>> TEST 7 — stats.fraud")

try:
    r = client.stats.fraud()
    print("Fraud stats ✓", r)
except Exception as e:
    print("ERROR:", e)

# %%
