import logging
logger = logging.getLogger(__name__)

def execute_with_retry(retry_times=3, fn, *args, **kwargs):
    for count in range(0, retry_times):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error("Get exception when executing fn {}, try again - {}".format(fn.__name__, count))
            logger.error(e)
