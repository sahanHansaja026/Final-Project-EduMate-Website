import boto3
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

AWS_BUCKET = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

s3 = boto3.client("s3")


def upload_file(file, folder: str):
    ext = file.filename.split(".")[-1]
    key = f"{folder}/{uuid.uuid4()}.{ext}"

    s3.upload_fileobj(
        file.file,
        AWS_BUCKET,
        key,
        ExtraArgs={"ContentType": file.content_type}
    )

    return f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"


def delete_file(file_url: str):
    try:
        key = file_url.split(".amazonaws.com/")[1]
        s3.delete_object(Bucket=AWS_BUCKET, Key=key)
    except Exception as e:
        print("S3 delete error:", e)