0-Write a function called filter_datum that returns the log message obfuscated:

.Arguments:
 >fields: a list of strings representing all fields to obfuscate
 >redaction: a string representing by what the field will be obfuscated
 >message: a string representing the log line
 >separator: a string representing by which character is separating all fields in the log line (message)
.The function should use a regex to replace occurrences of certain field values.
.filter_datum should be less than 5 lines long and use re.sub to perform the substitution with a single regex.

1-Use user_data.csv for this task

Implement a get_logger function that takes no arguments and returns a logging.Logger object.

The logger should be named "user_data" and only log up to logging.INFO level. It should not propagate messages to other loggers. It should have a StreamHandler with RedactingFormatter as formatter.

Create a tuple PII_FIELDS constant at the root of the module containing the fields from user_data.csv that are considered PII. PII_FIELDS can contain only 5 fields - choose the right list of fields that can are considered as “important” PIIs or information that you must hide in your logs. Use it to parameterize the formatter.

Tips:

What Is PII, non-PII, and personal data?
Uncovering Password Habits

2-Database credentials should NEVER be stored in code or checked into version control. One secure option is to store them as environment variable on the application server.

In this task, you will connect to a secure holberton database to read a users table. The database is protected by a username and password that are set as environment variables on the server named PERSONAL_DATA_DB_USERNAME (set the default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default as an empty string) and PERSONAL_DATA_DB_HOST (set the default as “localhost”).

The database name is stored in PERSONAL_DATA_DB_NAME.

Implement a get_db function that returns a connector to the database (mysql.connector.connection.MySQLConnection object).

.Use the os module to obtain credentials from the environment
.Use the module mysql-connector-python to connect to the MySQL database (pip3 install mysql-connector-python)

3-Implement a main function that takes no arguments and returns nothing.

The function will obtain a database connection using get_db and retrieve all rows in the users table and display each row under a filtered format like this:

Filtered fields:

.name
.email
.phone
.ssn
password
Only your main function should run when the module is executed.

4-User passwords should NEVER be stored in plain text in a database.

Implement a hash_password function that expects one string argument name password and returns a salted, hashed password, which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw).

5-Implement an is_valid function that expects 2 arguments and returns a boolean.

Arguments:

.hashed_password: bytes type
.password: string type
Use bcrypt to validate that the provided password matches the hashed password
