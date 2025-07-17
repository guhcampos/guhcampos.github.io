"""
Johnny Decimal related utilities.
"""

import re


def strip_jdecimal_id(s: str) -> str:
    """
    Strip a Johnny Decimal ID from a string. Useful for publishing Johnny Decimal
    organized notes and content to the website without the organization clutter.
    """
    return re.sub(r"^\d+(\.\d+)+\s", "", s)
