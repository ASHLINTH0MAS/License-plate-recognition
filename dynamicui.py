import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pyodbc
import os

def run_npr():
    # Code to run npr.py
    os.system('python npr.py')

def show_dataset():
    dataset_window = tk.Toplevel()
    dataset_window.title("Detected Plates Dataset")
    tree = ttk.Treeview(dataset_window, columns=("Plate Number", "Date", "Time"), show="headings")
    tree.heading("Plate Number", text="Plate Number")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")

    # Database connection details
    server_name = 'LAPTOP-K2HEN4CR'
    database_name = 'db'
    table_name = 'nprtable'

    # Establish connection to the SSMS database using Windows authentication
    conn = pyodbc.connect(
        f'DRIVER=ODBC Driver 17 for SQL Server;'
        f'SERVER={server_name};'
        f'DATABASE={database_name};'
        'Trusted_Connection=yes;'
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Fetch the data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=(row.PlateNumber, row.DetectionDate, row.DetectionTime))

    tree.pack(fill=tk.BOTH, expand=True)

    # Close the cursor and connection
    cursor.close()
    conn.close()

def search_by_time():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    if not start_date or not end_date or not start_time or not end_time:
        messagebox.showwarning("Error", "Please enter valid start and end dates and times.")
        return

    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
        datetime.strptime(start_time, '%H:%M:%S')
        datetime.strptime(end_time, '%H:%M:%S')
        start_datetime = datetime.strptime(start_date + " " + start_time, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(end_date + " " + end_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        messagebox.showwarning("Error", "Invalid date or time format.")
        return

    if start_datetime >= end_datetime:
        messagebox.showwarning("Error", "End date and time should be greater than start date and time.")
        return

    search_window = tk.Toplevel()
    search_window.title(f"Detected Plates Dataset ({start_date} {start_time} - {end_date} {end_time}")
    tree = ttk.Treeview(search_window, columns=("Plate Number", "Date", "Time"), show="headings")
    tree.heading("Plate Number", text="Plate Number")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")

    # Database connection details
    server_name = 'LAPTOP-K2HEN4CR'
    database_name = 'db'
    table_name = 'nprtable'

    # Establish connection to the SSMS database using Windows authentication
    conn = pyodbc.connect(
        f'DRIVER=ODBC Driver 17 for SQL Server;'
        f'SERVER={server_name};'
        f'DATABASE={database_name};'
        'Trusted_Connection=yes;'
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Fetch the data from the table within the specified time range
    cursor.execute(f"SELECT * FROM {table_name} WHERE DetectionDate >= ? AND DetectionDate <= ? "
                   f"AND DetectionTime >= ? AND DetectionTime <= ?",
                   start_date, end_date, start_time, end_time)
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=(row.PlateNumber, row.DetectionDate, row.DetectionTime))

    tree.pack(fill=tk.BOTH, expand=True)

    # Close the cursor and connection
    cursor.close()
    conn.close()

# Create main window
root = tk.Tk()
root.title("License Plate Detection System")

# Create a dashboard
dashboard = ttk.Notebook(root)
dashboard.pack(fill=tk.BOTH, expand=True)

# NPR Section
npr_frame = ttk.Frame(dashboard)
dashboard.add(npr_frame, text="Live Capturing")

run_button = tk.Button(npr_frame, text="Run NPR", command=run_npr)
run_button.pack(pady=10)

# NPR Dataset Section
dataset_frame = ttk.Frame(dashboard)
dashboard.add(dataset_frame, text="Database")

show_button = tk.Button(dataset_frame, text="Stored data", command=show_dataset)
show_button.pack(pady=10)

# NPR Search Section
search_frame = ttk.Frame(dashboard)
dashboard.add(search_frame, text="Search")

# Add date range option
date_frame = tk.Frame(search_frame)
date_frame.pack(pady=5)

start_date_label = tk.Label(date_frame, text="Start date (YYYY-MM-DD):")
start_date_label.pack(side=tk.LEFT)

start_date_entry = tk.Entry(date_frame)
start_date_entry.pack(side=tk.LEFT, padx=5)

end_date_label = tk.Label(date_frame, text="End date (YYYY-MM-DD):")
end_date_label.pack(side=tk.LEFT)

end_date_entry = tk.Entry(date_frame)
end_date_entry.pack(side=tk.LEFT, padx=5)

# Add time range option
time_frame = tk.Frame(search_frame)
time_frame.pack(pady=5)

start_time_label = tk.Label(time_frame, text="Start time (HH:MM:SS):")
start_time_label.pack(side=tk.LEFT)

start_time_entry = tk.Entry(time_frame)
start_time_entry.pack(side=tk.LEFT, padx=5)

end_time_label = tk.Label(time_frame, text="End time (HH:MM:SS):")
end_time_label.pack(side=tk.LEFT)

end_time_entry = tk.Entry(time_frame)
end_time_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_by_time)
search_button.pack(pady=10)

# Configure window to auto adjust contents
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Make windows resizable
root.resizable(True, True)

root.mainloop()
