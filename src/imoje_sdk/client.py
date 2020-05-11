from urllib.parse import urljoin

import requests

from imoje_sdk.enums import AllowedHTTPMetohds


class Client:
    BASE_URL = "https://api.imoje.pl/v1/merchant"

    def __init__(self, merchant_id, auth_token):
        super().__init__()
        self.merchant_id = merchant_id
        self._auth_token = auth_token

    def request(self, path: str, payload: dict, method: AllowedHTTPMetohds = AllowedHTTPMetohds.POST, headers=None,
                **kwargs):
        _headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self._auth_token}"
        }

        if headers:
            _headers.update(headers)

        url = urljoin(self.request_url, path)

        if method is AllowedHTTPMetohds.POST:
            return requests.post(url, data=payload, headers=_headers, timeout=60, **kwargs)
        else:
            # GET
            return requests.get(url, params=payload, headers=_headers, timeout=60, **kwargs)

    @property
    def request_url(self):
        return urljoin(self.BASE_URL, self.merchant_id)
