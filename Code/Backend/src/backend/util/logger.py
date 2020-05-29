import datetime

class log():
    # fallback to old method
    def __init__(self, *args):
        log._log(*args)

    @staticmethod
    def _log(name, level, message, show_time = True):
        level_types = ['INFO', 'WARN', 'ERROR', 'CRITICAL']

        if level not in level_types:
            print('Invalid error logging level, please use one of the following:', level_types)
            return

        log = ''
        color = ('', '')

        if show_time:
            currentDate = datetime.datetime.now()
            log = f'[{currentDate.strftime("%H:%M:%S")}] '

        if level == 'WARN':
            color = ('\x1b[33m', '\x1b[0m')
        elif level == 'ERROR' or level == 'CRITICAL':
            color = ('\x1b[31m', '\x1b[0m')

        print(f'{log}{color[0]}[{name}/{level}]{color[1]} {message}')

    @staticmethod
    def info(name, message, show_time = True):
        log._log(name, 'INFO', message, show_time)

    @staticmethod
    def warning(name, message, show_time = True):
        log._log(name, 'WARN', message, show_time)

    @staticmethod
    def error(name, message, show_time = True):
        log._log(name, 'ERROR', message, show_time)

    @staticmethod
    def critical(name, message, show_time = True):
        log._log(name, 'CRITICAL', message, show_time)

"""def log(name, level, message, show_time = True):
    level_types = ['INFO', 'WARN', 'ERROR', 'CRITICAL']

    if level not in level_types:
        print('Invalid error logging level, please use one of the following:', level_types)
        return

    log = ''
    color = ('', '')

    if show_time:
        currentDate = datetime.datetime.now()
        log = f'[{currentDate.strftime("%H:%M:%S")}] '

    if level == 'WARN':
        color = ('\x1b[33m', '\x1b[0m')
    elif level == 'ERROR' or level == 'CRITICAL':
        color = ('\x1b[31m', '\x1b[0m')

    print(f'{log}{color[0]}[{name}/{level}]{color[1]} {message}')
"""
