from core.type_system import (
    ANY_TYPE,
    INT_TYPE,
    FLOAT_TYPE,
    STRING_TYPE,
    BOOL_TYPE,
    LIST_TYPE,
)


class TypeInferenceEngine:
    def infer_literal(self, value):
        if isinstance(value, bool):
            return BOOL_TYPE

        if isinstance(value, int):
            return INT_TYPE

        if isinstance(value, float):
            return FLOAT_TYPE

        if isinstance(value, str):
            return STRING_TYPE

        if isinstance(value, list):
            if not value:
                return LIST_TYPE(ANY_TYPE)

            inner = self.infer_literal(
                value[0]
            )

            return LIST_TYPE(inner)

        return ANY_TYPE