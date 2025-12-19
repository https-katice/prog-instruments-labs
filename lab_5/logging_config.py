import logging
import sys
from pathlib import Path


def setup_logging(
        log_file='project.log',
        console_level=logging.WARNING,
        file_level=logging.INFO
):
    """
    Настраивает систему логирования для проекта.

    Args:
        log_file (str): Имя файла для записи логов
        console_level: Уровень логирования для консоли
        file_level: Уровень логирования для файла

    Returns:
        logging.Logger: Корневой логгер
    """
    log_path = Path(log_file)
    if log_path.parent and not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(
        log_file, encoding='utf-8', mode='a', errors='replace'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if root_logger.handlers:
        root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

    root_logger.info("=" * 50)
    root_logger.info("Система логирования успешно настроена")
    root_logger.info(f"Файл логов: {log_file}")
    root_logger.info(f"Уровень консоли: {logging.getLevelName(console_level)}")
    root_logger.info(f"Уровень файла: {logging.getLevelName(file_level)}")
    root_logger.info("=" * 50)

    return root_logger


def get_module_logger(module_name):
    logger = logging.getLogger(module_name)
    return logger


logger = get_module_logger('main')
