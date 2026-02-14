import pandas as pd
import numpy as np
import os

def generate_retail_data(num_records=1000, output_dir="data"):
    """
    Generates dummy retail transaction data with active and churned customers.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam', 'Headphones', 'Speaker', 'Microphone']
    product_categories = {
        'Laptop': 'Electronics', 'Monitor': 'Electronics',
        'Mouse': 'Accessories', 'Keyboard': 'Accessories', 'Webcam': 'Accessories', 'Headphones': 'Accessories',
        'Speaker': 'Audio', 'Microphone': 'Audio'
    }
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Online Transfer']
    genders = ['Male', 'Female']
    
    active_cities = ['New York', 'Los Angeles', 'Chicago']
    churned_cities = ['Houston', 'Phoenix', 'Philadelphia']

    # Generate data for active customers
    active_data = {
        'OrderID': np.arange(1, num_records // 2 + 1),
        'Product': np.random.choice(products, num_records // 2),
        'Quantity': np.random.randint(2, 6, num_records // 2),
        'Price': np.round(np.random.uniform(50, 1200, num_records // 2), 2),
        'CustomerAge': np.random.randint(18, 70, num_records // 2),
        'City': np.random.choice(active_cities, num_records // 2),
        'PaymentMethod': np.random.choice(payment_methods, num_records // 2),
        'TransactionDate': pd.to_datetime('2025-12-01') - pd.to_timedelta(np.random.randint(0, 30, num_records // 2), unit='D'),
        'Customer_Gender': np.random.choice(genders, num_records // 2),
        'Discount_Applied': np.random.choice([True, False], num_records // 2, p=[0.2, 0.8])
    }
    active_df = pd.DataFrame(active_data)

    # Generate data for churned customers
    churned_data = {
        'OrderID': np.arange(num_records // 2 + 1, num_records + 1),
        'Product': np.random.choice(products, num_records // 2),
        'Quantity': np.random.randint(1, 3, num_records // 2),
        'Price': np.round(np.random.uniform(10, 500, num_records // 2), 2),
        'CustomerAge': np.random.randint(18, 70, num_records // 2),
        'City': np.random.choice(churned_cities, num_records // 2),
        'PaymentMethod': np.random.choice(payment_methods, num_records // 2),
        'TransactionDate': pd.to_datetime('2025-12-01') - pd.to_timedelta(np.random.randint(31, 365, num_records // 2), unit='D'),
        'Customer_Gender': np.random.choice(genders, num_records // 2),
        'Discount_Applied': np.random.choice([True, False], num_records // 2, p=[0.1, 0.9])
    }
    churned_df = pd.DataFrame(churned_data)

    df = pd.concat([active_df, churned_df])
    df['Product_Category'] = df['Product'].map(product_categories)
    df = df.sort_values(by='TransactionDate').reset_index(drop=True)
    
    output_path = os.path.join(output_dir, "retail_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Generated {num_records} retail data records with new features to {output_path}")

if __name__ == "__main__":
    generate_retail_data()
