FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app/stratigraph
COPY stratigraph/*.py ./
WORKDIR /app
COPY stratigraph/api.py /app/main.py
