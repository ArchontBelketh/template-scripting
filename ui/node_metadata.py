NODE_METADATA = {
    "while": {
        "title": "While",
        "category": "Flow",
        "color": "#ffb347",
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
                "name": "completed",
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
                "type": "string",
            },
        ],
        "outputs": [
            {
                "name": "next",
                "type": "execution",
            },
        ],
    },
}