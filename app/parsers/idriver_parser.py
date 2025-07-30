import asyncio
import json
from bs4 import BeautifulSoup
from httpx import AsyncClient


idriver_brands = {
    "Не важно": "0",
    "Acura": "1",
    "Alfa Romeo": "3",
    # "Aprilia": "205",
    # "Arctic Cat": "221",
    # "Aston Martin": "8",
    # "Audi": "9",
    # "Austin": "285",
    # "Avatr": "299",
    # "BAW": "235",
    # "Belgee": "261",
    # "Benelli moto": "288",
    # "Bentley": "15",
    # "Beta": "206",
    # "BMW": "18",
    # "BMW moto": "199",
    # "Brilliance": "20",
    # "BRP": "265",
    # "Buell": "286",
    # "Buick": "22",
    # "BYD": "225",
    # "Cadillac": "24",
    # "Cafe racer": "294",
    # "Cagiva": "207",
    # "CCM": "208",
    # "CF Moto": "209",
    # "Changan": "190",
    # "Chery": "28",
    # "Chevrolet": "29",
    # "Chrysler": "30",
    # "Citroen": "31",
    # "Cupra": "272",
    # "Dacia": "32",
    # "Dadi": "226",
    # "Daewoo": "34",
    # "DAF": "184",
    # "Daihatsu": "36",
    # "Datsun": "203",
    # "Dennis": "198",
    # "Denza": "274",
    # "Derbi": "290",
    # "Dodge": "40",
    # "Dongfeng": "196",
    # "DS": "232",
    # "Ducati": "210",
    # "Eicher": "254",
    # "EXEED": "273",
    # "FAW": "43",
    # "FENDT": "250",
    # "Ferrari": "179",
    # "Fiat": "46",
    # "Ford": "47",
    # "Foton": "263",
    # "Geely": "51",
    # "Genesis": "189",
    # "Gilera": "213",
    # "GMC": "53",
    # "Great Wall": "55",
    # "Hafei": "284",
    # "Haima": "192",
    # "Hanomag": "253",
    # "Harley-Davidson": "194",
    # "Haval": "188",
    # "Hino": "193",
    # "Honda": "60",
    # "Honda moto": "200",
    # "Hongqi": "259",
    # "Hummer": "64",
    # "Husqvarna": "267",
    # "Hyosung moto": "297",
    # "Hyundai": "65",
    # "Indian moto": "292",
    # "Infiniti": "66",
    # "Iran-khodro": "113",
    # "Isuzu": "67",
    # "Iveco": "68",
    # "JAC": "234",
    # "Jaecoo": "298",
    # "Jaguar": "70",
    # "JCB": "229",
    # "Jeep": "71",
    # "Jetour": "271",
    # "JMC": "249",
    # "John Deere": "255",
    # "KAMAZ": "182",
    # "Kawasaki": "204",
    # "Kia": "75",
    # "Kogel": "279",
    # "Komatsu": "252",
    # "Krone": "301",
    # "KTM": "222",
    # "Kymco moto": "289",
    # "Lada": "161",
    # "Lamborghini": "77",
    # "Lancia": "78",
    # "Land Rover": "79",
    # "Landwind": "248",
    # "LDV": "177",
    # "Leapmotor": "228",
    # "Lexus": "82",
    # "Lifan": "178",
    # "Lincoln": "84",
    # "LiXiang": "257",
    # "Luxgen": "191",
    # "Mahindra": "241",
    # "MAN": "180",
    # "Maruti": "244",
    # "Maserati": "86",
    # "Mash moto": "287",
    # "Massey Ferguson": "236",
    # "Maybach": "283",
    # "Mazda": "88",
    # "Mercedes": "90",
    # "Mercury": "91",
    # "MG": "92",
    # "Microcar": "243",
    # "MINI": "93",
    # "Mitsubishi": "94",
    # "Mitsuoka": "247",
    # "Morini moto": "295",
    # "Moto Guzzi": "268",
    # "Mv Agusta motorcycle": "269",
    # "NIO": "246",
    # "Nissan": "96",
    # "Oldsmobile": "99",
    # "Omoda": "238",
    # "Opel": "101",
    # "Peugeot": "102",
    # "Peugeot moto": "214",
    # "PGO": "216",
    # "Piaggio": "217",
    # "Plymouth": "103",
    # "Polestar": "264",
    # "Pontiac": "105",
    # "Porsche": "106",
    # "Proton": "186",
    # "Ravon": "187",
    # "Renault": "108",
    # "Roewe": "242",
    # "Rolls-Royce": "110",
    # "Rover": "111",
    # "Royal Enfield moto": "270",
    # "S24": "280",
    # "Saab": "112",
    # "Samsung": "233",
    # "Saturn": "115",
    # "Scania": "183",
    # "Schmitz": "277",
    # "Scion": "197",
    # "Seat": "118",
    # "Skoda": "121",
    # "Smart": "123",
    # "Sollers": "282",
    # "SsangYong": "126",
    # "Subaru": "128",
    # "Suzuki": "129",
    # "Suzuki moto": "215",
    # "SYM moto": "293",
    # "Tank": "302",
    # "TATA": "202",
    # "Tesla": "175",
    # "Toyota": "138",
    # "Triumph": "218",
    # "Unimog": "251",
    # "Vespa": "219",
    # "Victory": "220",
    # "Volkswagen": "143",
    # "Volvo": "144",
    # "Vortex": "240",
    # "Voyah": "227",
    # "Wartburg": "237",
    # "Weltmeister": "245",
    # "YAMAHA": "201",
    # "Zeekr": "256",
    # "Zotye": "185",
    # "ZX": "239",
    # "ГАЗ": "163",
    # "ЗАЗ": "169",
    # "ЗИЛ": "195",
    # "ИЖ": "230",
    # "КРАЗ": "281",
    # "МАЗ": "181",
    # "Маз-Man": "276",
    # "Минск": "224",
    # "Москвич": "174",
    # "МТЗ": "223",
    # "УАЗ": "176",
}

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

    async def get_url(self, data: dict | None = None):
        async with AsyncClient(
            headers=headers,
            cookies=await self.__get_cookies(),
        ) as client:

            wha = {
                "type": "c",
                "txt": "",
                "brandID": "3",
                "clubID": "0",
            }

            response = await client.get(
                url=f"{self.base_url}mylist/addpart?postID=94571952"
            )
            response = await client.post(
                url="https://idriver.by/ajax/asi.php",
                data=wha,
            )

            # await client.post(url="https://idriver.by/ajax/asi.php", data=wha)
            # response = await client.post(
            #     url="https://idriver.by/ajax/asi.php", data=data
            # )
            return response.text

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


async def main():
    what = IDriverClient(
        user_phone="375293703729",
        user_password="freetouse",
        club_id="4346",
    )

    brands_data = {}

    html_doc = await what.get_url()
    soup = BeautifulSoup(markup=html_doc, features="lxml")
    items = soup.find_all("li")
    data = {}
    for item in items:
        name = item.text.strip()
        part_id = item.get("data-id")
        data[name] = part_id

    print(data)

    with open("idriver_car_parts.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# for item in all_serieses:
#     series_name = item.text
#     series_id = item.get("data-id")

#     series_data = {
#         series_name: series_id,
#     }
#     series.update(series_data)

# brands_data[idriver_brand_id] = {
#     "series": series,
# }

# with open("idk.json", mode="a", encoding="utf-8") as file:
#     json.dump(brands_data, file, ensure_ascii=False, indent=4)


asyncio.run(main())
