from enum import Enum, unique


class StringEnum(str, Enum):
    """
    ``This class is the base string enumerate.``
    """

    def __str__(self):
        return self.value


@unique
class ColName(StringEnum):
    """
    Constant values for name conventions

    """

    # TODO
