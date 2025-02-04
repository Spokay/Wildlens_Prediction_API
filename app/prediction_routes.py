from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"]
)


@router.post("/binary")
async def predict_binary(image_file : UploadFile):
    return {"message": "Predicting binary"}