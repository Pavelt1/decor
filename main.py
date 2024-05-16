import os
import datetime


def logger(old_function):

    def new_function(*args, **kwargs):
        path = "main.log"
        start_time_func = datetime.datetime.now()
        result = old_function(*args, **kwargs)

        with open(path, "a", encoding="utf-8" ) as f:
            f.write(f"{old_function.__name__}\n")
            f.write(f"Дата и время активации {start_time_func}\n")
            f.write(f"{args if args else ''}{kwargs if kwargs else ''}{result}\n\n")

        return result

    return new_function

def llogger(path):
    
    def __logger(old_function):
        def new_function(*args, **kwargs):
            start_time_func = datetime.datetime.now()
            result = old_function(*args, **kwargs)

            with open(path, "a", encoding="utf-8" ) as f:
                f.write(f"{old_function.__name__}\n")
                f.write(f"Дата и время активации {start_time_func}\n")
                f.write(f"{args if args else ''}{kwargs if kwargs else ''}{result}\n\n")

            return result
        return new_function

    return __logger


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @llogger(path)
        def hello_world():
            return 'Hello World'

        @llogger(path)
        def summator(a, b=0):
            return a + b

        @llogger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    test_2()
