from typing import Any

import numpy as np
from PIL import Image
from fastapi import UploadFile
from numpy import ndarray, dtype, generic


def prepare_input_tensor(image_file: UploadFile) -> ndarray[Any, dtype[generic | Any]]:
    image = Image.open(image_file.file).convert("RGB")

    image_array = np.array(image)

    return np.expand_dims(image_array, axis=0)

class PredictionService:
    def __init__(self, binary_model, multiclass_model):
        self.binary_model = binary_model
        self.multiclass_model = multiclass_model

    def predict_binary(self, image_file: UploadFile) -> list[float]:

        try:
            input_tensor = prepare_input_tensor(image_file)

            prediction = self.binary_model.predict(input_tensor)

            return prediction

        except Exception as e:
            raise Exception(f"Error when predicting with binary classifier {str(e)}")


    def predict_multiclass(self, image: UploadFile) -> list[float]:
        try:
            input_tensor = prepare_input_tensor(image)

            prediction = self.multiclass_model.predict(input_tensor)

            return prediction

        except Exception as e:
            raise Exception(f"Error when predicting with multiclass classifier {str(e)}")