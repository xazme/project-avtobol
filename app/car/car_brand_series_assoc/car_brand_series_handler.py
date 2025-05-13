from app.shared import BaseHandler
from .car_brand_series_repository import CarBrandSeriesRepository


class CarBrandSeriesHandler(BaseHandler):
    def __init__(self, repository):
        super().__init__(repository)
