from pydantic import BaseModel


class BinaryClassifierPredictionResponse(BaseModel):
    predictions: list[float]

class MulticlassClassifierPredictionResponse(BaseModel):
    predictions: list[float]
