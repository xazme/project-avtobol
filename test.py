import re
import base64
import bs4
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
        print(product_id)
        data_dict = {
            "ajaxDiv": "#addParts+.result",
            "addPart": "1",
            "carID": "0",
            "clubID": "4346",
            "clubRowID": "4346",
            "carList": "",
            "number": "567156780",
            "partCode": "",
            "brand": "3",
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
        # POST
        response = await client.post(f"{url}{script_link}", data=data_dict)
        print(response.text)

        # DELETE
        # response = await client.get(
        #     f"{url}sections/mylist/addpart/kill.php?id={product_id}&table=avtorazborka_posts2"
        # )

        # UPDATE
        # response = await client.get(f"{url}mylist/addpart?postID=f{product_id}")
        # data_dict_upd = {
        #     "ajaxDiv": "#addParts+.result",
        #     "addPart": "1",
        #     "carID": "0",
        #     "clubID": "4346",
        #     "clubRowID": "4346",
        #     "carList": "https://www.google.com/imgres?q=%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B0%20%D0%BD%D0%B0%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D1%83&imgurl=https%3A%2F%2Fcdn-icons-png.flaticon.com%2F512%2F181%2F181531.png&imgrefurl=https%3A%2F%2Fwww.flaticon.com%2Fru%2Ffree-icon%2Flink_181531&docid=_KTH8SVd4hj9EM&tbnid=vgq0iNf_dMqotM&vet=12ahUKEwiehdmBheeNAxUnHRAIHY0QPKsQM3oECHAQAA..i&w=512&h=512&hcb=2&ved=2ahUKEwiehdmBheeNAxUnHRAIHY0QPKsQM3oECHAQAA",
        #     "number": "",
        #     "partCode": "",
        #     "brand": "1",
        #     "model": "",
        #     "year": "",
        #     "body": "0",
        #     "driveV": "",
        #     "kpp": "",
        #     "gas": "",
        #     "driveType": "",
        #     "vin": "",
        #     "cat": "",
        #     "D2": "0",
        #     "J": "0",
        #     "ET": "",
        #     "DIA": "",
        #     "hole": "0",
        #     "PCD": "",
        #     "brandDisc": "",
        #     "serieID2": "",
        #     "D": "0",
        #     "w": "",
        #     "h": "",
        #     "tireYear": "",
        #     "loadIndex": "",
        #     "type": "0",
        #     "brandTyres": "",
        #     "serieID": "",
        #     "season": "0",
        #     "remains": "",
        #     "notation": "",
        #     "txt": "",
        #     "price": "",
        #     "prop22": "",
        #     "sale": "",
        #     "currency": "USD",
        #     "quantity": "1",
        #     "newPart": "0",
        #     "video": "",
        #     "undOrder": "",
        #     "phones": "",
        #     "dop": "",
        #     "postID": f"{product_id}",
        # }
        # response = await client.post(
        #     f"{url}mylist/addpart?postID=f{product_id}",
        #     data=data_dict_upd,
        # )
        # print(response.status_code)

        # PHOTO
        ##https://idriver.by/sections/mylist/addpart/inc/photoLoader.php?postID=94462608

        # with open("test.jpeg", "rb") as file:
        #     encoded_image = base64.b64encode(file.read()).decode("utf-8")
        #     data_pic = {
        #         "photo": ["test"],
        #         "postID": product_id,
        #         "pic": f"{"test"}data:image/jpeg;base64,{encoded_image}",
        #         "test": "0",
        #         "mini": "",
        #     }

        #     response = await client.post(
        #         f"{url}sections/mylist/addpart/inc/photoLoader.php?postID={product_id}",
        #         data=data_pic,
        #     )


asyncio.run(main=main())
