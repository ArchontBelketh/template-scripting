NODE_METADATA = {
    "start": {
        "title": "Start",
        "category": "Flow",
        "color": "#ffffff",
        "inputs": [],
        "outputs": [
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "print": {
        "title": "Print",
        "category": "Statement",
        "color": "#5eead4",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "value",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "literal": {
        "title": "Literal",
        "category": "Expression",
        "color": "#c084fc",
        "inputs": [],
        "outputs": [
            {
                "name": "value",
                "type": "any",
            },
        ],
    },

    "variable": {
        "title": "Variable",
        "category": "Expression",
        "color": "#4ade80",
        "inputs": [],
        "outputs": [
            {
                "name": "value",
                "type": "any",
            },
        ],
    },

    "add": {
        "title": "Add",
        "category": "Math",
        "color": "#00d0ff",
        "inputs": [
            {
                "name": "left",
                "type": "any",
            },
            {
                "name": "right",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "result",
                "type": "any",
            },
        ],
    },

    "subtract": {
        "title": "Subtract",
        "category": "Math",
        "color": "#00d0ff",
        "inputs": [
            {
                "name": "left",
                "type": "any",
            },
            {
                "name": "right",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "result",
                "type": "any",
            },
        ],
    },

    "greater": {
        "title": "Greater",
        "category": "Logic",
        "color": "#ffcc00",
        "inputs": [
            {
                "name": "left",
                "type": "any",
            },
            {
                "name": "right",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "result",
                "type": "bool",
            },
        ],
    },

    "branch": {
        "title": "Branch",
        "category": "Flow",
        "color": "#ffffff",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "condition",
                "type": "bool",
            },
        ],
        "outputs": [
            {
                "name": "true",
                "type": "execution",
            },
            {
                "name": "false",
                "type": "execution",
            },
        ],
    },

    "while": {
        "title": "While",
        "category": "Flow",
        "color": "#ffffff",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "condition",
                "type": "bool",
            },
        ],
        "outputs": [
            {
                "name": "loop",
                "type": "execution",
            },
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "assign": {
        "title": "Assign",
        "category": "Statement",
        "color": "#4ade80",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "value",
                "type": "any",
            },
        ],
        "outputs": [
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },

    "return": {
        "title": "Return",
        "category": "Statement",
        "color": "#ffcc00",
        "inputs": [
            {
                "name": "exec",
                "type": "execution",
            },
            {
                "name": "value",
                "type": "any",
            },
        ],
        "outputs": [],
    },
}