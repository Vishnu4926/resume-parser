from datetime import timedelta
from google.cloud import storage

from google.cloud import storage

from config.settings import BUCKET_NAME

client = storage.Client()

bucket = client.bucket(BUCKET_NAME)


def upload_resume(
    file_bytes,
    filename
):

    blob = bucket.blob(
        f"resumes/{filename}"
    )

    blob.upload_from_string(
        file_bytes,
        content_type="application/pdf"
    )

    return blob.public_url

def generate_signed_url(filename):

    blob = bucket.blob(
        f"resumes/{filename}"
    )

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="GET"
    )

    return url
