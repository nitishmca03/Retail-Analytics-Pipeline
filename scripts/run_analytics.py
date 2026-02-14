import pandas as pd
import sqlite3
import os

def run_analytics(db_file="retail_db.sqlite", output_dir="data", output_file="monthly_analysis.csv"):
    """
    Connects to the SQLite database, calculates monthly revenue, profit, and MoM growth,
    and saves the results to a CSV file.
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

    query = """
    WITH MonthlySales AS (
        SELECT
            strftime('%Y-%m', TransactionDate) AS SalesMonth,
            SUM(Quantity * Price) AS Revenue,
            SUM(Quantity * Price * 0.3) AS Profit  -- Assuming a 30% profit margin
        FROM
            transactions
        GROUP BY
            SalesMonth
    )
    SELECT
        SalesMonth,
        Revenue,
        Profit,
        (Revenue - LAG(Revenue, 1, 0) OVER (ORDER BY SalesMonth)) * 100.0 / LAG(Revenue, 1, Revenue) OVER (ORDER BY SalesMonth) AS MoM_Revenue_Growth_Percentage
    FROM
        MonthlySales
    ORDER BY
        SalesMonth;
    """

    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        print("Successfully executed analytics query.")
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.close()
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, output_file)
    try:
        df.to_csv(output_path, index=False)
        print(f"Successfully saved monthly analysis to {output_path}")
    except Exception as e:
        print(f"Error saving output file: {e}")

if __name__ == "__main__":
    run_analytics()
    """
    This script connects to a SQLite database, `retail_db.sqlite`, which is expected to contain a `transactions` table.
    It calculates the monthly revenue and profit from the sales data.
    The profit is estimated as 30% of the revenue.

    The script uses a Common Table Expression (CTE) to first aggregate sales data into monthly summaries.
    Then, it uses the `LAG` window function to calculate the Month-over-Month (MoM) revenue growth percentage.

    The final analysis, including the sales month, total revenue, estimated profit, and MoM growth,
    is saved to a CSV file named `monthly_analysis.csv` in the `data/` directory.
    """
