from datetime import timedelta

from google.cloud import storage

from config.settings import (
    BUCKET_NAME
)

from utils.logger import logger


def get_bucket():

    client = storage.Client()

    return client.bucket(
        BUCKET_NAME
    )


def upload_resume(
    file_bytes,
    filename
):

    logger.info(
        f"Uploading resume {filename}"
    )

    bucket = get_bucket()

    blob = bucket.blob(
        f"resumes/{filename}"
    )

    blob.upload_from_string(
        file_bytes,
        content_type="application/pdf"
    )

    return blob.public_url


def generate_signed_url(
    filename
):

    bucket = get_bucket()

    blob = bucket.blob(
        f"resumes/{filename}"
    )

    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(
            minutes=15
        ),
        method="GET"
    )
