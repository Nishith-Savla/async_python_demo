import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__}({args}, {kwargs}): Time taken: {end - start:0.2f} seconds")
        return result

    return wrapper


def async_timer(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__}({args}, {kwargs}): Time taken: {end - start:0.2f} seconds")
        return result

    return wrapper
