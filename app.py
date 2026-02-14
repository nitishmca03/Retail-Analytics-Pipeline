import streamlit as st
import pandas as pd
import sqlite3
import joblib
import os
from datetime import datetime

# --- Data and Model Loading ---

@st.cache_data
def load_data(db_file="retail_db.sqlite"):
    if not os.path.exists(db_file):
        st.error(f"Database file not found at {db_file}")
        return None
    try:
        conn = sqlite3.connect(db_file)
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
        conn.close()
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_resource
def load_model(model_file="churn_model.pkl"):
    if not os.path.exists(model_file):
        st.error(f"Model file not found at {model_file}")
        return None
    try:
        model = joblib.load(model_file)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# --- Main App ---

st.title("Retail Analytics Dashboard")

df = load_data()
model = load_model()

if df is not None:
    tab1, tab2, tab3 = st.tabs(["Business Overview", "Data Explorer", "Prediction Tool"])

    # --- Business Overview Tab ---
    with tab1:
        st.header("Key Business Metrics")

        # Calculations
        total_revenue = (df['Quantity'] * df['Price']).sum()
        avg_order_value = total_revenue / df['OrderID'].nunique()
        
        # Churn Rate Calculation
        max_date = df['TransactionDate'].max()
        last_purchase = df.groupby('City')['TransactionDate'].max().reset_index()
        last_purchase['Recency'] = (max_date - last_purchase['TransactionDate']).dt.days
        churned_customers = last_purchase[last_purchase['Recency'] > 30].shape[0]
        total_customers = last_purchase.shape[0]
        churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:,.2f}")
        col2.metric("Average Order Value", f"${avg_order_value:,.2f}")
        col3.metric("Churn Rate", f"{churn_rate:.2f}%")

    # --- Data Explorer Tab ---
    with tab2:
        st.header("Data Explorer")
        
        # Category Filter
        products = df['Product'].unique()
        selected_products = st.multiselect("Filter by Product:", products, default=products)
        
        filtered_df = df[df['Product'].isin(selected_products)]
        st.dataframe(filtered_df)

        # Download Button
        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(filtered_df)

        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name='filtered_retail_data.csv',
            mime='text/csv',
        )

    # --- Prediction Tool Tab ---
    with tab3:
        st.header("Customer Churn Prediction")

        st.sidebar.header("Enter Customer Details:")
        
        # Load model and scaler
        scaler = joblib.load('scaler.pkl')
        with open('model_columns.txt', 'r') as f:
            model_columns = [line.strip() for line in f]

        # Input fields
        frequency = st.sidebar.number_input("Frequency (Number of Orders)", min_value=1, step=1, value=160)
        monetary = st.sidebar.number_input("Monetary (Total Spent)", min_value=0.0, step=1000.0, value=80000.0)
        product_variety = st.sidebar.number_input("Product Variety (Unique Products)", min_value=1, step=1, value=5)
        average_age = st.sidebar.number_input("Average Age", min_value=18, max_value=100, step=1, value=40)
        gender = st.sidebar.selectbox("Gender", ['Male', 'Female'])
        discount_rate = st.sidebar.slider("Discount Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.1)
        product_category_variety = st.sidebar.number_input("Product Category Variety", min_value=1, step=1, value=3)

        if st.sidebar.button("Predict Churn"):
            if model is not None and scaler is not None:
                # Create a dataframe from the inputs
                input_data = {
                    'Frequency': [frequency],
                    'Monetary': [monetary],
                    'ProductVariety': [product_variety],
                    'AverageAge': [average_age],
                    'DiscountRate': [discount_rate],
                    'ProductCategoryVariety': [product_category_variety],
                    'Gender_Male': [1 if gender == 'Male' else 0]
                }
                input_df = pd.DataFrame(input_data)
                
                # Align columns with the model's training columns
                input_df = input_df.reindex(columns=model_columns, fill_value=0)
                
                # Scale the input
                input_scaled = scaler.transform(input_df)

                prediction = model.predict(input_scaled)
                prediction_proba = model.predict_proba(input_scaled)

                if prediction[0] == 1:
                    churn_probability = prediction_proba[0][1]
                    st.error("Prediction: Customer is likely to CHURN")
                    st.progress(churn_probability)
                    st.write(f"Churn Probability: {churn_probability*100:.2f}%")
                else:
                    stay_probability = prediction_proba[0][0]
                    st.success("Prediction: Customer is likely to STAY")
                    st.progress(stay_probability)
                    st.write(f"Stay Probability: {stay_probability*100:.2f}%")
            else:
                st.warning("Prediction model or scaler not available.")
else:
    st.warning("Could not load data. Please ensure retail_db.sqlite is available.")
