# paysim_sdk (local)

Simple Python SDK to call the PaySim Cassandra API.

Usage:

```python
from paysim_sdk import PaySimClient

client = PaySimClient("http://127.0.0.1:8000")

# health
print(client.health())

# analytics
print(client.analytics.fraud_summary())
print(client.analytics.amount_by_type())

# customers
print(client.customers.get("C12345"))
print(client.customers.list(limit=10))
