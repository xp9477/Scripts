import time
import functools
from notify import send

def retry_on_error(max_retries=3, retry_delay=120, error_types=(Exception,), error_message="操作失败"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    response = func(*args, **kwargs)
                    if hasattr(response, 'raise_for_status'):
                        response.raise_for_status()
                    return response
                except error_types as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        break
                    delay = retry_delay * (2 ** attempt)  # 指数退避
                    print(f"尝试 {attempt + 1}/{max_retries} 失败: {str(e)}. {delay}秒后重试...")
                    time.sleep(delay)
            
            error_msg = f"{error_message}: {str(last_exception)}"
            print(error_msg)
            send(func.__name__, error_msg)
            return None
        return wrapper
    return decorator