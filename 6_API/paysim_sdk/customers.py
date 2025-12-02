from typing import List, Dict, Optional
from .utils import build_session, handle_response, DEFAULT_TIMEOUT
import urllib.parse

class CustomersAPI:
    def __init__(self, base_url: str, session=None):
        self.base_url = base_url.rstrip("/")
        self.session = session or build_session()

    def get(self, customer_id: str, timeout=DEFAULT_TIMEOUT) -> Dict:
        url = f"{self.base_url}/customers/{urllib.parse.quote(customer_id)}"
        r = self.session.get(url, timeout=timeout)
        return handle_response(r)

    def list(self, limit: int = 100, offset: int = 0, timeout=DEFAULT_TIMEOUT) -> List[Dict]:
        url = f"{self.base_url}/customers?limit={limit}&offset={offset}"
        r = self.session.get(url, timeout=timeout)
        return handle_response(r)

    def find_by_date_range(self, from_step: int, to_step: int, limit:int=100, timeout=DEFAULT_TIMEOUT) -> List[Dict]:
        """Example: server can implement filtering by step range; adjust according to API."""
        url = f"{self.base_url}/customers/search?from_step={from_step}&to_step={to_step}&limit={limit}"
        r = self.session.get(url, timeout=timeout)
        return handle_response(r)
