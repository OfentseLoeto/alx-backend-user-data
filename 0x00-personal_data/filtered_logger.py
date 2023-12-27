#!/usr/bin/env python3
"""
Obfuscate specified fields in the log message
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscate specified fields in the log message.

    Arguments:
    - fields (List[str]): A list of strings representing fields to obfuscate.
    - redaction (str): A string representing the value by which the field
                       will be obfuscated.
    - message (str): A string representing the log line.
    - separator (str): A string representing the character used to separate
                       fields in the log line.

    Returns:
    - str: The obfuscated log message.
    """
    # Creating a regular expression pattern to match the specified fields
    pattern = re.compile(
        fr'({"|".join(map(re.escape, fields))})=[^{separator}]+'
    )

    # Using re.sub to perform the substitution with a single regex
    obfuscated_message = pattern.sub(fr'\1={redaction}', message)
    return obfuscated_message
