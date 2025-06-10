import io
import asyncio
import uuid
import logging
from typing import cast
from datetime import datetime
from contextlib import asynccontextmanager
from PIL import Image
from aiobotocore.session import get_session
from types_aiobotocore_s3 import S3Client as AioS3Client
from .storage_decorators import s3_error_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StorageService:
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
        async with self.session.create_client("s3", **self.config) as client:
            yield cast(AioS3Client, client)

    @s3_error_handler
    async def create_bucket(self):
        async with self.get_client() as client:
            await client.create_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket '{self.bucket_name}' created.")

    @s3_error_handler
    async def delete_bucket(self):
        async with self.get_client() as client:
            await client.delete_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket '{self.bucket_name}' deleted.")

    @s3_error_handler
    async def create_file(self, file: bytes) -> str:
        async with self.get_client() as client:
            if not isinstance(file, bytes):
                raise TypeError(f"file must be bytes not {type(bytes)}")
            file_bytes = await self._convert_to_webp(file=file)
            filename = self._generate_name() + ".webp"
            await client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_bytes,
            )
            logger.info(f"File '{filename}' deleted.")
            return filename

    @s3_error_handler
    async def delete_file(self, filename: str) -> None:
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=filename)
            logger.info(f"File '{filename}' deleted.")

    @s3_error_handler
    async def file_exists(self, filename: str) -> bool:
        async with self.get_client() as client:
            try:
                await client.get_object(Bucket=self.bucket_name, Key=filename)
                logger.info(f"File '{filename}' was found.")
            except Exception as e:
                return None
            return True

    @s3_error_handler
    async def get_presigned_upload_url(
        self, filename: str, content_type: str, expiration: int = 300
    ) -> str:
        async with self.get_client() as client:
            presigned_url = await client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": filename,
                    "ContentType": content_type,
                },
                ExpiresIn=expiration,
            )
            logger.info(
                f"Generated presigned upload URL for '{filename}': {presigned_url}"
            )
            return presigned_url

    @s3_error_handler
    async def create_files(self, list_of_files: list):
        tasks = [self.create_file(file=file) for file in list_of_files]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        logger.info("All files uploaded")
        return results

    @s3_error_handler
    async def delete_files(self, list_of_files: list):
        tasks = [self.delete_file(filename) for filename in list_of_files]
        await asyncio.gather(*tasks, return_exceptions=False)
        logger.info("All files deleted")

    async def _convert_to_webp(self, file: bytes) -> bytes:
        with Image.open(io.BytesIO(file)) as img:
            output_buffer = io.BytesIO()
            img.save(output_buffer, format="WEBP", quality=80)
            return output_buffer.getvalue()

    @staticmethod
    def _generate_name() -> str:
        dt_str = datetime.now().strftime("%Y%m%d%H%M%S")
        uniq_str = str(int(uuid.uuid4()) >> 64)
        return dt_str + uniq_str
