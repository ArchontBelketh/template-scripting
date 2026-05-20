from core.type_system import (
    ANY_TYPE,
    EXEC_TYPE,
    FLOAT_TYPE,
    STRING_TYPE,
    BOOL_TYPE,
    LIST_TYPE,
    DICT_TYPE,
    OPTIONAL_TYPE,
)
from nodes.base.executable_node import ExecutableNode

NODE_METADATA = {
    "start": {
        "title": "Start",
        "class": ExecutableNode,
        "category": "Flow",
        "description": "Точка входа для выполнения визуального скрипта"
    },
    "entry": {
        "title": "Start",
        "inputs": [],
        "outputs": [("next", EXEC_TYPE)]
    },
    "print": {
        "title": "Print",
        "inputs": [("exec_in", EXEC_TYPE), ("value", ANY_TYPE)],
        "outputs": [("exec_out", EXEC_TYPE)]
    },
    "if": {
        "title": "If Branch",
        "inputs": [("exec_in", EXEC_TYPE), ("condition", BOOL_TYPE)],
        "outputs": [("true", EXEC_TYPE), ("false", EXEC_TYPE)]
    },
    "binary_op": {
        "title": "Binary Op",
        "inputs": [("a", FLOAT_TYPE), ("b", FLOAT_TYPE)],
        "outputs": [("output", FLOAT_TYPE)]
    },
    "string_concat": {
        "title": "Concat Strings",
        "inputs": [("a", STRING_TYPE), ("b", STRING_TYPE)],
        "outputs": [("output", STRING_TYPE)]
    },
    "while": {
        "title": "While Loop",
        "inputs": [("exec_in", EXEC_TYPE), ("condition", BOOL_TYPE)],
        "outputs": [("body", EXEC_TYPE), ("completed", EXEC_TYPE)]
    },
    "create_list": {
        "title": "Create List",
        "inputs": [("item0", ANY_TYPE), ("item1", ANY_TYPE)],
        "outputs": [("list", LIST_TYPE(ANY_TYPE))]
    },
    "create_dict": {
        "title": "Create Dict",
        "inputs": [("key", STRING_TYPE), ("value", ANY_TYPE)],
        "outputs": [("dict", DICT_TYPE(STRING_TYPE, ANY_TYPE))]
    },
    "optional_handler": {
        "title": "Optional Handler",
        "inputs": [("data", OPTIONAL_TYPE(STRING_TYPE))],
        "outputs": [("result", STRING_TYPE)]
    }
}