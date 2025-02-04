import io
from unittest.mock import Mock, patch

import pytest
from PIL import Image
from fastapi import UploadFile

from app.prediction_service import PredictionService


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

@pytest.fixture
def prediction_service():
    with patch('app.prediction_service.binary_classifier_model', new=Mock()), \
            patch('app.prediction_service.multiclass_classifier_model', new=Mock()):
        yield PredictionService(
            binary_model=Mock(),
            multiclass_model=Mock()
        )