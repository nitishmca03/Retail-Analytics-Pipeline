# Retail Analytics Dashboard

This project is a comprehensive retail analytics dashboard built with Python and Streamlit. It provides insights into sales data, customer churn, and more. The project demonstrates a full data science workflow, from data generation and analysis to model training and deployment.

## Features

*   **Business Overview:** A high-level dashboard with key metrics such as Total Revenue, Average Order Value, and Churn Rate.
*   **Data Explorer:** An interactive table of the raw transaction data with filtering capabilities and a download option.
*   **Churn Prediction Tool:** A machine learning-powered tool to predict customer churn based on various customer attributes, including:
    *   Frequency and Monetary value
    *   Product variety and age
    *   Gender and discount rates
*   **Automated Data Pipeline:** The project includes scripts to generate, process, and analyze the data, as well as to train and test the churn prediction model.

## How to Run the Application Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nitishmca03/Retail-Analytics-Pipeline.git
    cd Retail-Analytics-Pipeline
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # On Windows
    python -m venv .venv
    .venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

## Deployment

The application is intended to be deployed on the Streamlit Community Cloud. Once you have deployed it, you can add the public URL here.

[**View the Live Application**](YOUR_STREAMLIT_APP_URL_HERE)

*(Note: You will need to replace `YOUR_STREAMLIT_APP_URL_HERE` with the actual URL of your deployed application after you've deployed it.)*

## Project Structure

```
.
├── app.py                  # The main Streamlit application file
├── requirements.txt        # Python dependencies
├── retail_db.sqlite        # The SQLite database
├── churn_model.pkl         # The trained churn prediction model
├── scaler.pkl              # The feature scaler for the model
├── model_columns.txt       # The column order for the model
├── scripts/                # Directory for all the project's scripts
│   ├── generate_data.py    # Generates the retail data
│   ├── etl_process.py      # A simple ETL script
│   ├── run_analytics.py    # A script to run some analytics
│   ├── churn_prediction.py # Trains the churn prediction model
│   └── test_model.py       # Tests the churn model with a generated dataset
└── data/                   # Directory for the data files
    ├── retail_data.csv
    └── ...
```
