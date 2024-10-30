import time
import functools
import logging
from notify import send

class QlLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 控制台处理器
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", 
                                    "%Y-%m-%d %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.name = name

    def info(self, message):
        self.logger.info(message)

    def error(self, message, notify=True):
        self.logger.error(message)
        if notify:
            send(self.name, message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

def retry_on_error(max_retries=3, retry_delay=120, error_types=(Exception,), error_message="操作失败"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = QlLogger(func.__name__)
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
                    logger.warning(f"尝试 {attempt + 1}/{max_retries} 失败: {str(e)}. {delay}秒后重试...")
                    time.sleep(delay)
            
            error_msg = f"{error_message}: {str(last_exception)}"
            logger.error(error_msg)
            return None
        return wrapper
    return decorator