"""
...
"""
import os
import typing as t
from contextlib import suppress

from core import scrap_mechanic as sm, gls
from core.utils import tools


class CopyInfo(t.NamedTuple):
    """..."""
    src: str
    dst: str


class ProjectTemplate(t.NamedTuple):
    """..."""
    clone_from: t.Optional[str]
    copy_files: list[CopyInfo]


INSTALLATION_INFO = CopyInfo(
    src='$PROJECT/Scrap Mechanic',
    dst='$SM_ROOT'
)

PT_GAME_FILES = ProjectTemplate(
    clone_from=None,
    copy_files=[
        # Icons
        CopyInfo(
            src='$SM_ROOT/Data/Gui/IconMap.xml',
            dst='$PROJECT/res/IconMap.xml'
        ),
        CopyInfo(
            src='$SM_ROOT/Data/Gui/IconMap.png',
            dst='$PROJECT/res/IconMap.png'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/Gui/IconMapSurvival.xml',
            dst='$PROJECT/res/IconMapSurvival.xml'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/Gui/IconMapSurvival.png',
            dst='$PROJECT/res/IconMapSurvival.png'
        ),

        # Items
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/item_names.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/item_names.json'
        ),

        # Craftbots
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/cookbot.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/cookbot.json'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/craftbot.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/craftbot.json'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/dispenser.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/dispenser.json'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/dressbot.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/dressbot.json'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/hideout.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/hideout.json'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/refinery.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/refinery.json'
        ),
        CopyInfo(
            src='$SM_ROOT/Survival/CraftingRecipes/workbench.json',
            dst='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/workbench.json'
        ),
    ]
)
PT_DEFAULT = ProjectTemplate(
    clone_from='core/res/project_templates/Default',
    copy_files=[]
)
PT_EMPTY = ProjectTemplate(
    clone_from='core/res/project_templates/Empty',
    copy_files=[]
)


class Project:
    """..."""
    PROJECT_NAME_DEFAULT = 'Unnamed'
    AUTHOR_DEFAULT = 'Unknown'

    RECENT_PROJECTS_FILE = 'user/_temp/recent.txt'
    RECENT_PROJECTS_COUNT = 10

    def __init__(self):
        self.__project_name: str = self.PROJECT_NAME_DEFAULT
        self.__project_path: str = ''
        self.__author: str = self.AUTHOR_DEFAULT

        self.__is_directly_loaded: bool = False

    @property
    def name(self):
        """..."""
        return self.__project_name

    @property
    def author(self):
        """..."""
        return self.__author

    @property
    def loaded_directly(self):
        """..."""
        return self.__is_directly_loaded

    def _init_resources(self):
        sm.resource_loader.load_image_set('$PROJECT/res/IconMap.xml')
        sm.resource_loader.load_image_set('$PROJECT/res/IconMapSurvival.xml')

        sm.craft_editor.load_items()

        sm.craft_editor.load_recipes(sm.COOKBOT)
        sm.craft_editor.load_recipes(sm.CRAFTBOT)
        sm.craft_editor.load_recipes(sm.DISPENSER)
        sm.craft_editor.load_recipes(sm.DRESSBOT)
        sm.craft_editor.load_recipes(sm.HIDEOUT)
        sm.craft_editor.load_recipes(sm.REFINERY)
        sm.craft_editor.load_recipes(sm.WORKBENCH)

    def _add_to_recent(self):
        recent = []
        with suppress(OSError), open(self.RECENT_PROJECTS_FILE, 'rt') as file:
            recent = list(map(str.strip, file.readlines()))
        if self.__project_path in recent:
            recent.remove(self.__project_path)
        recent.append(self.__project_path)
        if len(recent) > self.RECENT_PROJECTS_COUNT:
            del recent[-1]
        with open(self.RECENT_PROJECTS_FILE, 'wt') as file:
            file.write('\n'.join(recent))

    def get_recent(self):
        """..."""
        recent = []
        with suppress(OSError), open(self.RECENT_PROJECTS_FILE, 'rt') as file:
            recent = list(filter(os.path.exists, map(str.strip, file.readlines())))
        return list(reversed(recent))

    def new(self, project_name: str, system_name: str, author: str, path: str, template: ProjectTemplate):
        """..."""
        import shutil
        from os.path import join
        import json

        # SETTING UP SOME THINGS ############################
        self.__is_directly_loaded = False
        self.__project_name = project_name
        self.__project_path = os.path.normpath(join(path, system_name))
        self.__author = author

        os.environ['PROJECT'] = self.__project_path

        self._add_to_recent()
        # ###################################################

        os.makedirs(self.__project_path, exist_ok=True)

        if template.clone_from is not None:
            shutil.copytree(template.clone_from, self.__project_path, dirs_exist_ok=True)

        for copy_info in template.copy_files:
            dst = os.path.expandvars(copy_info.dst)

            dst_dir = dst
            if not os.path.isdir(dst_dir):
                dst_dir = os.path.split(dst)[0]
            os.makedirs(dst_dir, exist_ok=True)

            src = os.path.expandvars(copy_info.src)
            shutil.copy(src, dst)

        info_file_path = join(self.__project_path, 'info.json')
        with open(info_file_path, 'wt') as file:
            json.dump({
                'project_name': self.__project_name,
                'author': self.__author
            }, file, indent=4)

        self._init_resources()

    def load(self, path: str):
        """..."""
        import json
        from os.path import join

        info_file_path = join(path, 'info.json')
        with open(info_file_path, 'rt') as file:
            info = json.load(file)

        project_name = info.get('project_name', self.PROJECT_NAME_DEFAULT)
        author = info.get('author', self.AUTHOR_DEFAULT)

        # SETTING UP SOME THINGS ############################
        self.__is_directly_loaded = False
        self.__project_name = project_name
        self.__project_path = os.path.normpath(path)
        self.__author = author

        os.environ['PROJECT'] = self.__project_path

        self._add_to_recent()
        # ###################################################

        self._init_resources()

    def load_gf(self):
        """..."""
        project_name = 'GameFiles'
        self.new(
            project_name,
            tools.to_system_name(project_name),
            self.AUTHOR_DEFAULT,
            'user/_temp',
            PT_GAME_FILES
        )
        self.__is_directly_loaded = True

    def save(self):
        """..."""
        sm.craft_editor.build(message=gls.JSON_FILES_COMMENT)

    def install(self):
        """..."""
        import shutil
        self.save()
        dst = os.path.expandvars(INSTALLATION_INFO.dst)
        src = os.path.expandvars(INSTALLATION_INFO.src)
        shutil.copytree(src, dst, dirs_exist_ok=True)


Project = Project()
