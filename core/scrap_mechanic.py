"""
...
"""
import json
import os
import typing as t
from contextlib import suppress
from dataclasses import dataclass


class Item(t.NamedTuple):
    """..."""
    name: str
    uuid: str


DEFAULT_ITEM = Item('blk_scrapwood', '1fc74a28-addb-451a-878d-c3c605d63811')


@dataclass
class ItemStack:
    """..."""
    item: Item
    quantity: int

    def copy(self):
        """..."""
        return ItemStack(self.item, self.quantity)

    def copy_to(self, other: 'ItemStack'):
        """..."""
        other.item = self.item
        other.quantity = self.quantity

    @staticmethod
    def default():
        """Creates default"""
        return ItemStack(DEFAULT_ITEM, 1)

    @staticmethod
    def from_dict(dct: dict, mapping: dict[str, Item]):
        """..."""
        return ItemStack(mapping.get(dct['itemId'], Item(' ', dct['itemId'])), dct['quantity'])

    @staticmethod
    def to_dict(stack: 'ItemStack'):
        """..."""
        return {'itemId': stack.item.uuid, 'quantity': stack.quantity}


@dataclass
class CraftbotRecipe:
    """..."""
    result: ItemStack
    craft_time: int
    ingredients: list[ItemStack]

    def copy(self):
        """..."""
        return CraftbotRecipe(self.result.copy(), self.craft_time, [i.copy() for i in self.ingredients])

    def copy_to(self, other: 'CraftbotRecipe'):
        """..."""
        other.result = self.result.copy()
        other.craft_time = self.craft_time
        other.ingredients = [i.copy() for i in self.ingredients]

    @staticmethod
    def default():
        """..."""
        return CraftbotRecipe(ItemStack.default(), 32, [ItemStack.default()])

    @staticmethod
    def load(raw: list, mapping: dict[str, Item]):
        """..."""
        result = []
        for recipe_raw in raw:
            ingredient_list = []
            for ingredient_raw in recipe_raw['ingredientList']:
                ingredient_list.append(ItemStack.from_dict(ingredient_raw, mapping))

            result.append(CraftbotRecipe(
                ItemStack.from_dict(recipe_raw, mapping),
                recipe_raw['craftTime'],
                ingredient_list
            ))

        return result

    @staticmethod
    def dump(recipes: t.Sequence['CraftbotRecipe']):
        """..."""
        result = []
        for recipe in recipes:
            ingredient_list = []
            for ingredient in recipe.ingredients:
                ingredient_list.append(ItemStack.to_dict(ingredient))

            dumped = ItemStack.to_dict(recipe.result)
            dumped.update({
                "craftTime": recipe.craft_time,
                "ingredientList": ingredient_list
            })
            result.append(dumped)

        return result


@dataclass
class DressbotRecipe:
    """..."""
    result: ItemStack
    reward: dict[t.Literal['tier'], t.Literal['Common', 'Rare', 'Epic']]
    craft_time: int
    ingredients: list[ItemStack]

    def copy(self):
        """..."""
        return DressbotRecipe(self.result.copy(), self.reward, self.craft_time, [i.copy() for i in self.ingredients])

    def copy_to(self, other: 'DressbotRecipe'):
        """..."""
        other.result = self.result.copy()
        other.reward = self.reward
        other.craft_time = self.craft_time
        other.ingredients = [i.copy() for i in self.ingredients]

    @staticmethod
    def default():
        """..."""
        return DressbotRecipe(ItemStack.default(), {'tier': 'Common'}, 32, [ItemStack.default()])

    @staticmethod
    def load(raw: list, mapping: dict[str, Item]):
        """..."""
        result = []
        for recipe_raw in raw:
            with suppress(KeyError):
                ingredient_list = []
                for ingredient_raw in recipe_raw['ingredientList']:
                    ingredient_list.append(ItemStack.from_dict(ingredient_raw, mapping))

                tier_val = recipe_raw['reward'].get('tier', 'Common')
                tier_val = tier_val if tier_val in ('Common', 'Rare', 'Epic') else 'Common'
                tier_val: t.Literal['Common', 'Rare', 'Epic']
                tier: t.Literal['tier'] = 'tier'

                result.append(DressbotRecipe(
                    ItemStack.from_dict(recipe_raw, mapping),
                    {tier: tier_val},
                    recipe_raw['craftTime'],
                    ingredient_list
                ))

        return result

    @staticmethod
    def dump(recipes: t.Sequence['DressbotRecipe']):
        """..."""
        result = []
        for recipe in recipes:
            ingredient_list = []
            for ingredient in recipe.ingredients:
                ingredient_list.append(ItemStack.to_dict(ingredient))

            dumped = ItemStack.to_dict(recipe.result)
            dumped.update({
                "reward": {'tier': recipe.reward if recipe.reward in ('Common', 'Rare', 'Epic') else 'Common'},
                "craftTime": recipe.craft_time,
                "ingredientList": ingredient_list
            })
            result.append(dumped)

        return result


