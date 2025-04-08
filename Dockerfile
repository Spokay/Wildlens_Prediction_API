FROM python:3.12.0-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install fastapi[standard]


COPY ./app /app/app

COPY ./entrypoint.sh /app/entrypoint.sh

VOLUME /app/prediction_models

EXPOSE 5002

ENV FALLBACK_PORT=5002

ENTRYPOINT ["/app/entrypoint.sh"]