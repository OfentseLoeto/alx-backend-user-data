#!/usr/bin/env python3
"""
The function that returns the log message obfuscated
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specified fields in a log message using a regular expression.

    Args:
        fields (list of str): A list of strings representing fields to
        obfuscate.

        redaction (str): A string representing the value by which the fields
        will be obfuscated.

        message (str): A string representing the log line.

        separator (str): A string representing the character that separates
        fields in the log message.

        Returns:
                str: The log message with specified fields obfuscated.
    """

    regex_pattern = '|'.join(map(re.escape, fields))
    regex = f'({regex_pattern})(?={re.escape(separator)})'
    return re.sub(regex, redaction, message)
