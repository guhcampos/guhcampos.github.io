"""
Johnny Decimal related utilities.

I use a personal flavor of Johnny Decimal (https://johnnydecimal.com/) to
organize my notes and content in general, and this module contains some utilities
to facilitate publishing this content to the website.
"""

import re


def strip_jdecimal_id(s: str) -> str:
    """
    Strip a Johnny Decimal ID from a string. Useful for publishing Johnny Decimal
    organized notes and content to the website without the organization clutter.
    """
    return re.sub(r"^\d+(\.\d+)+\s", "", s)
