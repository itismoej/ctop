FROM python:3.9-slim

WORKDIR /app

COPY requirements.lock .
RUN sed '/-e/d' requirements.lock > requirements.txt && rm requirements.lock
RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT ["python", "-m", "quantcast_cli"]
