import json
import logging

from botocore.exceptions import ClientError
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    """S3/MinIO media storage that creates the local bucket when it is missing."""

    def _save(self, name, content):
        self.ensure_bucket()
        return super()._save(name, content)

    def ensure_bucket(self) -> None:
        if not settings.DEBUG or not settings.AWS_S3_ENDPOINT_URL:
            return

        client = self.connection.meta.client
        bucket = self.bucket_name
        try:
            client.head_bucket(Bucket=bucket)
            return
        except ClientError as exc:
            code = str(exc.response.get("Error", {}).get("Code", ""))
            if code not in {"404", "NoSuchBucket", "404 Not Found"}:
                raise

        client.create_bucket(Bucket=bucket)
        client.put_bucket_policy(
            Bucket=bucket,
            Policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "AllowPublicRead",
                            "Effect": "Allow",
                            "Principal": {"AWS": ["*"]},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{bucket}/*"],
                        }
                    ],
                }
            ),
        )
        logger.info("Created local media bucket %s", bucket)
