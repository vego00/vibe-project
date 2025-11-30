import asyncio

def async_retry(retries=3, delay=1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        raise
                    await asyncio.sleep(delay)
        return wrapper
    return decorator
