import json
from logging_config import get_module_logger

logger = get_module_logger(__name__)


def read_txt(filename: str) -> str:
    """
    Чтение содержимого файла
    :param filename: путь к текстовому файлу для чтения
    :return: содержимое файла в виде строки
    """
    logger.info(f"Чтение файла: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            logger.debug(f"Файл прочитан, размер: {len(content)} символов")
            return content

    except FileNotFoundError:
        logger.error(f"Файл не найден: {filename}")
        return None
    except PermissionError:
        logger.error(f"Нет прав на чтение файла: {filename}")
        return None
    except UnicodeDecodeError:
        logger.error(f"Ошибка кодировки файла: {filename}")
        return None
    except Exception as e:
        logger.exception(
            f"Неожиданная ошибка при чтении файла {filename}: {e}"
        )
        return None


def read_json(filename: str) -> dict:
    """
    Чтение файла JSON
    :param filename: путь к JSON файлу для чтения
    :return: данные в виде словаря
    """
    logger.info(f"Чтение JSON файла: {filename}")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug(f"JSON файл {filename} успешно прочитан")
            return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {filename}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка формата JSON в файле {filename}: {e}")
        return None
    except PermissionError:
        logger.error(f"Нет прав на чтение файла: {filename}")
        return None
    except Exception as e:
        logger.exception(
            f"Неожиданная ошибка при чтении JSON файла {filename}: {e}"
        )
        return None


def write_json(dictionary: dict, filename: str) -> None:
    """
    Запись словаря в формате JSON
    :param dictionary: словарь для записи в формате JSON
    :param filename: путь к выходному файлу
    """
    logger.info(f"Запись данных в JSON файл: {filename}")

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4, ensure_ascii=False)
            logger.info(f"Данные успешно записаны в файл {filename}")
            logger.debug(f"Записано {len(str(dictionary))} символов")

    except PermissionError:
        logger.error(f"Нет прав на запись в файл: {filename}")
        raise
    except TypeError as e:
        logger.error(f"Некорректный тип данных для JSON: {e}")
        raise
    except Exception as e:
        logger.exception(
            f"Неожиданная ошибка при записи в файл {filename}: {e}"
        )
        raise
