from enum import Enum, unique


class StringEnum(str, Enum):
    """
    ``This class is the base string enumerate.``
    """

    def __str__(self):
        return self.value

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


@unique
class ColName(StringEnum):
    """
    Constant values for name conventions

    """

    PASS = "Pass"
    USER = "User"
    DATA_BASE = "DataBase"
    SERVER = "Server"
    DRIVER = "Driver"
    SCHEMA = "Schema"
    PORT = "Port"
