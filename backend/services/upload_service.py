import uuid



from backend.services.s3_service import AWS_BUCKET, s3


def upload_file_to_s3(file, folder: str):

    file_key = f"{folder}/{uuid.uuid4()}-{file.filename}"

    s3.upload_fileobj(
        file.file,
        AWS_BUCKET,
        file_key,
        ExtraArgs={"ContentType": file.content_type}
    )

    return f"https://{AWS_BUCKET}.s3.ap-south-1.amazonaws.com/{file_key}"
