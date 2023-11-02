#!/usr/bin/env python3
'0. Regex-ing'

import re
from typing import List
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''filter values in incoming log records using filter_datum'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    ''' returns the log message obfuscated'''
    for i in fields:
        pattern = fr'{re.escape(i)}=(.*?){re.escape(separator)}'
        message = re.sub(pattern, f'{i}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    '''returns a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel = logging.INFO
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(hdlr)
    return logger
