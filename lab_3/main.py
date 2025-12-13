import csv
import re
from datetime import datetime
from typing import Dict, List, Tuple
from checksum import calculate_checksum, serialize_result


class DataValidator:
    def __init__(self):
        self.patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'height': r'^[12]\.\d{1,2}$',
            'inn': r'^\d{12}$',
            'passport': r'^\d{2}\s\d{2}\s\d{6}$',
            'latitude': r'^-?\d{1,2}\.\d+$',
            'hex_color': r'^#[0-9a-fA-F]{6}$',
            'issn': r'^\d{4}-\d{4}$',
            'uuid': (
                r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-'
                r'[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            ),
            'time': r'^\d{2}:\d{2}:\d{2}\.\d{1,6}$',
        }
        self.occupation_pattern = r'^[а-яА-ЯёЁ\s\-_]+$'

    def validate_email(self, email: str) -> bool:
        return bool(re.match(self.patterns['email'], email))

    def validate_height(self, height: str) -> bool:
        height_clean = height.replace(',', '.')
        height_clean = re.sub(r'[^\d.]', '', height_clean)
        if not re.match(self.patterns['height'], height_clean):
            return False
        try:
            h = float(height_clean)
            return 1.0 <= h <= 2.5
        except ValueError:
            return False

    def validate_inn(self, inn: str) -> bool:
        return bool(re.match(self.patterns['inn'], inn))

    def validate_passport(self, passport: str) -> bool:
        return bool(re.match(self.patterns['passport'], passport))

    def validate_occupation(self, occupation: str) -> bool:
        occupation_clean = occupation.strip()
        occupation_clean = re.sub(r'_+', '_', occupation_clean)
        if not re.match(
                self.occupation_pattern,
                occupation_clean.replace('_', '')
                        ):
            return False
        return True

    def validate_latitude(self, latitude: str) -> bool:
        lat_clean = latitude.replace(',', '.')
        lat_clean = re.sub(r'[^\d.\-]', '', lat_clean)
        if not re.match(self.patterns['latitude'], lat_clean):
            return False
        try:
            lat = float(lat_clean)
            return -90.0 <= lat <= 90.0
        except ValueError:
            return False

    def validate_hex_color(self, color: str) -> bool:
        return bool(re.match(self.patterns['hex_color'], color))

    def validate_issn(self, issn: str) -> bool:
        return bool(re.match(self.patterns['issn'], issn))

    def validate_uuid(self, uuid_str: str) -> bool:
        uuid_clean = uuid_str.strip('_')
        return bool(re.match(self.patterns['uuid'], uuid_clean))

    def validate_time(self, time_str: str) -> bool:
        time_clean = time_str.replace('_', ':').replace('-', ':')
        if not re.match(self.patterns['time'], time_clean):
            return False
        try:
            time_part = time_clean.split('.')[0]
            datetime.strptime(time_part, '%H:%M:%S')
            return True
        except ValueError:
            return False

    def validate_row(self, row: Dict) -> Tuple[Dict, Dict]:
        validated_data = {}
        errors = {}
        for field, value in row.items():
            try:
                if field == 'email':
                    if not self.validate_email(value):
                        errors[field] = f"Invalid email format: {value}"
                    else:
                        validated_data[field] = value.lower()
                elif field == 'height':
                    if not self.validate_height(value):
                        errors[field] = f"Invalid height: {value}"
                    else:
                        height_clean = value.replace(',', '.')
                        height_clean = re.sub(r'[^\d.]', '', height_clean)
                        validated_data[field] = float(height_clean)
                elif field == 'inn':
                    if not self.validate_inn(value):
                        errors[field] = f"Invalid INN: {value}"
                    else:
                        validated_data[field] = value
                elif field == 'passport':
                    if not self.validate_passport(value):
                        errors[field] = f"Invalid passport format: {value}"
                    else:
                        validated_data[field] = value
                elif field == 'occupation':
                    if not self.validate_occupation(value):
                        errors[field] = f"Invalid occupation: {value}"
                    else:
                        occ_clean = value.strip()
                        occ_clean = re.sub(r'_+', '_', occ_clean)
                        validated_data[field] = occ_clean
                elif field == 'latitude':
                    if not self.validate_latitude(value):
                        errors[field] = f"Invalid latitude: {value}"
                    else:
                        lat_clean = value.replace(',', '.')
                        lat_clean = re.sub(r'[^\d.\-]', '', lat_clean)
                        validated_data[field] = float(lat_clean)
                elif field == 'hex_color':
                    if not self.validate_hex_color(value):
                        errors[field] = f"Invalid hex color: {value}"
                    else:
                        validated_data[field] = value.lower()
                elif field == 'issn':
                    if not self.validate_issn(value):
                        errors[field] = f"Invalid ISSN: {value}"
                    else:
                        validated_data[field] = value
                elif field == 'uuid':
                    if not self.validate_uuid(value):
                        errors[field] = f"Invalid UUID: {value}"
                    else:
                        validated_data[field] = value.strip('_').lower()
                elif field == 'time':
                    if not self.validate_time(value):
                        errors[field] = f"Invalid time format: {value}"
                    else:
                        time_clean = value.replace('_', ':').replace('-', ':')
                        validated_data[field] = time_clean
            except Exception as e:
                errors[field] = f"Validation error: {str(e)}"
        return validated_data, errors


def read_csv_file(filename: str) -> List[Dict]:
    data = []
    with open(filename, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data.append(row)
    return data


def main():
    data = read_csv_file('47.csv')
    validator = DataValidator()
    invalid_rows = []

    for i, row in enumerate(data, 0):
        _, errors = validator.validate_row(row)
        if errors:
            invalid_rows.append(i)

    checksum = calculate_checksum(invalid_rows)
    serialize_result(47, checksum)


if __name__ == "__main__":
    main()
