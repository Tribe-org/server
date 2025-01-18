import re

from pydantic import ConfigDict


def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s


def snake2camel(snake: str, start_lower: bool = True) -> str:
    """
    Converts a snake_case string to camelCase.

    The `start_lower` argument determines whether the first letter in the generated camelcase should # noqa
    be lowercase (if `start_lower` is True), or capitalized (if `start_lower` is False). # noqa
    """

    # camelCase일 경우 그냥 바로 return 한다.
    if is_camel_case(s=snake):
        return snake

    # auth_name -> Auth_Name
    camel = snake.title()

    # Auth_Name -> AuthName
    camel = re.sub("([0-9A-Za-z])_(?=[0-9A-Z])", lambda m: m.group(1), camel)

    # AuthName -> authName
    if start_lower:
        camel = re.sub("(^_*[A-Z])", lambda m: m.group(1).lower(), camel)
    return camel


def camel2snake(camel: str) -> str:
    """
    Converts a camelCase string to snake_case.
    """
    snake = re.sub(
        r"([a-zA-Z])([0-9])", lambda m: f"{m.group(1)}_{m.group(2)}", camel
    )
    snake = re.sub(
        r"([a-z0-9])([A-Z])", lambda m: f"{m.group(1)}_{m.group(2)}", snake
    )
    return snake.lower()


def get_camel_model_config():
    return ConfigDict(alias_generator=snake2camel, populate_by_name=True)
