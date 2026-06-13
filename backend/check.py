from services.s3_service import upload_file, delete_file
from fastapi import UploadFile
import io


# -------------------------
# CREATE FAKE FILE (TEST)
# -------------------------
class FakeUploadFile:
    def __init__(self, filename, content, content_type="application/pdf"):
        self.filename = filename
        self.file = io.BytesIO(content)
        self.content_type = content_type


def test_upload_and_delete():
    print("🚀 Starting S3 test...")

    # fake file (simulating PDF)
    file_content = b"This is a test file for S3 upload"
    file = FakeUploadFile("test.pdf", file_content)

    # -------------------------
    # UPLOAD TEST
    # -------------------------
    url = upload_file(file, "test-folder")

    print("✅ Upload successful!")
    print("File URL:", url)

    # -------------------------
    # DELETE TEST
    # -------------------------
    delete_file(url)

    print("🗑️ Delete request sent!")
    print("✅ Test completed")


if __name__ == "__main__":
    test_upload_and_delete()