import re
import base64
import asyncio
from uuid import uuid4
from asyncio import Queue
from httpx import AsyncClient, Response
from idriver_schema import IDriverProductCreate, IDriverProductUpdate

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
        club_id: str,
    ):
        self.base_url = "https://idriver.by/"
        self.headers = headers
        self.user_phone = user_phone
        self.user_password = user_password
        self.club_id = club_id
        self.cookies = {}

    async def create_product(
        self,
        product_data: IDriverProductCreate,
    ):
        async with AsyncClient(
            headers=headers,
            cookies=await self.__get_cookies(),
        ) as client:
            script_path: str = await self.__get_post_script()
            post_id = await self.__get_post_id(script_link=script_path)

            data: IDriverProductCreate = product_data.model_copy()
            data.clubID = self.club_id
            data.clubRowID = self.club_id
            data.postID = post_id

            response: Response = await client.post(
                f"{self.base_url}{script_path}",
                data=data.model_dump(),
            )

    async def update_product(
        self,
        post_id: str,
        product_data: IDriverProductUpdate,
    ):
        async with AsyncClient(
            headers=headers,
            cookies=await self.__get_cookies(),
        ) as client:
            await client.get(f"{self.base_url}mylist/addpart?postID=f{post_id}")
            data: IDriverProductCreate = product_data.model_copy()
            data.clubID = self.club_id
            data.clubRowID = self.club_id
            data.postID = post_id
            response: Response = await client.post(
                f"{self.base_url}mylist/addpart?postID=f{post_id}",
                data=data.model_dump(),
            )
            return "y"

    async def delete_product(
        self,
        post_id: str,
    ):
        async with AsyncClient(
            headers=headers,
            cookies=await self.__get_cookies(),
        ) as client:
            response = await client.get(
                f"{self.base_url}sections/mylist/addpart/kill.php?id={post_id}&table=avtorazborka_posts2"
            )
            return

    async def upload_file(
        self,
        post_id: str,
        files: list[bytes],
    ):
        files_data = self.__prepare_file(post_id=post_id, files=files)
        async with AsyncClient(
            headers=headers,
            cookies=await self.__get_cookies(),
        ) as client:
            queue = Queue()
            for file_data in files_data:
                await queue.put(
                    client.post(
                        f"{self.base_url}sections/mylist/addpart/inc/photoLoader.php?postID={post_id}",
                        data=file_data,
                    )
                )
            await self.__async_worker(queue=queue)

    # https://idriver.by/ajax/killer.php?params=1072376310|aphotos|no|&div=Element1072376310&url=https:/idriver.by/mylist/addpart?postID=94496924

    async def get_my_list(self):
        async with AsyncClient(
            headers=headers,
            cookies=await self.__get_cookies(),
        ) as client:
            await client.get(url=f"{self.base_url}mylist")

    async def __get_post_script(self):
        async with AsyncClient(
            headers=headers,
            cookies=await self.__get_cookies(),
        ) as client:
            await client.get(f"{self.base_url}")
            await client.get(f"{self.base_url}mylist")
            script_text: Response = await client.get(
                f"{self.base_url}sections/mylist/addpart/new.php"
            )
            match_script = re.search(
                r"location\.href=['\"](.*?)['\"]", script_text.text
            )
            script_link: str = match_script.group(1)
            return script_link

    async def __get_post_id(self, script_link: str):
        match_post_id = re.search(r"postID=(\d+)", script_link)
        post_id = match_post_id.group(1)
        return post_id

    async def __get_cookies(self):
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
            cookies = dict(response.cookies)
            self.cookies = cookies
            return cookies

    async def __async_worker(
        self,
        queue: Queue,
    ):
        while not queue.empty():
            task = await queue.get()
            await task
            queue.task_done()

    def __prepare_file(
        self,
        post_id: str,
        files: list[bytes],
    ):
        ready_pictures = []
        for file in files:
            encoded_image = base64.b64encode(file).decode("utf-8")
            filename = str(uuid4())
            data_pic = {
                "photo": filename,
                "postID": post_id,
                "pic": f"{filename}data:image/jpeg;base64,{encoded_image}",
                "test": "0",
                "mini": "",
            }
            ready_pictures.append(data_pic)
        return ready_pictures


async def main():
    what = IDriverClient(
        user_phone="375293703729",
        user_password="freetouse",
        club_id="4346",
    )

    with open("image.png", "rb") as file:
        file_bytes = file.read()
        await what.upload_file(post_id="94507030", files=[file_bytes])


asyncio.run(main=main())
