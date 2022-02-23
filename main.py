import csv
import datetime

LOGS = 'iterator_logs.csv'

def create_logs_file(file_path=LOGS):
    try:
        with open(file_path) as f:
            pass
    except FileNotFoundError:
        with open(file_path, 'w') as f:
            data = csv.writer(f, delimiter=',')
            data.writerow(['date', 'time', 'function', 'params_in', 'return_value'])

def logging (log_list, path):
    with open(path, 'a') as f:
        data = csv.writer(f, delimiter=',')
        data.writerow(log_list)

def get_date_time() -> [str, str]:
    date = datetime.datetime.now()
    return date.strftime('%d-%m-%Y %H:%M:%S').split()

def param_logger_decor(path=LOGS):
    def logger_decor(old_func):
        def _logger_decor(*args, log_list=[]):
            date_start, time_start = get_date_time()
            params_start_str = ' '.join([str(val) for val in args])
            log_list += [date_start, time_start, old_func.__name__, params_start_str]
            res = list(old_func(*args))
            log_list.append(res)
            logging(log_list, path)
            return res
        return _logger_decor
    return logger_decor

@param_logger_decor()
class FlatIterator:

    def __init__(self, lst):
        self.lst = lst

    def __iter__(self):
        self.cursor = -1
        self.iter_stack = [iter(self.lst)]
        return self

    def __next__(self):
        while self.iter_stack:
            try:
                value = next(self.iter_stack[-1])
            except StopIteration:
                self.iter_stack.pop()
                continue
            if isinstance(value, list):
                self.iter_stack.append(iter(value))
            else:
                return value
        raise StopIteration

if __name__ == '__main__':
    create_logs_file()

    nested_list = [
        ['a', 'b', 'c'], 1, [[[3], 4], 5],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None], 6, [7]
    ]

    for item in FlatIterator(nested_list):
        print(item)