@dataclass
class RefineryRecipe:
    """..."""
    result: ItemStack
    ingredient: Item

    def copy(self):
        """..."""
        return RefineryRecipe(self.result.copy(), self.ingredient)

    def copy_to(self, other: 'RefineryRecipe'):
        """..."""
        other.result = self.result.copy()
        other.ingredient = self.ingredient

    @staticmethod
    def default():
        """..."""
        return RefineryRecipe(ItemStack.default(), DEFAULT_ITEM)

    @staticmethod
    def load(raw: dict, mapping: dict[str, Item]):
        """..."""
        result = []
        for ingredient_uuid, result_raw in raw.items():
            with suppress(KeyError):
                result.append(RefineryRecipe(
                    ItemStack.from_dict(result_raw, mapping),
                    mapping[ingredient_uuid]
                ))
        return result

    @staticmethod
    def dump(recipes: t.Sequence['RefineryRecipe']):
        """..."""
        result = {}
        for recipe in recipes:
            result[recipe.ingredient.uuid] = ItemStack.to_dict(recipe.result)
        return result


DRESSBOT_REWARD_TIERS = {
    'Common': {'tier': 'Common'},
    'Rare': {'tier': 'Rare'},
    'Epic': {'tier': 'Epic'},
}


class Craftbot(t.NamedTuple):
    """..."""
    name: str
    uuid: str
    path: str
    recipe_class: t.Any  # Can be CraftbotRecipe, DressbotRecipe, RefineryRecipe or something else
    restrictions: int


class CraftbotRestrictions:
    """..."""
    NO_RESTRICTIONS = 0
    NO_RECIPE_ADDITION = 1
    NO_RESULT_EDITING = 2
    NO_INGREDIENT_EDITING = 4
    NO_INGREDIENT_ADDITION = 8


COOKBOT = Craftbot(
    name='CookBot',
    uuid='2af00456-b22e-4743-b338-a91934aba7c5',
    path='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/cookbot.json',
    recipe_class=CraftbotRecipe,
    restrictions=CraftbotRestrictions.NO_RECIPE_ADDITION |
                 CraftbotRestrictions.NO_RESULT_EDITING
)
CRAFTBOT = Craftbot(
    name='CraftBot',
    uuid='b63c6440-dfc2-4da7-acdb-3c385080b2e4',
    path='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/craftbot.json',
    recipe_class=CraftbotRecipe,
    restrictions=CraftbotRestrictions.NO_RESTRICTIONS
)
DISPENSER = Craftbot(
    name='Dispenser',
    uuid='ebd73cee-988f-4ffb-95d1-d3c3c81fd506',
    path='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/dispenser.json',
    recipe_class=CraftbotRecipe,
    restrictions=CraftbotRestrictions.NO_RECIPE_ADDITION |
                 CraftbotRestrictions.NO_RESULT_EDITING
)
DRESSBOT = Craftbot(
    name='DressBot',
    uuid='767a3121-2c31-473c-a5ab-27e188fdd55a',
    path='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/dressbot.json',
    recipe_class=DressbotRecipe,
    restrictions=CraftbotRestrictions.NO_RESTRICTIONS
)
HIDEOUT = Craftbot(
    name='Hideout',
    uuid='614c3193-13da-40f4-9b03-37f26e760fd6',
    path='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/hideout.json',
    recipe_class=CraftbotRecipe,
    restrictions=CraftbotRestrictions.NO_RESTRICTIONS
)
REFINERY = Craftbot(
    name='Refinery',
    uuid='5cb15c93-4fa9-48da-9974-2e95ca6c9e1c',
    path='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/refinery.json',
    recipe_class=RefineryRecipe,
    restrictions=CraftbotRestrictions.NO_INGREDIENT_EDITING |
                 CraftbotRestrictions.NO_INGREDIENT_ADDITION |
                 CraftbotRestrictions.NO_RECIPE_ADDITION
)
WORKBENCH = Craftbot(
    name='Workbench',
    uuid='2ff2b13f-5a50-443c-bbda-1f40f6aa917f',
    path='$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/workbench.json',
    recipe_class=CraftbotRecipe,
    restrictions=CraftbotRestrictions.NO_RESTRICTIONS
)


