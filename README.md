[![Build and Test](https://github.com/breakingmews/codecrafters-bittorrent-python/actions/workflows/ci.yml/badge.svg)](https://github.com/breakingmews/codecrafters-bittorrent-python/actions/workflows/ci.yml)


# Measurements API

This project provides an API for managing and retrieving measurements.

This project was created as part of a coding challenge. The content has been anonymized to respect confidentiality.

## Getting Started

### Prerequisites

- Python 3.13
- Pipenv
- Docker (optional, for running in a container)

### Installation

Install dependencies using Pipenv:
```sh
pipenv install
```

### Running the Server

#### Development

To run  the server in development mode, includes `--reload` option:

```sh
pipenv run start
```
The server is running by default on http://0.0.0.0:8000/docs.

#### Production:
```sh
pipenv run serve
```

#### Run in Docker

```sh
docker build -t measurements-api .
docker run -d \
  --name measurements-api \
  -p 8000:8000 \
  --mount type=bind,source="$(pwd)"/logs,target=/code/logs \
  measurements-api
```

#### Run with Docker Compose

Build and start the services:
```sh
docker-compose up --build
```

### Logging
Logs are stored in the `/code/logs` directory inside the container. You can mount a host directory to this path to persist logs.

# TODOs

- improve pagination with fastapi-sqla
- add sorting to endpoint
- use alembic for datamigration

## Task 2
Implement the following API endpoints which use the model / database:

- /api/v1/measurements/ : Retrieve ( GET ) a list of measurements for a given
user_id , filter by start and stop timestamps (optional). This endpoint
should support pagination, sorting, and a way to limit the number of measurements returned.

