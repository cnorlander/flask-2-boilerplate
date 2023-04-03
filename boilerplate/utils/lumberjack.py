import logging
from logging.handlers import RotatingFileHandler
import boilerplate.config as config
import os
import sys

# ==============================================================================================================================================================
#                                                                      Configuration
# ==============================================================================================================================================================

# Create the logging handler from values in config
log_handler = RotatingFileHandler(config.LOGGING_FILE, maxBytes=1000*config.LOGGING_MAX_SIZE_KB, backupCount=config.LOGGING_MAX_LOGS)

# Set the logging level for the log
log_level = logging.WARNING
if config.DEBUG_MODE or config.LOGGING_LEVEL == "DEBUG":
    log_level = logging.DEBUG
elif config.LOGGING_LEVEL == "INFO":
    log_level = logging.INFO
elif config.LOGGING_LEVEL == "ERROR":
    log_level = logging.ERROR
elif config.LOGGING_LEVEL == "CRITICAL":
    log_level = logging.CRITICAL
log_handler.setLevel(log_level)

# Create the logging format and initialize the handler
pid = os.getpid()
formatter = logging.Formatter(f'%(asctime)s - PID:{pid} - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger = logging.getLogger('main_logger')
logger.setLevel(log_level)
logger.addHandler(log_handler)

# Log workers as they boot.
logger.info(f'Booting Worker')

# ==============================================================================================================================================================
#                                                                       Functions
# ==============================================================================================================================================================

def debug(message: str, traceback=None, silence_cli=False):
    log_out = message
    if traceback:
        log_out += f'\r\n{traceback}'
    logger.debug(log_out)
    if not silence_cli and config.DEBUG_MODE or config.LOGGING_LEVEL == "DEBUG":
        print(message, flush=True)


def info(message: str, traceback=None, silence_cli=False):
    log_out = message
    if traceback:
        log_out += f'\r\n{traceback}'
    logger.info(log_out)
    if not silence_cli and config.LOGGING_LEVEL in ["DEBUG", "INFO"]:
        print(message, flush=True)


def warning(message: str, traceback=None, silence_cli=False):
    log_out = message
    if traceback:
        log_out += f'\r\n{traceback}'
    logger.warning(log_out)
    if not silence_cli and config.LOGGING_LEVEL in ["DEBUG", "INFO", "WARNING"]:
        print(message, flush=True, file=sys.stderr)


def error(message: str, traceback=None, silence_cli=False):
    log_out = message
    if traceback:
        log_out += f'\r\n{traceback}'
    logger.error(log_out)
    if not silence_cli and config.LOGGING_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        print(message, flush=True, file=sys.stderr)


def critical(message: str, traceback=None, silence_cli=False):
    log_out = message
    if traceback:
        log_out += f'\r\n{traceback}'
    logger.critical(log_out)
    if not silence_cli:
        print(message, flush=True, file=sys.stderr)

