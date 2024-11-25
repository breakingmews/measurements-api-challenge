class Settings:
    sample_data_dir = "data"

    db = {
        "url": f"sqlite:///{sample_data_dir}/sample.db",
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
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "detailed",
                "level": "DEBUG",
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
                "filename": "logs/log",
                "formatter": "standard",
                "level": "INFO",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": "DEBUG",
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "watchfiles.main": {
                "handlers": ["console"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }


settings = Settings()
