#!/usr/bin/env python3
'0. Regex-ing'

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    ''' returns the log message obfuscated'''
    for i in fields:
        pattern = fr'{re.escape(i)}=(.*?){re.escape(separator)}'
        message = re.sub(pattern, f'{i}={redaction}{separator}', message)
    return message
