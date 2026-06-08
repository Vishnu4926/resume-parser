from services.storage_service import upload_resume

with open(
    "uploads/Resume_BN.pdf",
    "rb"
) as f:

    file_bytes = f.read()

url = upload_resume(
    file_bytes,
    "test_resume.pdf"
)

print(url)
