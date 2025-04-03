# Reference: https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/python3.8.dockerfile
FROM python:3.12-slim-bullseye

WORKDIR /code

# Install build essentials in order to install gcc
RUN apt update && apt install build-essential -y

# Update pip to get the latest dependency-resolver.
RUN pip install --no-cache-dir -U pip

COPY ./requirements.txt .
COPY ./setup.py .
COPY ./app ./app

RUN pip install --no-cache-dir -e .



# Start with Uvicorn
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4" ]
