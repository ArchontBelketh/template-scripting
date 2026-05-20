from core.type_system import TypeInfo


class TypeValidationEngine:
    @staticmethod
    def validate_connection(source_type: TypeInfo, target_type: TypeInfo) -> bool:
        """Проверяет допустимость связи между выходным и входным пинами."""
        if source_type.name == "exec" or target_type.name == "exec":
            return source_type.name == target_type.name
        return source_type.matches(target_type)