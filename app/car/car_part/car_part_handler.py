from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .car_part_repository import CarPartRepository
from .car_part_model import CarPart
from .car_part_schema import CarPartCreate, CarPartUpdate


class CarPartHandler(BaseHandler):

    def __init__(self, repository: CarPartRepository):
        super().__init__(repository)
        self.repository: CarPartRepository = repository

    async def create_part(
        self,
        data: CarPartCreate,
    ) -> Optional[CarPart]:
        car_part_data = data.model_dump(exclude_unset=True)
        latin_name: str = self.__get_latin_name(name=data.name)
        car_part_data.update({"latin_name": latin_name})
        part: CarPart | None = await self.create_obj(car_part_data)
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=400, detail="Failed to create car part."
            )
        return part

    async def update_part(
        self,
        car_part_id: UUID,
        data: CarPartUpdate,
    ) -> Optional[CarPart]:
        car_part_data = data.model_dump(exclude_unset=True)
        latin_name: str = self.__get_latin_name(name=data.name)
        car_part_data.update({"latin_name": latin_name})
        part: CarPart | None = await self.update_obj(
            id=car_part_id,
            data=car_part_data,
        )
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Car part not found.",
            )
        return part

    async def delete_part(
        self,
        car_part_id: UUID,
    ) -> bool:
        result: bool = await self.delete_obj(id=car_part_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Failed to delete car part.",
            )
        return result

    async def get_part_by_id(
        self,
        car_part_id: UUID,
    ) -> Optional[CarPart]:
        part: CarPart | None = await self.get_obj_by_id(id=car_part_id)
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Car part not found.",
            )
        return part

    async def get_all_parts(
        self,
        query: str,
        cursor: int,
        take: int,
    ) -> tuple[int | None, list]:
        return await self.get_all_obj_by_scroll(
            query=query,
            cursor=cursor,
            take=take,
        )

    def __get_latin_name(
        self,
        name: str,
    ):
        rus_to_latin_hashtable = {
            # строчные буквы
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "yo",
            "ж": "zh",
            "з": "z",
            "и": "i",
            "й": "y",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "kh",
            "ц": "ts",
            "ч": "ch",
            "ш": "sh",
            "щ": "shch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
            # заглавные буквы
            "А": "A",
            "Б": "B",
            "В": "V",
            "Г": "G",
            "Д": "D",
            "Е": "E",
            "Ё": "Yo",
            "Ж": "Zh",
            "З": "Z",
            "И": "I",
            "Й": "Y",
            "К": "K",
            "Л": "L",
            "М": "M",
            "Н": "N",
            "О": "O",
            "П": "P",
            "Р": "R",
            "С": "S",
            "Т": "T",
            "У": "U",
            "Ф": "F",
            "Х": "Kh",
            "Ц": "Ts",
            "Ч": "Ch",
            "Ш": "Sh",
            "Щ": "Shch",
            "Ъ": "",
            "Ы": "Y",
            "Ь": "",
            "Э": "E",
            "Ю": "Yu",
            "Я": "Ya",
            # прочие символы
            " ": "-",
            ".": ".",
        }

        latin_word = []
        for char in name:
            latin_word.append(rus_to_latin_hashtable[char])
        return "".join(latin_word)
