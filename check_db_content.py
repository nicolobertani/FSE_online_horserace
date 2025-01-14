import sqlite3

def check_db_content(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print the content of each table
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print("\n")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    db_path = 'db.sqlite3'
    check_db_content(db_path)