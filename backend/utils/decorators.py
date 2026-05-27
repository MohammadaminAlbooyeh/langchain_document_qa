import time
import functools
from backend.utils.logger import get_logger

logger = get_logger()


def timing_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def log_call(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__}")
        result = await func(*args, **kwargs)
        logger.debug(f"{func.__name__} completed")
        return result
    return wrapper
