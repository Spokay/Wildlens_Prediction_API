from app.dto.prediction import BinaryClassifierPredictionResponse, \
    MulticlassClassifierPredictionResponse


async def binary_predictions_to_response(predictions: list[float]):
    return BinaryClassifierPredictionResponse(predictions=predictions)


async def multiclass_predictions_to_response(predictions: list[float]):
    return MulticlassClassifierPredictionResponse(predictions=predictions)