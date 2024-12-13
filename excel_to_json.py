import pandas as pd
import json
import os

# Path file JSON dan Excel
JSON_FILE = 'kb_borobudur.json'
EXCEL_FILE = 'kb_borobudur_export.xlsx'

def remove_quotes_from_string(value):
    """
    Hapus tanda kutip di awal string jika ada.
    """
    if isinstance(value, str) and value.startswith("'"):
        return value[1:]
    return value

def excel_to_json(excel_file, json_file):
    if not os.path.exists(excel_file):
        print(f"File {excel_file} tidak ditemukan.")
        return

    new_data = {}
    excel_data = pd.ExcelFile(excel_file)

    for sheet_name in excel_data.sheet_names:
        df = excel_data.parse(sheet_name, dtype=str)
        
        # Hapus kutip dari semua data
        df = df.apply(lambda x: x.apply(remove_quotes_from_string))

        if "Key" in df.columns and "Value" in df.columns:
            new_data[sheet_name] = {row["Key"]: row["Value"] for _, row in df.iterrows()}
        else:
            new_data[sheet_name] = df.to_dict(orient='records')

    with open(json_file, 'w') as f:
        json.dump(new_data, f, indent=4)

    print(f"Data Excel berhasil diimpor ke JSON: {json_file}")


if __name__ == "__main__":
    try:
        excel_to_json(EXCEL_FILE, JSON_FILE)
    except Exception as e:
        print(f"Error: {e}")