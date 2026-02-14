import pandas as pd
import numpy as np
import joblib
import os

def test_model(num_profiles=100, output_file="test_predictions.csv"):
    """
    Generates a diverse set of customer profiles, loads the trained churn model,
    predicts churn probability for each profile, and saves the results to a CSV file.
    """
    if not os.path.exists('churn_model.pkl') or not os.path.exists('scaler.pkl'):
        print("Error: Model or scaler not found. Please train the model first.")
        return

    # Load model, scaler, and columns
    model = joblib.load('churn_model.pkl')
    scaler = joblib.load('scaler.pkl')
    with open('model_columns.txt', 'r') as f:
        model_columns = [line.strip() for line in f]
    
    print("Successfully loaded model, scaler, and column order.")

    # Generate diverse customer profiles
    test_data = {
        'Frequency': np.random.randint(10, 250, num_profiles),
        'Monetary': np.round(np.random.uniform(1000, 120000, num_profiles), 2),
        'ProductVariety': np.random.randint(1, 9, num_profiles),
        'AverageAge': np.random.randint(18, 75, num_profiles),
        'Gender': np.random.choice(['Male', 'Female'], num_profiles),
        'DiscountRate': np.round(np.random.uniform(0, 1, num_profiles), 2),
        'ProductCategoryVariety': np.random.randint(1, 4, num_profiles)
    }
    test_df = pd.DataFrame(test_data)
    print(f"Generated {num_profiles} diverse customer profiles for testing.")

    # Prepare data for prediction (one-hot encoding and scaling)
    X_test = pd.get_dummies(test_df, columns=['Gender'], drop_first=True)
    X_test = X_test.reindex(columns=model_columns, fill_value=0)
    
    # Ensure all columns are numeric before scaling
    for col in X_test.columns:
        X_test[col] = pd.to_numeric(X_test[col])

    X_test_scaled = scaler.transform(X_test)

    # Make predictions
    predictions_proba = model.predict_proba(X_test_scaled)[:, 1]
    test_df['Churn_Probability'] = predictions_proba
    
    # Save results
    test_df.to_csv(output_file, index=False)
    print(f"Saved test predictions to {output_file}")

    # Analyze and print interesting findings
    print("\n--- Test Analysis ---")
    highest_churn = test_df.sort_values(by='Churn_Probability', ascending=False).iloc[0]
    lowest_churn = test_df.sort_values(by='Churn_Probability', ascending=True).iloc[0]

    print("\nProfile with HIGHEST Churn Probability:")
    print(highest_churn)
    
    print("\nProfile with LOWEST Churn Probability:")
    print(lowest_churn)


if __name__ == "__main__":
    test_model()
