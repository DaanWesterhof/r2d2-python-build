#!python

"""enums"""

import abc

class Enum(abc.ABC):
    """Base Enum class"""
    def __init__(self, name: str, items: dict):
        self.name = name
        self.items = dict(items)

    @classmethod
    def from_enum(cls, base):
        """returns a copy of an enum"""
        return cls(base.name, base.items)

    @abc.abstractmethod
    def __str__(self) -> str:
        """readable representation in the implemented language"""

class CxxEnum(Enum):
    """Class that defines an Enumeration in C++"""

    def __init__(self, name: str, inner_type: str, items: dict):
        """Initializes the enum class"""
        super().__init__(name, items)
        self.inner_type: str = inner_type

    def __len__(self) -> int:
        """Gives the number of items inside the enum"""
        return len(self.items)

    def __str__(self):
        return NotImplemented

    def __repr__(self) -> str:
        """Gives a representation in a string inside"""
        return f"{self.name} : {self.inner_type} {self.items.__repr__()}"

    def __iter__(self) -> str:
        """Iterates over all the items inside the enum"""
        for item in self.items:
            yield item

class PythonEnum(Enum):
    """python representation of an enum"""

    def __str__(self):
        return (
            """\nclass {self.name}(enum.Enum):\n{items}\n"""
            .format(
                self=self,
                items="\n".join([
                    "    {} = {}".format(
                        key, value if value is not None else "enum.auto()")
                    for key, value in self.items.items()])
            )
        )
