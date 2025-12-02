import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .exceptions import APIRequestError, ConnectionError, NotFoundError, ValidationError

DEFAULT_TIMEOUT = 30  # seconds

def build_session(retries: int = 3, backoff: float = 0.3, status_forcelist=(500,502,503,504)):
    s = requests.Session()
    retry = Retry(total=retries, backoff_factor=backoff, status_forcelist=status_forcelist, allowed_methods=["GET","POST","PUT","DELETE","OPTIONS"])
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

def handle_response(r: requests.Response):
    try:
        data = r.json()
    except Exception:
        data = r.text

    if 200 <= r.status_code < 300:
        return data
    if r.status_code == 404:
        raise NotFoundError(f"Not found: {r.url} - {data}")
    if r.status_code == 422:
        raise ValidationError(f"Validation error: {r.url} - {data}")
    raise APIRequestError(f"API error {r.status_code}: {r.url} - {data}")
