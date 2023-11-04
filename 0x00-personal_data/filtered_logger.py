#!/usr/bin/env python3
"""
The function that returns the log message obfuscated
"""
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscate specified fields in a log message using a regular
    expression.

    Args:
        fields (list of str): A list of strings representing
        fields to obfuscate.

    redaction (str): A string representing the value by which the
                    fields will be obfuscated.

    message (str): A string representing the log line.

    separator (str): A string representing the character that
                    separates fields in the log message.

    Returns:
            str: The log message with specified fields obfuscated.
    Example
    >>> filter_datum(['password', 'credit_card'], '***REDACTED***'
    ... 'User login: theo, password: 1234, credit_card: 12345678'
        ', ')
    'User login: theo, password: ***REDACTED***, credit_card:
    ***REDACTED***',
    """
    regex_pattern = '|'.join(map(re.escape, fields))
    regex = f'({regex_pattern})(?={re.escape(separator)})'
    return re.sub(regex, redaction, message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
