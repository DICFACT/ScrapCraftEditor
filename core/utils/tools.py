"""..."""
import re
import typing as t


def to_system_name(name: str):
    """Converts name so you can use it in paths without any problem"""
    name = '_'.join(map(str.lower, name.split(' ')))
    name = re.sub(r'[()\-]', '_', name)
    name = re.sub(r'[^A-Za-z0-9_]', '', name)
    return name
