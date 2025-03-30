FROM python:3.12.0-slim

WORKDIR /api


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install fastapi[standard]


COPY app /api/app

COPY cnn_models /api/cnn_models


ENV PYTHONPATH="/api"

EXPOSE 5001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]