from pydantic import BaseModel, Field


class IDriverProductBase(BaseModel):
    # ИНФОРМАЦИЯ ДЛЯ IDRIVER
    ajaxDiv: str = Field("#addParts+.result", description="AJAX target div")
    addPart: str = Field("1", description="Добавить запчасть")
    carID: str = Field("0", description="ID машины")
    clubID: str = Field("", description="ID клуба")
    clubRowID: str = Field("", description="ID строки клуба")

    # ЗАПЧАСТИ
    carList: str = Field("", description="Список машин")
    number: str = Field("", description="Номер детали")
    partCode: str = Field("", description="Код детали")
    brand: str = Field("", description="Бренд автомобиля")
    model: str = Field("", description="Модель автомобиля")
    year: str = Field("", description="Год выпуска")
    body: str = Field("0", description="Тип кузова")
    driveV: str = Field("", description="Привод (вариант)")
    gas: str = Field("", description="Тип топлива")
    driveType: str = Field("", description="Тип привода")
    vin: str = Field("", description="VIN номер")
    cat: str = Field("", description="Категория")

    # ДИСКИ
    D2: str = Field("0", description="Радиус")
    J: str = Field("0", description="Ширина")
    ET: str = Field("", description="Вылет")
    DIA: str = Field("", description="Диаметр центрального отверстия")
    hole: str = Field("0", description="Количество отверстий")
    PCD: str = Field("", description="Разболтовка")
    brandDisc: str = Field("", description="Бренд диска")
    serieID2: str = Field("", description="Серия диска")

    # ШИНЫ
    D: str = Field("", description="Радиус шины")
    w: str = Field("", description="Ширина шины")
    h: str = Field("", description="Высота шины")
    tireYear: str = Field("", description="Год шины")
    loadIndex: str = Field("", description="Индекс нагрузки")
    type: str = Field("0", description="Тип детали")
    brandTyres: str = Field("", description="Бренд шины")
    serieID: str = Field("", description="Серия шины")
    season: str = Field("0", description="Сезон")
    remains: str = Field("", description="Остатки")

    # ИНФОРМАЦИЯ
    notation: str = Field("", description="Заметка к заголовку")
    txt: str = Field("", description="Описание")
    price: str = Field("", description="Цена")
    prop22: str = Field("", description="Стоимость закупки")
    sale: str = Field("", description="Скидка")
    currency: str = Field("USD", description="Валюта")
    quantity: str = Field("1", description="Количество")
    newPart: str = Field("", description="Состояние (новое или бу)")
    undOrder: str = Field("", description="в наличии или под заказ")
    phones: str = Field("", description="Телефоны")
    dop: str = Field("", description="Примечания для продавцов")
    postID: str = Field("", description="ID поста")


class IDriverProductCreate(IDriverProductBase):
    pass


class IDriverProductUpdate(IDriverProductBase):
    pass
