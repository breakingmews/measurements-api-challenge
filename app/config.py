class Settings:
    db = {
        "url": "sqlite:///sample-data/sample-data.db",
        "connect_args": {"check_same_thread": False},
    }

    logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "detailed": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
            "simple": {
                "format": "%(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "detailed",
                "level": "DEBUG",
            },
            "file_info": {
                "class": "logging.FileHandler",
                "filename": "logs/info.log",
                "formatter": "standard",
                "level": "INFO",
            },
            "file_debug": {
                "class": "logging.FileHandler",
                "filename": "logs/debug.log",
                "formatter": "detailed",
                "level": "DEBUG",
            },
            "file_error": {
                "class": "logging.FileHandler",
                "filename": "logs/error.log",
                "formatter": "detailed",
                "level": "ERROR",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file_debug"],
                "level": "DEBUG",
            },
            "uvicorn": {
                "handlers": ["console", "file_debug"],
                "level": "INFO",
                "propagate": False,
            },
            "watchfiles.main": {
                "handlers": ["console", "file_error"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }


settings = Settings()
