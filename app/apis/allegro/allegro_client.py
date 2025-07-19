import time
import httpx
import json
import asyncio
from base64 import b64encode
from datetime import datetime
from pydantic import BaseModel
from pytz import timezone
from httpx import AsyncClient, Response
from pydantic import BaseModel, Field
from app.core import settings
from app.car.product import Product as ORMProduct
from ..shared import Translator


class Category(BaseModel):
    id: str


class RangeValue(BaseModel):
    from_: str = Field(..., alias="from")
    to: str


class Parameter(BaseModel):
    id: str
    name: str
    rangeValue: RangeValue | None = None
    values: list[str] = []
    valuesIds: list[str] = []


class Product(BaseModel):
    name: str
    category: Category
    id: str
    idType: str
    parameters: list[Parameter] = []
    images: list[str] = []


class Quantity(BaseModel):
    value: int


class ResponsiblePerson(BaseModel):
    id: str
    name: str


class ResponsibleProducer(BaseModel):
    type: str
    id: str


class SafetyInformation(BaseModel):
    type: str
    description: str


class ProductSetItem(BaseModel):
    product: Product
    quantity: Quantity
    responsiblePerson: ResponsiblePerson
    responsibleProducer: ResponsibleProducer
    safetyInformation: SafetyInformation
    marketedBeforeGPSRObligation: bool


class B2B(BaseModel):
    buyableOnlyByBusiness: bool


class Attachment(BaseModel):
    id: str


class FundraisingCampaign(BaseModel):
    id: str
    name: str


class AdditionalServices(BaseModel):
    id: str
    name: str


class Stock(BaseModel):
    available: int
    unit: str


class Delivery(BaseModel):
    handlingTime: str
    shippingRates: None = None
    additionalInfo: str
    shipmentDate: datetime


class Publication(BaseModel):
    duration: str
    startingAt: datetime
    status: str
    republish: bool


class MarketplacePrice(BaseModel):
    amount: str
    currency: str


class SellingModeMarketplace(BaseModel):
    price: MarketplacePrice


class AdditionalMarketplaces(BaseModel):
    allegro_cz: dict[str, SellingModeMarketplace] = {}


class CompatibilityItem(BaseModel):
    type: str
    text: str


class CompatibilityList(BaseModel):
    items: list[CompatibilityItem]


class AfterSalesItem(BaseModel):
    id: str
    name: str


class AfterSalesServices(BaseModel):
    impliedWarranty: AfterSalesItem
    returnPolicy: AfterSalesItem
    warranty: AfterSalesItem


class SizeTable(BaseModel):
    id: str
    name: str


class Contact(BaseModel):
    id: str
    name: str


class WholesalePriceList(BaseModel):
    id: str
    name: str


class Discounts(BaseModel):
    wholesalePriceList: WholesalePriceList


class Payments(BaseModel):
    invoice: str


class Price(BaseModel):
    amount: str
    currency: str


class SellingMode(BaseModel):
    format: str
    price: Price
    minimalPrice: Price
    startingPrice: Price


class Location(BaseModel):
    city: str
    countryCode: str
    postCode: str
    province: str


class DescriptionItem(BaseModel):
    type: str


class DescriptionSection(BaseModel):
    items: list[DescriptionItem] = []


class Description(BaseModel):
    sections: list[DescriptionSection] = []


class External(BaseModel):
    id: str


class TaxRate(BaseModel):
    rate: str
    countryCode: str


class TaxSettings(BaseModel):
    rates: list[TaxRate]
    subject: str
    exemption: str


class MessageToSellerSettings(BaseModel):
    mode: str
    hint: str


class CreateProductOffer(BaseModel):
    productSet: list[ProductSetItem]
    b2b: B2B
    attachments: list[Attachment] = []
    fundraisingCampaign: FundraisingCampaign
    additionalServices: AdditionalServices
    stock: Stock
    delivery: Delivery
    publication: Publication
    additionalMarketplaces: AdditionalMarketplaces
    compatibilityList: CompatibilityList
    language: str
    category: Category
    parameters: list[Parameter] = []
    afterSalesServices: AfterSalesServices
    sizeTable: SizeTable
    contact: Contact
    discounts: Discounts
    name: str
    payments: Payments
    sellingMode: SellingMode
    location: Location
    images: list[str] = []
    description: Description
    external: External
    taxSettings: TaxSettings
    messageToSellerSettings: MessageToSellerSettings


