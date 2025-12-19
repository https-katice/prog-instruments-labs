import json


def read_txt(filename: str) -> str:
    """
    Чтение содержимого файла
    :param filename: путь к текстовому файлу для чтения
    :return: содержимое файла в виде строки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file = file.read().strip()
            return file
    except FileNotFoundError:
        print(f"file {filename} not found")
    except Exception as e:
        print(f"error: {e}")


def read_json(filename: str) -> dict:
    """
    Чтение файла json
    :param filename: путь к текстовому файлу для чтения
    :return: данные в виде словаря
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"file {filename} not found")
    except json.JSONDecodeError:
        print(f"file {filename} isn't correct JSON.")
    except Exception as e:
        print(f"error: {e}")


def write_json(dictionary: dict, filename: str) -> None:
    """
    Запись словаря в формате json
    :param dictionary: словарь для записи в формате json
    :param filename: путь к выходному файлу
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"An error occurred when saving the file: {e}")