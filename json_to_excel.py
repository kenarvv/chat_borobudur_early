import json
import pandas as pd
import os

# Path file JSON dan Excel
JSON_FILE = 'kb_borobudur.json'
EXCEL_FILE = 'kb_borobudur_export.xlsx'

def add_quotes_to_string(value):
    """
    Tambahkan kutip pada data yang rentan diubah formatnya oleh Excel.
    """
    if isinstance(value, str):
        # Tambahkan tanda kutip hanya jika data berupa string
        return f"'{value}"
    return value

def json_to_excel(json_file, excel_file):
    if not os.path.exists(json_file):
        print(f"File {json_file} tidak ditemukan.")
        return

    # Membaca file JSON
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    with pd.ExcelWriter(excel_file) as writer:
        for category, items in json_data.items():
            if isinstance(items, list):  # Data berupa list
                # Konversi list of dict ke DataFrame
                df = pd.DataFrame(items)
                # Terapkan tanda kutip pada semua data
                df = df.apply(lambda x: x.apply(add_quotes_to_string))
            elif isinstance(items, dict):  # Data berupa dictionary
                # Konversi dictionary ke DataFrame dengan Key-Value
                df = pd.DataFrame(items.items(), columns=["Key", "Value"])
                df["Key"] = df["Key"].apply(add_quotes_to_string)
                df["Value"] = df["Value"].apply(add_quotes_to_string)
            else:
                # Abaikan data yang tidak valid
                print(f"Kategori '{category}' tidak valid dan akan dilewati.")
                continue

            # Simpan ke Excel
            df.to_excel(writer, sheet_name=category, index=False)

    print(f"Data JSON berhasil diekspor ke Excel: {excel_file}")

if __name__ == "__main__":
    try:
        json_to_excel(JSON_FILE, EXCEL_FILE)
    except Exception as e:
        print(f"Error: {e}")