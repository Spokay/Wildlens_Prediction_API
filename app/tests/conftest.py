import io

import pytest
from PIL import Image
from fastapi import UploadFile


@pytest.fixture
def valid_image_file():
    # Create an in-memory image
    img = Image.new("RGB", (100, 100), color="white")
    file_content = io.BytesIO()
    img.save(file_content, format="JPEG")
    file_content.seek(0)

    return UploadFile(filename="valid_image.jpg", file=file_content)

@pytest.fixture
def invalid_image_file():
    return UploadFile(filename="invalid_image.jpg", file=io.BytesIO("invalid_image".encode()))