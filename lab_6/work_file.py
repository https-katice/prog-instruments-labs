import json


def read_bytes(path: str) -> bytes:
    """
    Reads bytes from txt file
    :param path: path to txt file
    :return: bytes
    """
    try:
        with open(path, "rb") as file:
            data = file.read()
        return data
    except Exception as e:
        print("Error:", e)


def write_bytes(data: bytes, path: str) -> None:
    """
    Writes bytes into txt file
    :param data: bytes object that is needed to write
    :param path: path to txt file
    """
    try:
        with open(path, "wb") as file:
            file.write(data)
    except Exception as e:
        print("Error:", e)


def read_txt(filename: str) -> str:
    """
    Read and return the content of a text file
    :param filename: path to the text file to be read
    :return: content of the file as a string
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file = file.read().strip()
            return file
    except FileNotFoundError:
        print(f"file {filename} not found")
    except Exception as e:
        print(f"error: {e}")


def write_txt(data: str, filename: str) -> None:
    """
    Writes string into txt file
    :param data: object that is needed to write
    :param filename: path to the output txt file
    :return:
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        raise Exception(f"An error occurred when saving the file: {e}")


def read_json(filename: str) -> dict:
    """
    Read and parse a JSON file into a dictionary
    :param filename: path to the text file to be read
    :return: parsed JSON data as a dictionary
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