from enum import Enum


class DataType(Enum):
    ANY = "any"

    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"

    LIST = "list"
    DICT = "dict"
    TUPLE = "tuple"
    SET = "set"

    OBJECT = "object"