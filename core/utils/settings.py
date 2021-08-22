"""
This module contains anything you need to create your own settings.
This settings can be loaded from file using any loader, can be saved
and edited. All of these comes with dynamic type checking, needed to
make sure that all your settings have expected type.
"""

import typing as t
import yaml

from .dynamic_typing import check_type


class Field(t.NamedTuple):
    """Setting field"""
    type: t.Any
    default: t.Any


class Settings:
    """
    Class that represents settings. Settings is a set of fields, that in this case
    implemented as dictionary, where key is setting name and value - field it self.
    Fields contain information about what setting type and default value are.
    This information can not be changed after initialization.

    Settings object can as well load user settings, that will redefine defaults.
    All types will be dynamical checked to prevent any unexpected errors.
    """

    def __init__(self, fields: dict[str, Field]):
        # This dictionary contains only user defined settings that passed type checking
        # That means you can not find all settings here, but only redefined by user
        self.__settings = {}

        self.__fields = fields

    def get(self, key: str):
        """
        Returns value for setting with a given name. If key that you
        passed is not specified in defaults - raises KeyError

        :param key: name of the setting
        :return: setting value
        """
        # KeyError generates in self.__fields[key] then there is no such key
        return self.__settings.get(key, self.__fields[key].default)

    def load_object(self, obj: dict, override: bool = True):
        """
        Loads settings from given dictionary. If it has unexpected structure
        (including types of values that appeared to be different from expected) TypeError
        will be raised.

        :param obj:
        :param override:
        :return: None
        """

        # Checking type of each item in given dictionary
        loaded = {}
        for key, value in obj.items():
            field = self.__fields.get(key)
            if not isinstance(field, Field):
                raise KeyError(f"Got unexpected setting name: {key}")
            check_type(value, field.type)
            loaded[key] = value

        # Updating settings
        if override:
            self.__settings.clear()
        self.__settings.update(loaded)

    def load(self, path: str, loader=yaml.safe_load, override: bool = True):
        """
        Loads settings from the file using given loader (yaml.safe_load by default).
        Does not handle errors that occurred while loading the file, leaving it up to you.
        If file not well structured, then its problem of a loader and that's on it side to decide
        raise error or not. On the other hand, if parsed object has unexpected structure
        (including types of values that appeared to be different from expected) TypeError
        will be raised.

        :param path: path to file to load
        :param loader: function to parse file contents
        :param override: if set to False will load on top of already loaded settings
        :return: None
        """
        # TODO: Сделать класс LoadManager, который позволит загружать объекты, ориентируясь по их расширению
        with open(path, 'rt') as file:
            content = loader(file)
        if not isinstance(content, dict) and content is not None:
            raise TypeError(f"File {path} contains unexpected structure (expected dict)")
        self.load_object(content or {}, override)

    def change_setting(self, key: str, value: t.Any):
        """
        Sets new value to given setting. The passed value will be checked against the required type.
        If types are different - TypeError will be raised. If key does not exists - KeyError will be raised.

        :param key: name of the setting
        :param value: value that needs to be set
        """
        field = self.__fields[key]
        check_type(value, field.type)  # TypeError if the values don't match
        self.__settings[key] = value
