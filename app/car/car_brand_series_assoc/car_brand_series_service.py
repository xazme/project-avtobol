# from sqlalchemy import Select, Result
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
# from app.shared import CRUDGenerator
# from .car_brand_series_model import CarBrandPartSeriesAssoc


# class CarBrandSeriesService(CRUDGenerator):

#     def __init__(self, session: AsyncSession):
#         super().__init__(
#             session=session,
#             model=CarBrandPartSeriesAssoc,
#         )

#     async def get_all(self):
#         stmt = Select(self.model).options(  # TODO
#             selectinload(self.model.brand),
#             selectinload(self.model.part),
#             selectinload(self.model.series),
#         )
#         result: Result = await self.session.execute(statement=stmt)
#         return result.scalars().all()

#     async def get_part_by_id(self, id: int):
#         stmt = (
#             Select(self.model)
#             .where(self.model.id == id)
#             .options(
#                 selectinload(self.model.brand),
#                 selectinload(self.model.series),
#                 selectinload(self.model.car_part),
#             )
#         )

#         result: Result = self.session.execute(statement=stmt)
#         return result.scalar_one_or_none()
