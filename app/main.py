import os

from dotenv import load_dotenv

load_dotenv()

import uvicorn
from fastapi import FastAPI
from prediction_routes import router

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    port = os.getenv("WILDLENS_PREDICTION_API_PORT")
    if port is None:
        port = 5000
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
