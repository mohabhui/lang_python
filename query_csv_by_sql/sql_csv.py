'''
---------------------
python 3
Author: mohabhui
Date: 12-Mar-2024
---------------------
'''

import pandas as pd
import sqlite3
import os
from glob import glob
from datetime import datetime
import re


def change_date_format_in_string(text: str, from_format: str, to_format: str) -> str:
    """
    Changes the date format in a given string based on a known `from_format` to another format `to_format`.

    :param text: The original string containing one or more dates
    :param from_format: The format to parse the date from
    :param to_format: The format to convert the date to
    :return: String with all matching dates reformatted
    """
    # Mapping of date format directives to regex equivalents
    pattern_map = {
        '%d': r'(\d{1,2})',      # Day of the month (1-31)
        '%m': r'(\d{1,2})',      # Month as a number (1-12)
        '%b': r'([A-Za-z]{3})',  # Month as a short name (Jan, Feb, ...)
        '%B': r'([A-Za-z]+)',    # Full month name (January, February, ...)
        '%Y': r'(\d{4})',        # Four-digit year
        '%y': r'(\d{2})'         # Two-digit year
    }

    # Build the regex pattern dynamically from the `from_format`
    regex_pattern = re.escape(from_format)
    for key, value in pattern_map.items():
        regex_pattern = regex_pattern.replace(re.escape(key), value)

    # Compile the final regex pattern
    date_pattern = re.compile(regex_pattern)

    # Function to replace the date format within the main text
    def replace_match(match):
        date_str = match.group(0)
        parsed_date = datetime.strptime(date_str, from_format)
        return parsed_date.strftime(to_format)

    # Substitute all matches of the original date format with the target format
    updated_text = date_pattern.sub(replace_match, text)

    return updated_text


def sql_on_csvs_in_dir(csvSrc, sql_query, sql_query_date_format=None, date_col=None, date_col_date_format=None, isFirstRowColName=False, save_res_to_file=False):
    """
    In this function, csvSrc (CSV Source) is the directory containing the CSV files or
    path of a CSV file, and sql_query is the SQL query string you want to
    execute on these files. The CSV files are loaded into the SQLite database
    with table names table0, table1, etc. If isFirstRowColName is True, the
    first row of the CSV files will be used as column names. Otherwise, the
    columns within these tables are named col0, col1, etc. You can refer to
    these tables and columns using these names in your SQL queries.

    CSV files will be mapped alphabetically as table0, table1, etc., and the
    columns of each CSV file will be named according to the first row if
    isFirstRowColName is True, or as col0, col1, etc., as per their index otherwise.

    If the column name has space, the column name should be in double quote inside
    the SQL. The double quote, inside the double quote should be escaped as below

    mySQL = "SELECT * FROM table0 WHERE \"Start Date\" BETWEEN '1-Dec-2008' AND '15-Sep-2009';"


    """


    # Connect to an in-memory SQLite database
    conn = sqlite3.connect(':memory:')

    # Check if csvSrc is a directory or a file
    if os.path.isdir(csvSrc):
        # If it's a directory, get all CSV file paths and sort them alphabetically
        csv_files = sorted(glob(os.path.join(csvSrc, '*.csv')))
    elif os.path.isfile(csvSrc) and csvSrc.endswith('.csv'):
        # If it's a file, work only with that file
        csv_files = [csvSrc]
    else:
        raise ValueError("csvSrc must be a directory path or a CSV file path.")



    # Iterate over sorted CSV files and load each into the SQLite database
    for i, filepath in enumerate(csv_files):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath, header=0 if isFirstRowColName else None)

        # If isFirstRowColName is False, rename columns to col0, col1, col2, ...
        if not isFirstRowColName:
            df.columns = [f'col{j}' for j in range(len(df.columns))]

            if date_col is not None and type(date_col) == str:
                date_col = int(date_col[3:]) # if date_col = 'col0' or date_col = 'col1' etc

        # Convert date column if specified
        if date_col is not None and date_col_date_format is not None:

            # Determine the date column's name or index
            date_column = date_col if isFirstRowColName else f'col{date_col}'
            # Convert dates to SQLite-compatible format
            df[date_column] = pd.to_datetime(df[date_column], format=date_col_date_format).dt.strftime('%Y-%m-%d')


        # Construct table name based on index: table0, table1, ...
        tablename = f'table{i}'

        # Load the DataFrame into the SQLite database
        df.to_sql(tablename, conn, if_exists='replace', index=False)

    if sql_query_date_format is not None:
        sql_query = change_date_format_in_string(sql_query, sql_query_date_format, '%Y-%m-%d')

    # Execute the SQL query
    df_query_result = pd.read_sql_query(sql_query, conn)
    df_query_result = round(df_query_result, 2)

    conn.close()

    print(df_query_result)

    if save_res_to_file:
        # Generate the file name for the output CSV
        dirName = os.path.basename(os.path.normpath(csvSrc))
        existing_files = glob(dirName + '_' + 'query_result_*.csv')

        highest_num = max(
            [int(fname.split('_')[-1].split('.')[0]) for fname in existing_files] + [0]
        )

        output_filename = f'{dirName}_query_result_{highest_num + 1}.csv'

        # Export the query result to a CSV file
        df_query_result.to_csv(output_filename, index=False)

        print(f'Result File: {output_filename}')


# Example usage
if __name__ == "__main__":


    # When the csv file has column name.
    mySQL = "SELECT * FROM table0 WHERE Start_Date BETWEEN '1-Dec-2008' AND '15-Sep-2009';"

    csvSrc = r'..\data\employees.csv'

    sql_on_csvs_in_dir(csvSrc, mySQL, sql_query_date_format='%d-%b-%Y', date_col= 'Start_Date', date_col_date_format='%m/%d/%Y', isFirstRowColName=True, save_res_to_file=True)

