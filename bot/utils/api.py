import requests
from requests.exceptions import HTTPError

from data.config import API_URL

class FastAPIClient(requests.Session):
    def __init__(self):
        super().__init__()
        self.base_url = API_URL

    def make_request(self, method, endpoint, data=None, params=None, user_id: int=None):
        url = f"{self.base_url}{endpoint}"
        try:
            access = self.request("POST", f"{self.base_url}users/access/{user_id}/")
            token = ''
            access_response = access.json()
            if access_response.get("status_code") == 403:
                token = access_response.get("detail")
            else:
                token = access_response.get("token")
            response = self.request(method, url, json=data, params=params, headers={"authorization": f"Bearer {token}"})
            response.raise_for_status()
            return True, response.json()
        except HTTPError:
            return False, response.json()