class AllegroClient:

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
        base_api_url: str,
        translator: Translator,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.base_api_url = base_api_url
        self.translator: Translator = translator
        self.access_token = None
        self.token_expiry = 0

    def _get_auth_headers(self) -> dict:
        auth = b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        return {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _get_pass_data(self) -> dict:
        return {"grant_type": "client_credentials"}

    def _ensure_token(self):
        if self.access_token is None or time.time() > self.token_expiry:
            self._get_access_token()

    def _get_access_token(self):
        url = f"{self.base_url}/auth/oauth/token"
        response: Response = httpx.post(
            url=url,
            headers=self._get_auth_headers(),
            data=self._get_pass_data(),
        )
        token_data: dict = response.json()
        try:
            access_token: str = token_data.get("access_token")
            token_expiry: float = token_data.get("expires_in")
        except (KeyError, TypeError) as e:
            raise Exception  # TODO

        self.access_token = access_token
        self.token_expiry = token_expiry

    def _get_api_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.allegro.public.v1+json",
        }

    def resolve_category_id(
        self,
        car_part_name: str,
    ):
        with open(
            file="app/apis/allegro/JSON/allegro_car_part_group.json",
            mode="r",
            encoding="UTF-8",
        ) as file:
            car_parts_allegro: dict = json.load(file)
        allegro_category_id: str | None = car_parts_allegro.get(car_part_name)

        if not allegro_category_id:
            return "0"

        return allegro_category_id

    async def get_categories(self, parent_id: str | None = None) -> dict:
        self._ensure_token()
        url = f"{self.base_api_url}/sale/categories"
        if parent_id:
            url += f"?parent.id={parent_id}"

        async with AsyncClient() as client:
            response = await client.get(url, headers=self._get_api_headers())
            return response.json()

    async def create_product(
        self,
        orm_product: ORMProduct,
    ):
        car_brand_name = orm_product.car_brand.name
        car_series_name = orm_product.car_series.name
        car_part_name = orm_product.car_part.name
        product_article = orm_product.article
        product_images = []
        if orm_product.pictures:
            for picture in orm_product.pictures:
                product_images.append(picture)

        # if orm_product.idriver_pictures:
        #   for picture in orm_product.idriver_pictures:
        #       product_images.append(picture)
        #
        now = datetime.now(tz=timezone("Europe/Warsaw"))

        product_name_rus = car_part_name + car_brand_name + car_series_name
        product_category_id = self.resolve_category_id(car_part_name=car_part_name)
        product_name_pl = await self.translator.translate_text(
            text=product_name_rus,
            target_lang="PL",
        )

        product = Product(
            name=product_name_pl,
            category=Category(id=product_category_id),
            id=product_article,
            idType="SELLER_SKU",
            parameters=[],  # можешь потом передать список
            images=["https://example.com/image1.jpg"],
        )

        # Кол-во
        quantity = Quantity(value=1)

        # Ответственное лицо
        responsible_person = ResponsiblePerson(
            id="person_001",
            name="ООО АвтоПлюс",
        )

        # Производитель / Импортер
        responsible_producer = ResponsibleProducer(
            type="importer",
            id="manufacturer_001",
        )

        # Информация по безопасности
        safety_info = SafetyInformation(
            type="none",
            description="",
        )

        # Один элемент productSet
        product_item = ProductSetItem(
            product=product,
            quantity=quantity,
            responsiblePerson=responsible_person,
            responsibleProducer=responsible_producer,
            safetyInformation=safety_info,
            marketedBeforeGPSRObligation=False,
        )

        offer_data = CreateProductOffer(
            productSet=[product_item],
            b2b=B2B(buyableOnlyByBusiness=False),
            attachments=[],
            fundraisingCampaign=FundraisingCampaign(id="fund_001", name=""),
            additionalServices=AdditionalServices(id="svc_001", name=""),
            stock=Stock(available=10, unit="unit"),
            delivery=Delivery(
                handlingTime="PT24H",
                shippingRates=None,
                additionalInfo="Доставка в течение суток",
                shipmentDate=datetime.utcnow(),
            ),
            publication=Publication(
                duration="PT720H",
                startingAt=datetime.utcnow(),
                status="INACTIVE",
                republish=False,
            ),
            additionalMarketplaces=AdditionalMarketplaces(allegro_cz={}),
            compatibilityList=CompatibilityList(items=[]),
            language="PL",
            category=Category(id="4094"),
            parameters=[],
            afterSalesServices=AfterSalesServices(
                impliedWarranty=AfterSalesItem(
                    id="warranty_001", name="Implied warranty"
                ),
                returnPolicy=AfterSalesItem(id="return_001", name="Return policy"),
                warranty=AfterSalesItem(id="extra_001", name="Extended warranty"),
            ),
            sizeTable=SizeTable(id="size_001", name="Размерная таблица"),
            contact=Contact(id="contact_001", name="Контактное лицо"),
            discounts=Discounts(
                wholesalePriceList=WholesalePriceList(id="wh_001", name="Оптом")
            ),
            name="Фара левая VW Passat B6",
            payments=Payments(invoice="VAT"),
            sellingMode=SellingMode(
                format="BUY_NOW",
                price=Price(amount="399.99", currency="PLN"),
                minimalPrice=Price(amount="0", currency="PLN"),
                startingPrice=Price(amount="0", currency="PLN"),
            ),
            location=Location(
                city="Warszawa",
                countryCode="PL",
                postCode="00-001",
                province="MAZOWIECKIE",
            ),
            images=["https://example.com/image1.jpg"],
            description=Description(
                sections=[DescriptionSection(items=[DescriptionItem(type="TEXT")])]
            ),
            external=External(id="SKU-12345"),
            taxSettings=TaxSettings(
                rates=[TaxRate(rate="23", countryCode="PL")],
                subject="VAT",
                exemption="",
            ),
            messageToSellerSettings=MessageToSellerSettings(
                mode="ENABLED", hint="Можете уточнить совместимость"
            ),
        )

        return offer_data


async def main():

    asd = AllegroClient(
        client_id="фыв",
        client_secret="фывфывфыв",
        base_url="https://allegro.pl",
        base_api_url="https://api.allegro.pl",
    )

    print(asd.resolve_category_id(car_part_name="Пневмостойка"))


asyncio.run(main=main())
