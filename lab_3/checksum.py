import hashlib


def calculate_checksum(invalid_rows: list) -> str:
    invalid_rows_str = ','.join(map(str, invalid_rows))
    return hashlib.sha256(invalid_rows_str.encode()).hexdigest()


if __name__ == "__main__":
    print("main.py")
