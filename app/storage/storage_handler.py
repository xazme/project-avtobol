import io
import asyncio
import uuid
from typing import cast
from datetime import datetime
from contextlib import asynccontextmanager
from PIL import Image
from aiobotocore.session import get_session
from types_aiobotocore_s3 import S3Client as AioS3Client
from app.shared import ExceptionRaiser


class StorageHandler:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        try:
            async with self.session.create_client("s3", **self.config) as client:
                yield cast(AioS3Client, client)
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail=f"Ошибка подключения к хранилищу: {e}",
            )

    async def create_file(self, file: bytes) -> str:
        if not isinstance(file, bytes):
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Тип файла должен быть bytes, а не {type(file)}",
            )

        try:
            file_bytes = await self._convert_to_webp(file=file)
            filename = self._generate_name() + ".webp"

            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=filename,
                    Body=file_bytes,
                )
            return filename
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail=f"Не удалось создать файл: {e}",
            )

    async def delete_file(self, filename: str) -> None:
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=filename)
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Ошибка удаления файла '{filename}': {e}",
            )

    async def get_presigned_upload_url(
        self,
        filename: str,
        content_type: str,
        expiration: int = 300,
    ) -> str:
        try:
            async with self.get_client() as client:
                return await client.generate_presigned_url(
                    "put_object",
                    Params={
                        "Bucket": self.bucket_name,
                        "Key": filename,
                        "ContentType": content_type,
                    },
                    ExpiresIn=expiration,
                )
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail=f"Ошибка генерации ссылки: {e}",
            )

    async def create_files(self, list_of_files: list):
        try:
            tasks = [self.create_file(file) for file in list_of_files]
            return await asyncio.gather(*tasks, return_exceptions=False)
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail=f"Ошибка множественной загрузки: {e}",
            )

    async def delete_files(self, list_of_files: list):
        try:
            tasks = [self.delete_file(name) for name in list_of_files]
            await asyncio.gather(*tasks, return_exceptions=False)
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail=f"Ошибка множественного удаления: {e}",
            )

    async def get_file(self, filename: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=filename,
                )
                WHAT = response["Body"]
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail=f"Ошибка множественного удаления: {e}",
            )

    async def _convert_to_webp(self, file: bytes) -> bytes:
        try:
            with Image.open(io.BytesIO(file)) as img:
                output_buffer = io.BytesIO()
                img.save(output_buffer, format="WEBP", quality=80)
                return output_buffer.getvalue()
        except Exception as e:
            ExceptionRaiser.raise_exception(
                status_code=415,
                detail=f"Ошибка конвертации изображения: {e}",
            )

    @staticmethod
    def _generate_name() -> str:
        dt_str = datetime.now().strftime("%Y%m%d%H%M%S")
        uniq_str = str(int(uuid.uuid4()) >> 64)
        return dt_str + uniq_str
