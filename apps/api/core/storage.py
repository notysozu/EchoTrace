import boto3
from botocore.exceptions import ClientError
from core.config import get_settings

settings = get_settings()

_s3_client = None


def get_s3():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
    return _s3_client


def generate_presigned_url(s3_key: str, expires_in: int = 3600) -> str:
    """Generate a pre-signed S3 URL valid for `expires_in` seconds."""
    s3 = get_s3()
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket_name, "Key": s3_key},
            ExpiresIn=expires_in,
        )
        return url
    except ClientError as e:
        raise RuntimeError(f"Failed to generate presigned URL: {e}")


def upload_audio(s3_key: str, file_bytes: bytes, content_type: str = "audio/mpeg") -> str:
    """Upload audio bytes to S3. Returns the S3 key."""
    s3 = get_s3()
    s3.put_object(
        Bucket=settings.s3_bucket_name,
        Key=s3_key,
        Body=file_bytes,
        ContentType=content_type,
        CacheControl="max-age=31536000",  # CDN cache 1 year
    )
    return s3_key


def cdn_url(s3_key: str) -> str:
    """Convert S3 key to CloudFront CDN URL for public assets."""
    return f"{settings.cloudfront_domain}/{s3_key}"
