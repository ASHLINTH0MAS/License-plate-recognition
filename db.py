import pyodbc
import csv

# Database connection details
server_name = 'LAPTOP-K2HEN4CR'
database_name = 'db'
table_name = 'nprtable'

# Open CSV file for reading
with open('number.csv', mode='r', encoding='utf-8-sig') as csv_file:
    reader = csv.DictReader(csv_file)

    # Establish connection to the SSMS database using Windows authentication
    conn = pyodbc.connect(
        f'DRIVER=ODBC Driver 17 for SQL Server;'
        f'SERVER={server_name};'
        f'DATABASE={database_name};'
        'Trusted_Connection=yes;'
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
    if cursor.fetchone() is None:
        # Create the table if it doesn't exist
        cursor.execute(f"CREATE TABLE {table_name} (PlateNumber VARCHAR(50), DetectionDate DATE, DetectionTime TIME)")

    # Prepare the SQL query to insert data into the table
    sql_query = f"INSERT INTO {table_name} (PlateNumber, DetectionDate, DetectionTime) VALUES (?, ?, ?)"

    for row in reader:
        plate_number = row['Plate Number']
        detection_date = row['Date']
        detection_time = row['Time']

        # Execute the SQL query with the values from the CSV file
        cursor.execute(sql_query, plate_number, detection_date, detection_time)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
