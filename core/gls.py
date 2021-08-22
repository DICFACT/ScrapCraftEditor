"""..."""
import os

from core.utils.settings import Settings, Field


WINDOW_SETTINGS = "core/window_settings.yaml"
SETTINGS = "settings.yaml"

APP_INFO = {
    "app_name": 'ScrapCraftEditor',
    "version_id": 0,
    "version": 'alpha 1.0 dev main',
    "author": 'DicfactSoft'
}


# SCRAP MECHANIC RELATED
JSON_FILES_COMMENT = 'Generated by ScrapCraftEditor, free open source ScrapMechanic tool ' \
                     '(check it here ...)'
# ######################


# This is a part, that contains all global settings for this program
# Here you can specify new setting by defining its name, type and default value
# To do so you need to add another item to dictionary below as follows:
#
# <setting_name: str>: settings.Field(<type: Any>, <default_value: Any>)
#
# To use set value, you can use get method:
#
# Settings.get(<key: str>)
#
# Only strings can be used as keys. To define a type of a field you can use basic types as
# int, str, float, list as well as construct more complex using Optional, Union, Literal, Any
# Good luck!

window_settings = Settings({
    "main_window_title": Field(str, "{app_name} {version} by {author}"),
    "default_geometry": Field(list[int], [400, 650])
})

settings = Settings({
    "game_root": Field(str, r"C:\Program Files (x86)\Steam\steamapps\common\Scrap Mechanic"),
    "default_project_path": Field(str, r"$SMCE/projects")
})