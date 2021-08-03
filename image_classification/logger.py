import logging

LOG_FORMAT = '{asctime} [{levelname}] [{filename}:{lineno}] {message}'

logger = logging.getLogger('Image Classification')
formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', style='{')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
