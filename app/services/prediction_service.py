from typing import Any

import numpy as np
from PIL import Image
from fastapi import UploadFile
from numpy import ndarray, dtype, generic


def renormalize_probabilities(probs, num_classes_to_keep=13):
    kept_probs = probs[..., :num_classes_to_keep]

    # Renormalize so they sum to 1
    renormalized_probs = kept_probs / np.sum(kept_probs, axis=-1, keepdims=True)

    return renormalized_probs

def prepare_input_tensor(image_file: UploadFile, resize: tuple[int, int] = None) -> ndarray[Any, dtype[generic | Any]]:
    # If image is bytes convert to PIL image

    image = Image.open(image_file.file).convert("RGB")
    if resize:
        image = image.resize((224, 224), Image.Resampling.BILINEAR)
    image_array = np.array(image)

    return np.expand_dims(image_array, axis=0)

class PredictionService:
    def __init__(self, binary_model, multiclass_model):
        self.binary_model = binary_model
        self.multiclass_model = multiclass_model

    async def predict_binary(self, image_file: UploadFile) -> list[float]:

        try:
            input_tensor = prepare_input_tensor(image_file)

            prediction = self.binary_model.predict(input_tensor)

            return prediction

        except Exception as e:
            raise Exception(f"Error when predicting with binary classifier {str(e)}")


    async def predict_multiclass(self, image: UploadFile) -> list[float]:
        try:
            input_tensor = prepare_input_tensor(image, resize=(224, 224))

            prediction = self.multiclass_model.predict(input_tensor)

            renormalized_probs = renormalize_probabilities(prediction[0])

            return renormalized_probs.tolist()

        except Exception as e:
            raise Exception(f"Error when predicting with multiclass classifier {str(e)}")