#!/usr/bin/env python3
"""
Obfuscate specified fields in the log message
"""
import os
import mysql.connector
import logging
import re
from logging import StreamHandler
from typing import List


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for obfuscating sensitive information in
    log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter with a list of fields to obfuscate.

        Arguments:
        - fields (List[str]): A list of strings representing fields to
                              obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating values for specified fields.

        Arguments:
        - record (logging.LogRecord): The log record to be formatted.

        Returns:
        - str: The obfuscated log message.
        """
        log_message = super().format(record)
        return self.filter_datum(
            self.fields, self.REDACTION, log_message, self.SEPARATOR
        )

    def filter_datum(self, fields: List[str], redaction: str,
                     message: str, separator: str) -> str:
        """
        Obfuscate specified fields in the log message.

        Arguments:
        - fields (List[str]): A list of strings representing fields to
                              obfuscate.
        - redaction (str): A string representing the value by which the field
                           will be obfuscated.
        - message (str): A string representing the log line.
        - separator (str): A string representing the character used to separate
                           fields in the log line.

        Returns:
        - str: The obfuscated log message.
        """
        return self.substitute_fields(fields, redaction, message, separator)

    def substitute_fields(self, fields: List[str], redaction: str,
                          message: str, separator: str) -> str:
        """
        Substitute specified fields with redaction in the log message.

        Arguments:
        - fields (List[str]): A list of strings representing fields to
                              substitute.
        - redaction (str): A string representing the value by which the field
                           will be substituted.
        - message (str): A string representing the log line.
        - separator (str): A string representing the character used to separate
                           fields in the log line.

        Returns:
        - str: The log message with specified fields substituted.
        """
        return re.sub(
            fr'({"|".join(map(re.escape, fields))})=[^{separator}]+',
            fr'\1={redaction}',
            message
        )


# Create a constant tuple PII_FIELDS containing the fields considered as PII
PII_FIELDS = ("name", "email", "phone", "ssn", "credit_card")


def get_logger() -> logging.Logger:
    """
    Create and configure a logger named "user_data" with specified settings.

    Returns:
    - logging.Logger: The configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    # Preventing messages from being propagated to other loggers
    logger.propagate = False

    # Creating a StreamHandler with RedactingFormatter
    stream_handler = StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    # NullHandler to suppress messages when no other suitable
    # handler is configured
    logger.addHandler(logging.NullHandler())

    return logger


def get_db():
    """
    Connect to the MySQL database using environment variables for credentials.

    Returns:
    - mysql.connector.connection.MySQLConnection: Database connector object.
    """

    # Retrieve database credentials from environmental variables
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")

    # Creating a connection to mysql database
    connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
    )

    return connection
