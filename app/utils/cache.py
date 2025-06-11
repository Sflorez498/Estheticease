from functools import wraps
from datetime import datetime, timedelta
import json
from typing import Callable, Any

cache = {}

def cache_response(ttl: int = 300):  # 5 minutes by default
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Create cache key based on function name and arguments
            key = json.dumps({
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs
            })
            
            # Check if result is in cache
            if key in cache:
                cached_data = cache[key]
                if cached_data["expires"] > datetime.now():
                    return cached_data["result"]
                else:
                    # Remove expired cache
                    del cache[key]
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache[key] = {
                "result": result,
                "expires": datetime.now() + timedelta(seconds=ttl)
            }
            return result
        
        return wrapper
    return decorator
