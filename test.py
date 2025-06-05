import asyncio
import httpx
from httpx import AsyncClient

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://example.com",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}

cookies = {
    "proof": "1",
    "user_m": "375293703729",
    "user_p": "84e82bd508314529268aaf38805f738a",
    "user_type": "phone",
}


async def main():
    async with httpx.AsyncClient(headers=headers, cookies=cookies) as client:
        responce = await client.get("https://idriver.by")
        # responce = await client.get("https://idriver.by/login")
        responce = await client.get("https://idriver.by/mylist")
        print(responce.text)


asyncio.run(main=main())
