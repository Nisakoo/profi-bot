import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base_formatter": {
            "format": "%(asctime)s %(levelname)s %(message)s",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "base_formatter",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "profi_bot.log",
            "formatter": "base_formatter"
        }
    },
    "loggers": {
        "": {"handlers": ["file"], "level": "DEBUG"}},
}

logging.config.dictConfig(LOGGING_CONFIG)