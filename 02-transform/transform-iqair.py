import os
import pandas as pd

def clean_csv(file_paths):
    for file_path in file_paths:
        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file_path)

        # Membersihkan data pada kolom 'iqa', 'wind_dir(deg)', 'wind_spd(km/h)', 'pressure(mbar)'
        df['iqa'] = df['iqa'].str.replace('*', '')
        df['wind_dir(deg)'] = df['wind_dir(deg)'].str.extract(r'(\d+)')
        df['wind_spd(km/h)'] = df['wind_spd(km/h)'].str.replace(' km/h', '')
        df['pressure(mbar)'] = df['pressure(mbar)'].str.replace('mbar', '').str.lstrip('0')

        # Mengonversi data type ke data type yang seharusnya
        df['kota'] = df['kota'].astype(str)
        df['wind_dir(deg)'] = df['wind_dir(deg)'].astype(int)
        df['wind_spd(km/h)'] = df['wind_spd(km/h)'].astype(float)
        df['pressure(mbar)'] = df['pressure(mbar)'].astype(int)
        df['iqa'] = df['iqa'].astype(int)
        df['accessed'] = pd.to_datetime(df['accessed'], format = '%Y-%m-%d %H')

        # Mendapatkan nama file tanpa ekstensi
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Menentukan direktori untuk menyimpan file CSV yang sudah dibersihkan
        cleaned_dir = '../ETL-Pipeline/csv/cleaned-iqair/'
        os.makedirs(cleaned_dir, exist_ok=True)  # Membuat direktori jika belum ada

        # Menyimpan DataFrame yang sudah dibersihkan ke dalam file CSV baru
        cleaned_file_path = os.path.join(cleaned_dir, f'cleaned_{file_name}.csv')
        df.to_csv(cleaned_file_path, index=False)

def merge_cleaned_files(directory):
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.startswith('cleaned_')]

    # Membaca semua file cleaned_{file_name}.csv ke dalam list DataFrame
    dfs = [pd.read_csv(file) for file in file_paths]

    if dfs:
        # Menggabungkan DataFrames
        merged_df = pd.concat(dfs, ignore_index=True)

        # Menghapus data yang ganda
        merged_df.drop_duplicates(inplace=True)

        # Mengurutkan berdasarkan kolom 'kota'
        merged_df = merged_df.sort_values(by='kota')

        # Menyimpan DataFrame yang sudah digabungkan, diurutkan, dan tanpa data ganda ke dalam file CSV baru
        merged_dir = '../ETL-Pipeline/csv/merged-iqair/'
        os.makedirs(merged_dir, exist_ok=True)  # Membuat direktori jika belum ada

        merged_file_path = os.path.join(merged_dir, 'merged_cleaned_files.csv')
        merged_df.to_csv(merged_file_path, index=False)
        print("Files successfully merged, sorted, and duplicates removed.")
    else:
        print("No cleaned files found in the directory.")

# Daftar file yang perlu dibersihkan
file_paths = [
    '../ETL-Pipeline/csv/raw-iqair/2023-11-20-00.csv',
    '../ETL-Pipeline/csv/raw-iqair/2023-11-20-06.csv'
]

# Memanggil fungsi clean_csv untuk membersihkan data pada file-file CSV
clean_csv(file_paths)

# Directory tempat file cleaned_{file_name}.csv disimpan
directory = '../ETL-Pipeline/csv/cleaned-iqair/'

# Memanggil fungsi untuk menggabungkan file-file yang telah dibersihkan
merge_cleaned_files(directory)
