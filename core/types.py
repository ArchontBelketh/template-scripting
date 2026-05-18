from enum import Enum


class DataType(Enum):
    ANY = "any"

    EXECUTION = "execution"

    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"

    LIST = "list"
    DICT = "dict"
    TUPLE = "tuple"
    SET = "set"

    OBJECT = "object"

    FUNCTION = "function"
    CLASS = "class"


TYPE_COMPATIBILITY = {
    DataType.ANY: [
        item for item in DataType
    ],

    DataType.EXECUTION: [
        DataType.EXECUTION,
    ],

    DataType.INT: [
        DataType.INT,
    ],

    DataType.FLOAT: [
        DataType.FLOAT,
        DataType.INT,
    ],

    DataType.STRING: [
        DataType.STRING,
    ],

    DataType.BOOL: [
        DataType.BOOL,
    ],

    DataType.LIST: [
        DataType.LIST,
    ],

    DataType.DICT: [
        DataType.DICT,
    ],

    DataType.OBJECT: [
        DataType.OBJECT,
        DataType.CLASS,
    ],
}


def normalize_type(value):
    if isinstance(value, DataType):
        return value

    if isinstance(value, str):
        for item in DataType:
            if item.value == value:
                return item

    return DataType.ANY


def is_type_compatible(
    output_type,
    input_type,
):
    output_type = normalize_type(output_type)
    input_type = normalize_type(input_type)

    if input_type == DataType.ANY:
        return True

    compatible = TYPE_COMPATIBILITY.get(
        input_type,
        [],
    )

    return output_type in compatible