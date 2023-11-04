#!/usr/bin/env python3
"""
The function that returns the log message obfuscated
"""
import logging
import re


class RedactingFormatter(logging.Formatter):

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        """
        init method
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        - The format method uses the filter_datum function to filter values
          in incoming log records.
        - It passes the fields to filter as well as the REDACTION and
          SEPARATOR class attributes.

        - The log message in the record is updated with the filtered message
          using filter_datum.
        - The formatted log message is then returned using the parent class's
          format method.
        """
        message = record.getMessage()
        if self.fields:
            for field in self.fields:
                message = self.filter_datum(field, self.REDACTION, message,
                                            self.SEPARATOR)
        record.msg = message
        return super(RedactingFormatter, self).format(record)

    def filter_datum(self, field, redaction, message, separator):
        """
        Obfuscate specified fields in a log message using a regular
        expression.
        """
        regex_pattern = f'{re.escape(field)}=[^{re.escape(separator)}]+'
        return re.sub(regex_pattern, f'{field}={redaction}', message)
