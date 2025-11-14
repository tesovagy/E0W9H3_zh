import json
import os

def load_data_ob(filepath="warehouse_data.json"):

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if isinstance(data, dict) and 'products' in data:
                return data
            else:
                return {'products': data, 'thresholds': {}}
    except FileNotFoundError:
        return {'products': {}, 'thresholds': {}}

def save_data_ob(data, filepath="warehouse_data.json"):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def export_report_ob(data, filepath="warehouse_report.txt"):
    with open(filepath, 'w', encoding='utf-8') as file:
        for product, quantity in data.items():
            file.write(f"{product}: {quantity} db\n")