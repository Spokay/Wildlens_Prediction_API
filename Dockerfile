FROM python:3.12.0-alpine

# Set the working directory
WORKDIR /app
# Copy the source code into the container
COPY ./app /app
# Copy the entrypoint script into the container
COPY ./entrypoint.sh /app/entrypoint.sh
# Copy the requirements file into the container
COPY requirements.txt .
# Install the dependencies

RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]

