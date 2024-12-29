FROM python:3.14.0a3-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    && apt-get install -y curl \
    && pip3 install pipenv \
    && rm -rf /var/lib/apt/lists/*

COPY ./data/ /code/data

RUN mkdir -p /code/logs

COPY ./Pipfile ./Pipfile.lock /code/

RUN pipenv install --system --deploy 

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=1m --retries=1 --timeout=1s --start-period=5s \
  CMD curl --fail http://localhost:8000/info