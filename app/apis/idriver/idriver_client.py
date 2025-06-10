import asyncio
from httpx import AsyncClient

# from ..shared import headers

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://example.com",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}


class IDriverClient:
    def __init__(
        self,
        user_phone: str,
        user_password: str,
    ):
        self.base_url = "https://idriver.by/"
        self.headers = headers
        self.user_phone = user_phone
        self.user_password = user_password
        self.cookies = None

    async def get_cookies(self):
        if self.cookies:
            return self.cookies

        async with AsyncClient(headers=self.headers) as client:
            await client.get(url=self.base_url)
            await client.get(url=f"{self.base_url}login")
            login_data: dict[str, str] = {
                "login": self.user_phone,
                "pswrd1": self.user_password,
                "ajaxDiv": "#formLogin+formResult",
            }
            response = await client.post(
                url=f"{self.base_url}ajax/forms/formLogin.php",
                follow_redirects=True,
                data=login_data,
            )
            if not self.cookies:
                self.cookies = dict(response.cookies)


async def main():
    what = IDriverClient(user_phone="375293703729", user_password="freetouse")
    await what.get_cookies()


asyncio.run(main=main())
