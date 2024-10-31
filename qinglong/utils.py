import logging
from qinglong.notify import send

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
