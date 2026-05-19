from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TypeInfo:
    name: str

    generic_args: list["TypeInfo"] | None = None

    nullable: bool = False

    inferred: bool = False

    def __str__(self):
        base = self.name

        if self.generic_args:
            generics = ", ".join(
                str(arg)
                for arg in self.generic_args
            )

            base += f"[{generics}]"

        if self.nullable:
            base += "?"

        return base

    @property
    def display_name(self):
        return str(self)

    def matches(self, other: "TypeInfo"):
        if self.name == "any":
            return True

        if other.name == "any":
            return True

        if self.name != other.name:
            return False

        if not self.generic_args:
            return True

        if not other.generic_args:
            return False

        if (
            len(self.generic_args)
            != len(other.generic_args)
        ):
            return False

        for left, right in zip(
            self.generic_args,
            other.generic_args,
        ):
            if not left.matches(right):
                return False

        return True


ANY_TYPE = TypeInfo("any")

INT_TYPE = TypeInfo("int")
FLOAT_TYPE = TypeInfo("float")
STRING_TYPE = TypeInfo("str")
BOOL_TYPE = TypeInfo("bool")

EXEC_TYPE = TypeInfo("execution")


def LIST_TYPE(item):
    return TypeInfo(
        "list",
        generic_args=[item],
    )


def DICT_TYPE(key, value):
    return TypeInfo(
        "dict",
        generic_args=[key, value],
    )


def OPTIONAL_TYPE(inner):
    return TypeInfo(
        inner.name,
        generic_args=inner.generic_args,
        nullable=True,
    )