def load_minified_json(path: str):
    """Minifies and loads json files. Useful for loading json with comments"""
    import rjsmin
    import json

    with open(path, 'rt') as file:
        content = file.read()
    minified = rjsmin.jsmin(content)
    processed = json.loads(minified)
    return processed


class CraftEditor:
    """..."""
    item_names_file_path = '$PROJECT/Scrap Mechanic/Survival/CraftingRecipes/item_names.json'

    def __init__(self):
        self.__recipes: dict[Craftbot, list] = {}
        self.__items = []
        self.__items_by_name = {}
        self.__items_by_uuid = {}

    @property
    def recipes(self):
        """..."""
        return self.__recipes

    @property
    def items(self):
        """..."""
        return self.__items

    def load_items(self):
        """..."""
        uuid_to_name = load_minified_json(os.path.expandvars(self.item_names_file_path))
        self.__items = []
        for uuid, name in uuid_to_name.items():
            self.__items.append(Item(name, uuid))

        self.__items_by_name = {}
        self.__items_by_uuid = {}
        for item in self.__items:
            self.__items_by_name[item.name] = item
            self.__items_by_uuid[item.uuid] = item

    def get_item_by_name(self, name: str):
        """..."""
        return self.__items_by_name[name]

    def get_item_by_uuid(self, uuid: str):
        """..."""
        return self.__items_by_uuid[uuid]

    def load_recipes(self, craftbot: Craftbot):
        """..."""
        raw_recipe_data_list = load_minified_json(os.path.expandvars(craftbot.path))
        recipes = craftbot.recipe_class.load(raw_recipe_data_list, self.__items_by_uuid)
        self.__recipes[craftbot] = recipes
        return recipes

    def build(self, message: str = None):
        """..."""
        for craftbot, recipes in self.__recipes.items():
            print(f'{craftbot.name}..  ', end='')

            dumped_recipes = craftbot.recipe_class.dump(recipes)
            json_recipes = json.dumps(dumped_recipes, indent=4)

            with open(os.path.expandvars(craftbot.path), 'wt') as file:
                # Message at the top of json file
                if message:
                    file.write(f'// {message}\n')
                file.write(json_recipes)

            print('Done.')


craft_editor = CraftEditor()


class ResourceLoader:
    """..."""

    def __init__(self):
        self.__resources = {}

    @property
    def resources(self):
        """..."""
        return self.__resources

    def get(self, path: str, sep: str = '/'):
        """..."""
        comp = path.split(sep)
        res = self.__resources
        for item in comp:
            res = res[item]
        return res

    def load_image_set(self, path: str):
        """..."""
        from xml.dom import minidom
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import QRect
        from os.path import split, join

        def is_element(n):
            """Is node an instance of a DOM Element"""
            return isinstance(n, minidom.Element)

        def parse_size(s: str):
            """Converts a string representation of a size to tuple of ints"""
            return tuple(map(int, s.split()))

        combined = os.path.expandvars(path)

        with open(combined, 'rt', encoding='utf-8') as file:
            dom = minidom.parse(file)

        resource = dom.childNodes[0].getElementsByTagName('Resource')[0]
        resource_name = resource.attributes.get('name').value

        dir_path = split(combined)[0]

        groups = {}
        for group_ in filter(is_element, resource.childNodes):
            group_name = group_.attributes.get('name').value

            atlas_path = group_.attributes.get('texture').value
            size = parse_size(group_.attributes.get('size').value)

            atlas = QPixmap(join(dir_path, atlas_path))

            indexes = {}
            for index in filter(is_element, group_.childNodes):
                index_name = index.attributes.get('name').value
                point = parse_size(index.getElementsByTagName('Frame')[0].attributes.get('point').value)

                rect = QRect(*point, *size)
                image = atlas.copy(rect)

                indexes[index_name] = image

            groups[group_name] = indexes
        self.__resources[resource_name] = groups

        return groups


resource_loader = ResourceLoader()
