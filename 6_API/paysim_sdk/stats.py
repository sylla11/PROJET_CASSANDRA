from .utils import build_session, handle_response, DEFAULT_TIMEOUT

class StatsAPI:
    def __init__(self, base_url: str, session=None):
        self.base_url = base_url.rstrip("/")
        self.session = session or build_session()

    def fraud(self, timeout=DEFAULT_TIMEOUT):
        url = f"{self.base_url}/stats/fraud"
        r = self.session.get(url, timeout=timeout)
        return handle_response(r)
