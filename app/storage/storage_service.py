import asyncio
import uuid
from typing import cast
from datetime import datetime
from contextlib import asynccontextmanager
import logging

from fastapi import UploadFile

# from starlette.datastructures import UploadFile
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

    # @s3_error_handler
    # async def clear_bucket(self):
    #     async with self.get_client() as client:
    #         await client.

    @s3_error_handler
    async def create_file(self, file: UploadFile | bytes) -> str:
        async with self.get_client() as client:
            if hasattr(file, "read"):
                file_bytes = await file.read()
            elif type(file) == bytes:
                file_bytes = file
            else:
                raise TypeError(
                    f"Arg 'file' must be a UploadFile type or bytes, not {type(file)}"
                )
            filename = self._generate_name()
            await client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_bytes,
            )
            logger.info(f"File '{filename}' deleted.")
            return filename

    @s3_error_handler
    async def delete_file(self, filename: str):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=filename)
            logger.info(f"File '{filename}' deleted.")

    @s3_error_handler
    async def file_exists(self, filename: str) -> bool:
        async with self.get_client() as client:
            await client.get_object(Bucket=self.bucket_name, Key=filename)
            logger.info(f"File '{filename}' was found.")
            return True

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

    @staticmethod
    def _generate_name() -> str:
        dt_str = datetime.now().strftime("%Y%m%d%H%M%S")
        uniq_str = str(int(uuid.uuid4()) >> 64)
        return dt_str + uniq_str
