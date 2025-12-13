import re
import json
import pandas as pd
from checksum import calculate_checksum, serialize_result


def read_json(path: str) -> dict[str, str]:
    """
    Reads json from the file
    :param path: Path to the JSON file
    :return: Dict of [str, Any]
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file was not found.")
    except PermissionError as e:
        print(f"Can't access this file: {str(e)}")
    except Exception as e:
        print(f"An error occurred while reading json the file: {str(e)}.")


def read_csv(path: str) -> pd.DataFrame:
    """
    Reads CSV file as a Pandas DataFrame
    :param path: Path to the CSV file
    :return: Pandas DataFrame
    """
    try:
        df = pd.read_csv(path, encoding='utf-16', header=0, sep=';', dtype=str)
        return df
    except FileNotFoundError:
        print(f"The file was not found.")
    except PermissionError as e:
        print(f"Can't access this file: {str(e)}")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}.")


def validate(data: pd.DataFrame, regular_expressions: dict[str, str]) -> list:
    """
    Validates DataFrame with regular expressions
    :param data: DataFrame
    :param regular_expressions: RegEx from file
    :return: list of wrong rows numbers
    """
    results = set()
    for col, expr in regular_expressions.items():
        for i in data.index:
            if not bool(re.fullmatch(expr, str(data.loc[i, col]))):
                results.add(i)

    return sorted(results)


def main():
    settings = read_json("settings.json")
    regex = read_json("regs.json")
    df = read_csv(settings["csv_path"])
    result = validate(df, regex)
    checksum = calculate_checksum(result)
    serialize_result(settings["variant"],
                     checksum,
                     str(settings["result_path"]))


if __name__ == "__main__":
    main()

