import mysql.connector
import pandas as pd
from typing import Tuple, Dict

def connect_to_mysql(host: str, user: str, password: str, database: str):
    """
    Establish a connection to the MySQL database.
    
    :param host: Hostname of the MySQL server
    :param user: Username to log into the MySQL server
    :param password: Password to log into the MySQL server
    :param database: Name of the database to connect to
    :return: MySQL connection object
    """
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

def execute_query(conn, query: str) -> pd.DataFrame:
    """
    Execute a query and return the result as a pandas DataFrame.
    
    :param conn: MySQL connection object
    :param query: SQL query to execute
    :return: Resulting DataFrame
    """
    return pd.read_sql(query, conn)

def compare_query_results(
    conn, 
    actual_query: str, 
    generated_query: str
) -> Dict[str, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Execute actual and generated SQL queries and compare their results.
    
    :param conn: MySQL connection object
    :param actual_query: The actual SQL query to execute
    :param generated_query: The generated SQL query to execute
    :return: Dictionary with the SQL queries and a tuple of DataFrames (actual, generated, comparison)
    """
    actual_df = execute_query(conn, actual_query)
    generated_df = execute_query(conn, generated_query)
    
    comparison_df = actual_df.compare(generated_df, keep_shape=True, keep_equal=True)
    
    result_dict = {
        'actual_query': actual_df,
        'generated_query': generated_df,
        'comparison': comparison_df
    }
    
    return result_dict

def main():
    # MySQL connection parameters
    host = "localhost"
    user = "root"
    password = "admin@123"
    host = "localhost"
    port ="3306"
    database = "classicmodels"

    
    # Connect to the database
    conn = connect_to_mysql(host, user, password, database)
    
    # Define your actual and generated queries
    actual_query = "SELECT * FROM Customers;"
    generated_query = """WITH EmployeeCount AS ( 
  SELECT reportsTo, COUNT(*) AS count 
  FROM employees 
  WHERE reportsTo IS NOT NULL 
  GROUP BY reportsTo 
), 
MaxCount AS ( 
  SELECT MAX(count) AS maxCount 
  FROM EmployeeCount 
) 
SELECT e.* 
FROM employees e 
JOIN EmployeeCount ec ON e.employeeNumber = ec.reportsTo 
JOIN MaxCount mc ON ec.count = mc.maxCount;"""
    
    # Compare the query results
    result = compare_query_results(conn, actual_query, generated_query)
    
    # Print the results
    print("Actual Query Result:")
    print(result['actual_query'])
    
    print("Generated Query Result:")
    print(result['generated_query'])
    
    print("Comparison Result:")
    print(result['comparison'])
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
