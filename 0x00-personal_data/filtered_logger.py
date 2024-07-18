#!/usr/bin/env python3
'''Regex-ing in python'''
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                message, self.SEPARATOR)


def filter_datum(fields, redaction, message, separator):
    '''Regex-ing in python'''
    for field in fields:
        message = re.sub(
            rf'{field}=.*?{separator}',
            f'{field}={redaction}{separator}', message
            )
    return message
