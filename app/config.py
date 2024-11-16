import logging


class Settings:
    db = {
        "url": "sqlite:///sample-data/sample-data.db",
        "connect_args": {"check_same_thread": False},
    }

    logging = {
        "encoding": "utf-8",
        "level": logging.DEBUG,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    }


settings = Settings()
