"""
Модуль, содержащий полезные функции и классы для динамической проверки типа.

Поддерживает такие расширения модуля typing как: Any, Union[X, Y], Optional[X], Literal[x, y], Sequence[X],
tuple[()], tuple[X, ...], tuple[X, Y], list[X], dict[X, Y]

Также поддерживает вложенные типы, например: Optional[tuple[int, str]], dict[str, tuple[Optional[int], ...]]
"""
import typing as t
from typing import Union, Literal
from collections.abc import Sequence


def each_item_matches(seq: t.Iterable[t.Any], type_: t.Any):
    """Каждый элемент последовательности соответствует указанному типу"""
    return all(map(lambda x: matches_type(x, type_), seq))


def matches_type(value: t.Any, type_: t.Any):
    """
    Возвращает True если тип value совпадает с type_, иначе False.
    :param value: Значение тип которого нужно проверить
    :param type_: Тип с которым необходимо соотнести значение
    :return: Соответствует ли value переданному типу
    """
    if type_ is t.Any:
        return True

    if hasattr(type_, '__args__') and hasattr(type_, '__origin__'):

        if type_.__origin__ is Union:  # Union[X, Y]
            return any(map(lambda x: matches_type(value, x), type_.__args__))

        if type_.__origin__ is Literal:  # Literal[x, y]
            return any(map(lambda x: value == x, type_.__args__))

        if type_.__origin__ is Sequence and len(type_.__args__) == 1:  # Sequence[X]
            return hasattr(value, '__len__') and hasattr(value, '__getitem__') and each_item_matches(value, type_.__args__[0])

        if type_.__origin__ is tuple and len(type_.__args__) == 1 and type_.__args__[0] == tuple:  # tuple[()]
            return isinstance(value, tuple) and len(value) == 0

        if type_.__origin__ is tuple and len(type_.__args__) == 2 and type_.__args__[1] == Ellipsis:  # tuple[X, ...]
            return isinstance(value, tuple) and each_item_matches(value, type_.__args__[0])

        if type_.__origin__ is tuple and len(type_.__args__) > 0:  # tuple[X, Y]
            if not isinstance(value, tuple) or len(value) != len(type_.__args__):
                return False
            return all(map(lambda v, tp: matches_type(v, tp), value, type_.__args__))

        if type_.__origin__ is list and len(type_.__args__) == 1:  # list[X]
            return isinstance(value, list) and each_item_matches(value, type_.__args__[0])

        if type_.__origin__ is dict and len(type_.__args__) == 2:  # dict[X, Y]
            return all((
                isinstance(value, dict),
                each_item_matches(value.keys(), type_.__args__[0]),
                each_item_matches(value.values(), type_.__args__[1])
            ))

        raise NotImplementedError('Can not dynamically check given type yet')

    return isinstance(value, type_)


def check_type(value: t.Any, type_: t.Any):
    """
    Возвращает значение value если его тип совпадает с type_, иначе генерируется исключение TypeError.
    :param value: Значение тип которого нужно проверить
    :param type_: Тип с которым необходимо соотнести значение
    :return: value или TypeError в зависимости от результата работы
    """
    if matches_type(value, type_):
        return value
    raise TypeError('The value does not match the required type')


def check_type_default(value: t.Any, type_: t.Any, default: t.Any):
    """
    Возвращает значение value если его тип совпадает с type_, иначе - default.
    При этом проверка типа для default не осуществляется.
    :param value: Значение тип которого нужно проверить
    :param type_: Тип с которым необходимо соотнести значение
    :param default: Значение, которое будет возвращено в случае несовпадения типов (по умалчание: None)
    :return: value или default в зависимости от результата работы
    """
    if matches_type(value, type_):
        return value
    return default
