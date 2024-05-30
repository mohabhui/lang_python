## Summary

**Python Script: CSV to SQLite Query Processor**
**Author:** mohabhui
**Date:** 12-Mar-2024

This Python script provides functionality to process CSV files using SQL queries by leveraging SQLite. It includes utilities to dynamically change date formats within strings and manage the conversion and querying of CSV data. Below is a brief summary of the key functions and usage:

### Key Functions

1. **`change_date_format_in_string(text: str, from_format: str, to_format: str) -> str`**
   - Converts date formats within a given string from one format to another.
   - Uses regular expressions to identify and replace dates.
   - Parameters:
     - `text`: The original string containing dates.
     - `from_format`: The format of the dates in the original string.
     - `to_format`: The desired format for the dates.

2. **`sql_on_csvs_in_dir(csvSrc, sql_query, sql_query_date_format=None, date_col=None, date_col_date_format=None, isFirstRowColName=False, save_res_to_file=False)`**
   - Executes an SQL query on CSV files located in a directory or specified CSV file.
   - Loads CSV data into an in-memory SQLite database, allowing SQL operations.
   - Parameters:
     - `csvSrc`: Directory path containing CSV files or a specific CSV file path.
     - `sql_query`: SQL query string to execute.
     - `sql_query_date_format`: Format of the dates in the SQL query.
     - `date_col`: Name or index of the date column in the CSV files.
     - `date_col_date_format`: Format of the dates in the date column.
     - `isFirstRowColName`: Indicates if the first row of the CSV files contains column names.
     - `save_res_to_file`: Indicates if the query result should be saved to a file.

### Example Usage

This example demonstrates how to use the `sql_on_csvs_in_dir` function to run an SQL query on a CSV file:

```python
if __name__ == "__main__":
    # Example SQL query
    mySQL = "SELECT * FROM table0 WHERE Start_Date BETWEEN '1-Dec-2008' AND '15-Sep-2009';"
    # Path to the CSV file
    csvSrc = r'..\data\employees.csv'

    # Execute the SQL query on the CSV file
    sql_on_csvs_in_dir(
        csvSrc, 
        mySQL, 
        sql_query_date_format='%d-%b-%Y', 
        date_col='Start_Date', 
        date_col_date_format='%m/%d/%Y', 
        isFirstRowColName=True, 
        save_res_to_file=True
    )
```

This script is particularly useful for data analysts and developers who need to perform SQL queries on CSV data without setting up a full database. It also supports date format conversions and can handle multiple CSV files in a directory.