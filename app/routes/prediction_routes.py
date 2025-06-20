from functools import lru_cache

from fastapi import APIRouter, UploadFile, Depends, WebSocket
from starlette import status
import base64
from io import BytesIO
import numpy as np
from app.classifier_models import binary_classifier_model, multiclass_classifier_model
from app.config import get_settings
from app.dto.prediction import BinaryClassifierPredictionResponse, MulticlassClassifierPredictionResponse
from app.mappers.prediction_mapper import binary_predictions_to_response
from app.services.prediction_service import PredictionService
from dotenv import load_dotenv
import os

load_dotenv()

settings = get_settings()

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"]
)

@lru_cache()
def get_prediction_service():
    return PredictionService(
        binary_model=binary_classifier_model,
        multiclass_model=multiclass_classifier_model
    )

@router.post(
    "/binary",
    response_model=BinaryClassifierPredictionResponse,
    description="Predicts the class of an image using a binary classifier",
    status_code=status.HTTP_200_OK,
)
async def predict_binary(
        image_file : UploadFile,
        prediction_service: PredictionService = Depends(get_prediction_service)
) -> BinaryClassifierPredictionResponse:

    predictions = await prediction_service.predict_binary(image_file)

    prediction_response = await binary_predictions_to_response(predictions)

    return prediction_response


@router.websocket("/ws")
async def socket_binary(websocket: WebSocket):
    await websocket.accept()
    try:
        auth_header = websocket.headers.get("Authorization")
        if not auth_header or auth_header != "Key " + settings.wildlens_prediction_api_key:
            await websocket.send_json({
                "error": "Invalid API Key"
            })
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        prediction_service = get_prediction_service()
        while True:
            file = await websocket.receive_json()
            filename = file.get("filename")
            data = file.get("data")
            if filename and data:
                image_data = base64.b64decode(data)
                image_file = UploadFile(
                    filename=filename,
                    file=BytesIO(image_data)
                )

                predictions = await prediction_service.predict_binary(image_file)
                await websocket.send_json({
                    "predictions": predictions,
                })
            else:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    except Exception as e:
        await websocket.close(code=1008)
        return
    
    



@router.post(
    "/multiclass",
    response_model=MulticlassClassifierPredictionResponse,
    description="Predicts the class of an image using a multiclass classifier",
    status_code=status.HTTP_200_OK,
)
async def predict_multiclass(
        image_file : UploadFile,
        prediction_service: PredictionService = Depends(get_prediction_service)
) -> MulticlassClassifierPredictionResponse:

    num_classes = 13
    random_values = np.random.random(num_classes)
    normalized_predictions = (random_values / random_values.sum()).tolist()

    return MulticlassClassifierPredictionResponse(
        # TODO : when the MultiClassClassifier is implemented, replace the following predictions with the actual predictions
        predictions=normalized_predictions
    )



