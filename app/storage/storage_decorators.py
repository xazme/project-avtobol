import functools
import logging
from typing import Callable
from botocore.exceptions import ClientError, BotoCoreError
from .storage_exceptions import (
    FileDeletionError,
    FileUploadError,
    BucketNotFoundError,
    S3ServiceError,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def s3_error_handler(func: Callable):

    @functools.wraps(func)
    async def wrapper(*arg, **kwargs):
        try:
            return await func(*arg, **kwargs)
        except ClientError as ce:
            error_code = ce.response.get("Error", {}).get("Code", "Unknown")
            error_message = ce.response.get("Error", {}).get("Message", "No message")
            logger.error(
                f"S3 ClientError in {func.__name__}: {error_code} - {error_message}",
                exc_info=True,
            )
            if error_code == "NoSuchBucket":
                raise BucketNotFoundError(f"Bucket not found: {error_message}") from ce
            elif func.__name__ == "create_file":
                raise FileUploadError(
                    f"File upload error: {error_code} - {error_message}"
                ) from ce

            elif func.__name__ == "delete_file":
                raise FileDeletionError(
                    f"File deletion error: {error_code} - {error_message}"
                ) from ce
            else:
                raise S3ServiceError(
                    f"S3 ClientError: {error_code} - {error_message}"
                ) from ce
        except BotoCoreError as bce:
            logger.error(f"S3 BotoCoreError in {func.__name__}: {bce}", exc_info=True)
            raise S3ServiceError(f"S3 BotoCoreError: {str(bce)}") from bce
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            raise

    return wrapper
