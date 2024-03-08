LOGGING_FORMAT_DEFAULT: str = '%(levelname)-9s [%(correlation_id)s] [%(app_name)s] %(asctime)s - %(message)s'  # NOQA
LOGGING_FORMAT_ACCESS: str = '%(levelname)-9s [%(correlation_id)s] [%(app_name)s] %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s'  # NOQA
LOGGING_LEVEL: str = "DEBUG"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {
            "()": "utils.middleware.CorrelationIdFilter"
        }
    },
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOGGING_FORMAT_DEFAULT
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": LOGGING_FORMAT_ACCESS
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": ["correlation_id"]
        },
        "error": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "filters": ["correlation_id"]
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": ["correlation_id"]
        }
    },
    "loggers": {
        "": {
            "level": LOGGING_LEVEL,
            "handlers": ["default"],
            "propagate": False
        },
        "uvicorn.error": {
            "level": LOGGING_LEVEL,
            "handlers": ["error"],
            "propagate": False
        },
        "uvicorn.access": {
            "level": LOGGING_LEVEL,
            "handlers": ["access"],
            "propagate": False
        }
    }
}
