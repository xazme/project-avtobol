import httpx
import time
from base64 import b64encode
from httpx import BasicAuth, Response, AsyncClient

# client_id = "8fb687202c5d49f5944272959dbfe7f8"
# client_secret = "2UV1rO4ivEEBvPHwshThnBnSGCZHvP3SGHUOfVS6gr1idr78In4hZwMsk8lcPGFA"

# basic_auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()

# url = "https://allegro.pl/auth/oauth/token"
# headers = {
#     "Authorization": f"Basic {basic_auth}",
#     "Content-Type": "application/x-www-form-urlencoded",
# }
# data = {"grant_type": "client_credentials"}

# response = httpx.post(url, headers=headers, data=data)
# access_token = response.json()["access_token"]

# print(access_token)
# url = "https://api.allegro.pl/sale/categories"
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Accept": "application/vnd.allegro.public.v1+json",
# }
# url_s = "https://api.allegro.pl/sale/categories"
# response = httpx.get(url_s, headers=headers)
# print(response.status_code)
# print(response.json())


import time
from base64 import b64encode
from httpx import AsyncClient, Response


class AllegroClient:
    def __init__(
        self, client_id: str, client_secret: str, base_url: str, base_api_url: str
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.base_api_url = base_api_url
        self.access_token = None
        self.token_expiry = 0  # UNIX время, когда токен истекает

    def _get_auth_headers(self) -> dict:
        auth = b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        return {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _get_pass_data(self) -> dict:
        return {"grant_type": "client_credentials"}

    def _ensure_token(self):
        if self.access_token is None or time.time() > self.token_expiry:
            self._get_access_token()

    def _get_access_token(self):
        url = f"{self.base_url}/auth/oauth/token"
        response: Response = httpx.post(
            url=url,
            headers=self._get_auth_headers(),
            data=self._get_pass_data(),
        )
        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.token_expiry = time.time() + token_data["expires_in"]

    def _get_api_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.allegro.public.v1+json",
        }

    async def get_categories(self, parent_id: str = None) -> dict:
        self._ensure_token()
        url = f"{self.base_api_url}/sale/categories"
        if parent_id:
            url += f"?parent.id={parent_id}"

        async with AsyncClient() as client:
            response = await client.get(url, headers=self._get_api_headers())
            return response.json()


asd = AllegroClient(
    client_id="pass",
    client_secret="pass",
    base_url="https://allegro.pl",
    base_api_url="https://api.allegro.pl",
)
