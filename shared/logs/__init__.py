import logging
import logging.handlers


def setup_logging():
    logger = logging.getLogger('main_logger')
    logger.setLevel(logging.DEBUG)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)

    # Обработчик для сервера
    # TODO: почини меня
    # server_handler = logging.handlers.SysLogHandler(address=('localhost', 514))
    # server_handler.setLevel(logging.ERROR)
    # server_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    # server_handler.setFormatter(server_format)

    # Добавляем обработчики к логгеру
    logger.addHandler(console_handler)
    # logger.addHandler(server_handler)

    return logger


# пример использования логирования в модуле
# import logging

# def do_something():
#     logger = logging.getLogger('my_logger')
#     logger.info("Doing something!")
#     try:
#         # Некоторая логика, которая может вызвать исключение
#         pass
#     except Exception as e:
#         logger.error(f"Ошибка в do_something: {e}")
