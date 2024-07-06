FROM python:3.12

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

ENV PYHTONUNBUFFERED=1

RUN pip install --progress-bar off -r requirements.txt

COPY . .

WORKDIR .

# CMD gunicorn Fast_API:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
