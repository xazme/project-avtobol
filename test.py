import re
import asyncio
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
    url = "https://idriver.by/"
    async with AsyncClient(headers=headers, cookies=cookies) as client:
        response = await client.get(f"{url}")
        response = await client.get(f"{url}mylist")
        script_text = await client.get(f"{url}sections/mylist/addpart/new.php")

        match = re.search(r"location\.href=['\"](.*?)['\"]", script_text.text)
        match_post_id = re.search(r"postID=(\d+)", script_text.text)
        script_link = match.group(1)
        product_id = match_post_id.group(1)

        data_dict = {
            "ajaxDiv": "#addParts+.result",
            "addPart": "1",
            "carID": "0",
            "clubID": "4346",
            "clubRowID": "4346",
            "carList": "",
            "number": f"{product_id}",
            "partCode": "",
            "brand": "8",
            "model": "",
            "year": "",
            "body": "0",
            "driveV": "",
            "kpp": "",
            "gas": "",
            "driveType": "",
            "vin": "",
            "cat": "",
            "D2": "0",
            "J": "0",
            "ET": "",
            "DIA": "",
            "hole": "0",
            "PCD": "",
            "brandDisc": "",
            "serieID2": "",
            "D": "0",
            "w": "",
            "h": "",
            "tireYear": "",
            "loadIndex": "",
            "type": "0",
            "brandTyres": "",
            "serieID": "",
            "season": "0",
            "remains": "",
            "notation": "",
            "txt": "",
            "price": "",
            "prop22": "",
            "sale": "",
            "currency": "USD",
            "quantity": "1",
            "newPart": "0",
            "video": "",
            "undOrder": "",
            "phones": "",
            "dop": "",
            "postID": f"{product_id}",
        }
        response = await client.post(f"{url}{script_link}", data=data_dict)
        print(response.status_code)


asyncio.run(main=main())
