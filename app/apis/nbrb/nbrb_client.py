import httpx
import asyncio

# from app.apis.shared import headers


async def get_currencies():
    """
    431 - USD,
    456 - RUS,
    451 - EUR,
    """
    url = "https://api.nbrb.by/exrates/rates/"
    currencies_id: dict[str, int] = {
        "USD": 431,
        "RUS": 456,
        "EUR": 451,
    }

    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"{url}{currency_id}") for currency_id in currencies_id.values()
        ]
        responses = await asyncio.gather(*tasks)

    course = {}
    for currency, response in zip(currencies_id.keys(), responses):
        payload: dict = response.json()
        data = payload.get("Cur_OfficialRate")
        course[currency] = data

    return course


async def main():
    res = await get_currencies()
    print(res)


asyncio.run(main=main())
