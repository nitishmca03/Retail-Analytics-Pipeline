import pandas as pd
import os

def etl_process(input_file="data/retail_data.csv", output_dir="data", output_file="processed_retail_data.csv"):
    """
    Performs a simple ETL process on retail data:
    1. Extracts data from retail_data.csv.
    2. Transforms data by calculating total sales per product.
    3. Loads processed data to processed_retail_data.csv.
    """
    input_path = input_file
    output_path = os.path.join(output_dir, output_file)

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    try:
        df = pd.read_csv(input_path)
        print(f"Successfully extracted data from {input_path}")
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Transformation: Calculate total sales per product
    df['TotalSales'] = df['Quantity'] * df['Price']
    processed_df = df.groupby('Product')['TotalSales'].sum().reset_index()
    processed_df = processed_df.sort_values(by='TotalSales', ascending=False)
    print("Transformation: Calculated total sales per product.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        processed_df.to_csv(output_path, index=False)
        print(f"Successfully loaded processed data to {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    etl_process()
