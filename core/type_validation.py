from core.type_system import ANY_TYPE


class TypeValidationEngine:
    def validate(
        self,
        output_type,
        input_type,
    ):
        if input_type.name == "any":
            return True

        if output_type.name == "any":
            return True

        return output_type.matches(
            input_type
        )

    def can_auto_cast(
        self,
        output_type,
        input_type,
    ):
        allowed = {
            ("int", "float"),
            ("int", "str"),
            ("float", "str"),
            ("bool", "str"),
        }

        return (
            output_type.name,
            input_type.name,
        ) in allowed