from fastapi import APIRouter, UploadFile, Depends

from app.classifier_models import binary_classifier_model, multiclass_classifier_model
from app.prediction_service import PredictionService

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"]
)

def get_prediction_service():
    return PredictionService(
        binary_model=binary_classifier_model,
        multiclass_model=multiclass_classifier_model
    )

@router.post("/binary")
async def predict_binary(
        image_file : UploadFile,
        prediction_service: PredictionService = Depends(get_prediction_service)
):
    return {"message": "Predicting binary"}