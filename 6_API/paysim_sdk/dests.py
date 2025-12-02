from typing import Dict
from .utils import build_session, handle_response, DEFAULT_TIMEOUT
import urllib.parse

class DestsAPI:
    def __init__(self, base_url: str, session=None):
        self.base_url = base_url.rstrip("/")
        self.session = session or build_session()

    def get(self, dest_id: str, timeout=DEFAULT_TIMEOUT) -> Dict:
        url = f"{self.base_url}/dests/{urllib.parse.quote(dest_id)}"
        r = self.session.get(url, timeout=timeout)
        return handle_response(r)
