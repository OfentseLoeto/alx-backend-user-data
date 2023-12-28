#!/usr/bin/env python3
"""
Main file
"""

from filtered_logger import get_db
import os

# Retrieve database credentials from environment variables
db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
db_name = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")

# Call the get_db function with retrieved credentials
db = get_db(db_username, db_password, db_host, db_name)

cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()
