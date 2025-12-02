from typing import List, Dict
from .utils import build_session, handle_response, DEFAULT_TIMEOUT

class AnalyticsAPI:
    def __init__(self, base_url: str, session=None):
        self.base_url = base_url.rstrip("/")
        self.session = session or build_session()

    def fraud_summary(self, timeout=DEFAULT_TIMEOUT) -> Dict:
        url = f"{self.base_url}/analytics/fraud-summary"
        r = self.session.get(url, timeout=timeout)
        return handle_response(r)

    def amount_by_type(self, timeout=DEFAULT_TIMEOUT) -> List[Dict]:
        url = f"{self.base_url}/analytics/amount-by-type"
        r = self.session.get(url, timeout=timeout)
        return handle_response(r)
