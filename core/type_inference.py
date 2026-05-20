import ast
from core.type_system import (
    TypeInfo,
    INT_TYPE,
    FLOAT_TYPE,
    STRING_TYPE,
    BOOL_TYPE,
    ANY_TYPE,
    LIST_TYPE,
    DICT_TYPE,
    UNION_TYPE,
)


class TypeInferenceEngine:
    @staticmethod
    def infer_from_value(value: str) -> TypeInfo:
        """Определяет TypeInfo на основе строкового представления значения литерала."""
        if not value or value.strip() == "":
            return ANY_TYPE

        try:
            parsed = ast.parse(value, mode="eval")
            return TypeInferenceEngine.infer_from_ast_node(parsed.body)
        except Exception:
            # Если это не валидный литерал Python, считаем это строкой или произвольным кодом
            return STRING_TYPE

    @staticmethod
    def infer_from_ast_node(node: ast.AST) -> TypeInfo:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                return BOOL_TYPE
            if isinstance(node.value, int):
                return INT_TYPE
            if isinstance(node.value, float):
                return FLOAT_TYPE
            if isinstance(node.value, str):
                return STRING_TYPE
            if node.value is None:
                return ANY_TYPE

        elif isinstance(node, ast.List):
            if not node.elts:
                return LIST_TYPE(ANY_TYPE)
            element_types = [TypeInferenceEngine.infer_from_ast_node(el) for el in node.elts]
            return LIST_TYPE(UNION_TYPE(element_types))

        elif isinstance(node, ast.Dict):
            if not node.keys:
                return DICT_TYPE(ANY_TYPE, ANY_TYPE)
            key_types = [TypeInferenceEngine.infer_from_ast_node(k) for k in node.keys if k is not None]
            val_types = [TypeInferenceEngine.infer_from_ast_node(v) for v in node.values]
            return DICT_TYPE(UNION_TYPE(key_types), UNION_TYPE(val_types))

        return ANY_TYPE