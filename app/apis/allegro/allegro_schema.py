from pydantic import BaseModel, Field
from datetime import datetime


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
