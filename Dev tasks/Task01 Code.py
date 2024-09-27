# Task 1 solution 

import requests
import pyarrow.feather as feather
import zipfile
import os
import pandas as pd
from multiprocessing import Pool
import redis

# 1. Data Extraction: Fetch data from the Telegram channel or ICICI Breeze API and download it.
def download_data(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

# 2. Extract nested zip files if needed.
def extract_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# 3. Partition data by year, month, expiry, and derivative type.
def partition_data(df, output_dir):
    for derivative in df['derivative_type'].unique():
        derivative_dir = os.path.join(output_dir, derivative)
        os.makedirs(derivative_dir, exist_ok=True)
        for year in df['year'].unique():
            year_dir = os.path.join(derivative_dir, str(year))
            os.makedirs(year_dir, exist_ok=True)
            for expiry in df['expiry_date'].unique():
                expiry_data = df[df['expiry_date'] == expiry]
                expiry_file = os.path.join(year_dir, f"{expiry}_data.feather")
                expiry_data.to_feather(expiry_file)

# 4. Use Feather/Parquet formats for efficient local or cloud storage.
def save_to_feather(df, file_path):
    feather.write_feather(df, file_path)

# 5. Apply indexing on expiry dates and strike prices for faster access.
def index_data(df):
    df.set_index(['expiry_date', 'strike_price'], inplace=True)

# 6. Dynamically filter contracts based on expiry using rolling windows.
def filter_by_expiry(df, start_date, end_date):
    return df[(df['expiry_date'] >= start_date) & (df['expiry_date'] <= end_date)]

# 7. Load data in chunks to optimize memory usage.
def load_data_in_chunks(file_path, chunk_size=10000):
    return pd.read_feather(file_path, chunksize=chunk_size)

# 8. Implement rolling contracts functionality.
def roll_over_contracts(df, current_expiry):
    next_expiry = df[df['expiry_date'] > current_expiry]['expiry_date'].min()
    return df[df['expiry_date'] == next_expiry]

# 9. Use multiprocessing to handle large volumes of data in parallel.
def process_in_parallel(files):
    with Pool() as pool:
        pool.map(load_data_in_chunks, files)

# 10. Use Redis caching for frequently accessed data.
cache = redis.Redis()

def cache_data(key, df):
    cache.set(key, df.to_msgpack(compress='zlib'))

def retrieve_cached_data(key):
    cached_data = cache.get(key)
    if cached_data:
        return pd.read_msgpack(cached_data)

# Main function demonstrating data extraction, handling, and optimization.
def main():
    # Example URL for data download
    url = 'https://example.com/data.zip'
    file_path = 'data.zip'
    
    # Step 1: Download data
    download_data(url, file_path)
    
    # Step 2: Extract data
    extract_zip(file_path, 'extracted_data')
    
    # Step 3: Load data and partition it
    df = pd.read_feather('extracted_data/sample_data.feather')
    partition_data(df, 'partitioned_data')
    
    # Step 4: Index and filter data based on expiry
    index_data(df)
    filtered_data = filter_by_expiry(df, '2024-01-01', '2024-01-31')
    
    # Step 5: Save filtered data to Feather format
    save_to_feather(filtered_data, 'filtered_data.feather')
    
    # Step 6: Load data in chunks for processing
    chunks = load_data_in_chunks('filtered_data.feather')
    
    # Step 7: Process multiple files in parallel
    files = ['file1.feather', 'file2.feather']
    process_in_parallel(files)
    
    # Step 8: Cache frequently accessed data
    cache_data('filtered_data', filtered_data)
    cached_data = retrieve_cached_data('filtered_data')

if __name__ == "__main__":
    main()
