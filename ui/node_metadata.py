from core.type_system import *

NODE_METADATA = {
    "start": {
        "title": "Start",

        "inputs": [],

        "outputs": [
            {
                "name": "exec",
                "type": EXEC_TYPE,
            },
        ],
    },
    "print": {
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

    "number": {
        "title": "Number",

        "inputs": [],

        "outputs": [
            {
                "name": "value",
                "type": FLOAT_TYPE,
            },
        ],
    },

    "string": {
        "title": "String",

        "inputs": [],

        "outputs": [
            {
                "name": "value",
                "type": STRING_TYPE,
            },
        ],
    },

    "bool": {
        "title": "Bool",

        "inputs": [],

        "outputs": [
            {
                "name": "value",
                "type": BOOL_TYPE,
            },
        ],
    },

    "add": {
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

    "branch": {
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

    "list": {
        "title": "List",

        "inputs": [],

        "outputs": [
            {
                "name": "items",
                "type": LIST_TYPE(ANY_TYPE),
            },
        ],
    },

    "dictionary": {
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

    "optional_string": {
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