from typing import Optional
from .analytics import AnalyticsAPI
from .customers import CustomersAPI
from .dests import DestsAPI
from .stats import StatsAPI
from .utils import build_session

class PaySimClient:
    """
    PaySimClient(base_url: str)
    - base_url: base address of the running API, e.g. "http://127.0.0.1:8000"
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8000", session=None):
        self.base_url = base_url.rstrip("/")
        self._session = session or build_session()

        # sub-clients
        self.analytics = AnalyticsAPI(self.base_url, session=self._session)
        self.customers = CustomersAPI(self.base_url, session=self._session)
        self.dests = DestsAPI(self.base_url, session=self._session)
        self.stats = StatsAPI(self.base_url, session=self._session)

    def health(self, timeout: int = 10) -> dict:
        """Call root health endpoint."""
        r = self._session.get(f"{self.base_url}/", timeout=timeout)
        return r.json()
