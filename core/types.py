from core.type_system import *

from core.type_validation import (
    TypeValidationEngine,
)

validator = TypeValidationEngine()


def normalize_type(value):
    if isinstance(value, TypeInfo):
        return value

    if isinstance(value, str):
        return TypeInfo(value)

    return ANY_TYPE


def is_type_compatible(
    output_type,
    input_type,
):
    output_type = normalize_type(
        output_type
    )

    input_type = normalize_type(
        input_type
    )

    return validator.validate(
        output_type,
        input_type,
    )