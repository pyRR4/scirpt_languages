import datetime
import logging
import functools
import time


def logger(log_level=logging.DEBUG):
    logging.basicConfig(level=log_level)

    def decor(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_date = datetime.datetime.now().strftime("%H:%M:%S")
            start_time = time.time()
            f_res = f(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time

            logging.log(log_level, f"Nazwa funkcji: {f.__name__}, wywołana z argumentami: args - {args}"
                                   f", kwargs - {kwargs}")
            logging.log(log_level, f"Funkcja {f.__name__} została wywołana o: {start_date}, jej wykonanie trwało: {duration}")
            logging.log(log_level, f"Funkcja {f.__name__} zwróciła: {f_res}")
            return f_res
        return wrapper
    return decor


@logger(logging.DEBUG)
def some_func(x, y):
    num = 0
    while num < x ** y:
        num += 1

    return num


@logger(logging.DEBUG)
class SomeClass:
    def __init__(self, param):
        self.param = param


some_class = SomeClass("someclassparam")
func = some_func(80, 3)
