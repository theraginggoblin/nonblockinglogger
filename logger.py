from abc import ABC, abstractmethod
import atexit
import threading
import queue
#import sys

EXIT_MESSAGE = "EXIT"

class LoggerBase(ABC):
    @abstractmethod
    def _process_message(message):
        pass

    @abstractmethod
    def _process_queue(self):
        pass

    @abstractmethod
    def start_logger(self):
        pass

    @abstractmethod
    def stop_logger(self):
        pass

    @abstractmethod
    def log_message(self, message):
        pass

class ThreadLogger(LoggerBase):
    def __init__(self):
        self._queue = queue.Queue(maxsize=100)
        self._thread = None

    def _process_message(self, message):
        print(message)

    def _process_queue(self):
        while True:
            message = self._queue.get()
            if message:
                if message == EXIT_MESSAGE:
                    break
                self._process_message(message)

    def start_logger(self):
        self._thread = threading.Thread(target=self._process_queue, daemon=True)
        self._thread.start()

    def stop_logger(self):
        self._queue.put(EXIT_MESSAGE)
        self._thread.join()

    def log_message(self, message):
        self._queue.put(message)

class LoggerFactoryBase(ABC):
    @staticmethod
    @abstractmethod
    def get_logger() -> LoggerBase:
        pass

class ThreadLoggerFactory(LoggerFactoryBase):
    @staticmethod
    def get_logger() -> LoggerBase:
        return ThreadLogger()

logger_singleton = ThreadLoggerFactory().get_logger()
logger_singleton.start_logger()

# def exeption_handler(exception_type, value, traceback):
#     print("stopping logger in exception handler")
#     logger_singleton.stop_logger()
#     sys.__excepthook__(exception_type, value, traceback)

# sys.excepthook = exeption_handler

def atexit_handler():
    print("stopping logger in atexit handler")
    logger_singleton.stop_logger()

atexit.register(atexit_handler)
