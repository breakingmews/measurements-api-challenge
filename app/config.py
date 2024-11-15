import logging


class Settings:
    logging = {
        "encoding": "utf-8",
        "level": logging.DEBUG,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    }


settings = Settings()
