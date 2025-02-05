from functools import lru_cache

from fastapi import APIRouter, UploadFile, Depends
from starlette import status

from app.classifier_models import binary_classifier_model, multiclass_classifier_model
from app.dto.prediction import BinaryClassifierPredictionResponse, MulticlassClassifierPredictionResponse
from app.mappers.prediction_mapper import binary_predictions_to_response
from app.services.prediction_service import PredictionService

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

    predictions = await prediction_service.predict_multiclass(image_file)

    return MulticlassClassifierPredictionResponse(predictions=predictions)



