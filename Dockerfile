FROM python:3.13-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    && pip3 install pipenv \
    && rm -rf /var/lib/apt/lists/*

COPY ./data/ /code/data

RUN mkdir -p /code/logs

COPY ./Pipfile ./Pipfile.lock /code/

RUN pipenv install --system --deploy 

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]