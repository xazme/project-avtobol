import httpx
from base64 import b64encode
from httpx import BasicAuth, Response

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


class AllegroClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
        base_api_url: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.base_api_url = base_api_url
        self.access_token = None

    def get_acccess_token(
        self,
    ):
        token_url = f"{self.base_url}/auth/oauth/token"
        response: Response = httpx.post(
            url=token_url,
            headers=self.__get_headers(),
            data=self.__get_pass_data(),
        )
        print(response.status_code)

    def __get_headers(
        self,
    ) -> dict:
        auth = b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return headers

    def __get_pass_data(
        self,
    ) -> dict:
        passdata = {"grant_type": "client_credentials"}
        return passdata


asd = AllegroClient(
    client_id="pass",
    client_secret="pass",
    base_url="https://allegro.pl",
    base_api_url="https://api.allegro.pl",
)

asd.get_acccess_token()
