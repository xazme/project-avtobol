class S3ServiceError(Exception):
    pass


class BucketNotFoundError(S3ServiceError):
    pass


class FileUploadError(S3ServiceError):
    pass


class FileDeletionError(S3ServiceError):
    pass
