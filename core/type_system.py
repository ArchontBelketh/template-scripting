from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class TypeInfo:
    name: str  # "int", "float", "str", "bool", "list", "dict", "union", "any", "exec"
    generic_args: List["TypeInfo"] = field(default_factory=list)
    is_optional: bool = False

    def matches(self, other: "TypeInfo") -> bool:
        # 'any' совпадает с абсолютно любым типом
        if self.name == "any" or other.name == "any":
            return True

        # Если один из типов Union, проверяем вхождение
        if self.name == "union":
            return any(arg.matches(other) for arg in self.generic_args)
        if other.name == "union":
            return any(self.matches(arg) for arg in other.generic_args)

        # Проверка опциональности (nullable)
        if self.is_optional != other.is_optional and not (self.is_optional or other.is_optional):
            return False

        # Базовая проверка имени типа
        if self.name != other.name:
            # Поддержка безопасного неявного приведения (Type Casting): int -> float
            if self.name == "int" and other.name == "float":
                return True
            return False

        # Рекурсивная проверка Generics (например, list[int] vs list[str])
        if self.generic_args and other.generic_args:
            if len(self.generic_args) != len(other.generic_args):
                return False
            return all(g1.matches(g2) for g1, g2 in zip(self.generic_args, other.generic_args))

        return True

    def __str__(self) -> str:
        opt_str = "?" if self.is_optional else ""
        if self.name == "union":
            return f"({' | '.join(str(arg) for arg in self.generic_args)}){opt_str}"
        if self.generic_args:
            args_str = ", ".join(str(arg) for arg in self.generic_args)
            return f"{self.name}[{args_str}]{opt_str}"
        return f"{self.name}{opt_str}"


# Предопределенные константы базовых типов данных
ANY_TYPE = TypeInfo(name="any")
EXEC_TYPE = TypeInfo(name="exec")
INT_TYPE = TypeInfo(name="int")
FLOAT_TYPE = TypeInfo(name="float")
STRING_TYPE = TypeInfo(name="str")
BOOL_TYPE = TypeInfo(name="bool")


def LIST_TYPE(element_type: TypeInfo) -> TypeInfo:
    return TypeInfo(name="list", generic_args=[element_type])


def DICT_TYPE(key_type: TypeInfo, value_type: TypeInfo) -> TypeInfo:
    return TypeInfo(name="dict", generic_args=[key_type, value_type])


def UNION_TYPE(types: List[TypeInfo]) -> TypeInfo:
    # Плоское развертывание вложенных Union
    flat_types: Set[TypeInfo] = set()
    for t in types:
        if t.name == "union":
            flat_types.update(t.generic_args)
        else:
            flat_types.add(t)
    if len(flat_types) == 1:
        return list(flat_types)[0]
    return TypeInfo(name="union", generic_args=sorted(list(flat_types), key=lambda x: x.name))


def OPTIONAL_TYPE(base_type: TypeInfo) -> TypeInfo:
    return TypeInfo(name=base_type.name, generic_args=base_type.generic_args, is_optional=True)