import pandas as pd
import sqlite3
import os
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import joblib
from datetime import datetime

def churn_prediction(db_file="retail_db.sqlite", model_output="churn_model.pkl", plot_output="scripts/feature_importance.png"):
    """
    Connects to the SQLite database, calculates RFM features, trains a churn prediction model,
    and saves the model and a feature importance plot.
    """
    if not os.path.exists(db_file):
        print(f"Error: Database file not found at {db_file}")
        return

    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to database '{db_file}'")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    try:
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
        conn.close()
        print("Successfully loaded data from the 'transactions' table.")
    except Exception as e:
        print(f"Error loading data: {e}")
        conn.close()
        return

    # Feature Engineering
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    snapshot_date = df['TransactionDate'].max() + pd.DateOffset(days=1)
    
    features_df = df.groupby('City').agg({
        'TransactionDate': lambda date: (snapshot_date - date.max()).days,
        'OrderID': 'count',
        'Price': 'sum',
        'Product': 'nunique',
        'CustomerAge': 'mean',
        'Customer_Gender': 'first',
        'Discount_Applied': 'mean',
        'Product_Category': 'nunique'
    }).rename(columns={
        'TransactionDate': 'Recency',
        'OrderID': 'Frequency',
        'Price': 'Monetary',
        'Product': 'ProductVariety',
        'CustomerAge': 'AverageAge',
        'Customer_Gender': 'Gender',
        'Discount_Applied': 'DiscountRate',
        'Product_Category': 'ProductCategoryVariety'
    })
    
    # Labeling Churn
    features_df['Churn'] = (features_df['Recency'] > 30).astype(int)
    print("Calculated enhanced features and labeled churn.")

    # Model Training
    X = features_df.drop(['Recency', 'Churn'], axis=1)
    y = features_df['Churn']
    
    # One-hot encode categorical features
    X = pd.get_dummies(X, columns=['Gender'], drop_first=True)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    print(f"Model trained with accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Feature Importance Plot
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    plt.figure(figsize=(10, 8))
    feature_importances.nlargest(15).plot(kind='barh')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig(plot_output)
    print(f"Saved feature importance plot to {plot_output}")
    
    # Save Model, Scaler and Columns
    joblib.dump(model, model_output)
    joblib.dump(scaler, 'scaler.pkl')
    
    with open('model_columns.txt', 'w') as f:
        for col in X.columns:
            f.write(col + '\n')
            
    print(f"\nSaved trained model, scaler, and column order.")

if __name__ == "__main__":
    churn_prediction()
    """
    This script performs churn prediction based on retail data.

    It starts by connecting to the `retail_db.sqlite` database and loading the `transactions` table.
    
    Then, it calculates the Recency, Frequency, and Monetary (RFM) features for each customer.
    - **Recency**: Days since the last transaction.
    - **Frequency**: Total number of transactions.
    - **Monetary**: Total amount spent.

    A customer is labeled as 'Churn' if their Recency is more than 90 days.

    A RandomForestClassifier is trained to predict churn using the 'Frequency' and 'Monetary' features.
    
    Finally, the script saves:
    1. A bar plot of feature importances to `scripts/feature_importance.png`.
    2. The trained model to a file named `churn_model.pkl` using joblib.
    """
