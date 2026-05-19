from core.type_system import *

NODE_METADATA = {
    "PrintNode": {
        "title": "Print",

        "inputs": [
            {
                "name": "exec_in",
                "type": EXEC_TYPE,
            },
            {
                "name": "value",
                "type": ANY_TYPE,
            },
        ],

        "outputs": [
            {
                "name": "exec_out",
                "type": EXEC_TYPE,
            },
        ],
    },

    "NumberNode": {
        "title": "Number",

        "inputs": [],

        "outputs": [
            {
                "name": "value",
                "type": FLOAT_TYPE,
            },
        ],
    },

    "StringNode": {
        "title": "String",

        "inputs": [],

        "outputs": [
            {
                "name": "value",
                "type": STRING_TYPE,
            },
        ],
    },

    "BoolNode": {
        "title": "Bool",

        "inputs": [],

        "outputs": [
            {
                "name": "value",
                "type": BOOL_TYPE,
            },
        ],
    },

    "AddNode": {
        "title": "Add",

        "inputs": [
            {
                "name": "A",
                "type": FLOAT_TYPE,
            },
            {
                "name": "B",
                "type": FLOAT_TYPE,
            },
        ],

        "outputs": [
            {
                "name": "Result",
                "type": FLOAT_TYPE,
            },
        ],
    },

    "BranchNode": {
        "title": "Branch",

        "inputs": [
            {
                "name": "exec_in",
                "type": EXEC_TYPE,
            },
            {
                "name": "condition",
                "type": BOOL_TYPE,
            },
        ],

        "outputs": [
            {
                "name": "true",
                "type": EXEC_TYPE,
            },
            {
                "name": "false",
                "type": EXEC_TYPE,
            },
        ],
    },

    "ListNode": {
        "title": "List",

        "inputs": [],

        "outputs": [
            {
                "name": "items",
                "type": LIST_TYPE(ANY_TYPE),
            },
        ],
    },

    "DictionaryNode": {
        "title": "Dictionary",

        "inputs": [],

        "outputs": [
            {
                "name": "dict",
                "type": DICT_TYPE(
                    STRING_TYPE,
                    ANY_TYPE,
                ),
            },
        ],
    },

    "OptionalStringNode": {
        "title": "Optional String",

        "inputs": [],

        "outputs": [
            {
                "name": "value",
                "type": OPTIONAL_TYPE(
                    STRING_TYPE
                ),
            },
        ],
    },
}