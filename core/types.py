from core.type_system import TypeInfo, ANY_TYPE


def normalize_type(type_obj: TypeInfo) -> TypeInfo:
    """Приводит тип к каноничному виду."""
    if not isinstance(type_obj, TypeInfo):
        return ANY_TYPE
    return type_obj


def is_type_compatible(source: TypeInfo, target: TypeInfo) -> bool:
    """Проверяет, можно ли передать данные из source в target."""
    if source is None or target is None:
        return False
    return source.matches(target)


def auto_cast_expression(source_expr: str, source_type: TypeInfo, target_type: TypeInfo) -> str:
    """Генерирует код явного приведения типов, если это необходимо."""
    if source_type.name == "int" and target_type.name == "float":
        return source_expr  # Неявное аппроксимирование в Python разрешено
    if source_type.name != target_type.name:
        if target_type.name == "str":
            return f"str({source_expr})"
        if target_type.name == "int" and source_type.name == "float":
            return f"int({source_expr})"
        if target_type.name == "float" and source_type.name == "str":
            return f"float({source_expr})"
    return source_expr