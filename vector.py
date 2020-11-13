import functools
import math
import numbers
import operator
import reprlib
from array import array


class Vector:
    __slots__ = "_components"
    type_code = "d"
    shortcut_names = "xyzt"

    def __init__(self, components: iter):
        self._components = array(self.type_code, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find("["): -1]

        return f"Vector({components!r})"

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.type_code)]) + bytes(self._components)

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __len__(self):
        return len(self._components)

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x ** 2 for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __getitem__(self, item):
        cls = type(self)
        if isinstance(item, slice):
            return cls(self._components[item])

        elif isinstance(item, numbers.Integral):
            return self._components[item]

        else:
            raise TypeError(f"{cls.__name__!r} indices must be integers")

    def __getattr__(self, item):
        cls = type(self)
        if len(item) == 1:
            position = cls.shortcut_names.find(item)

            if 0 <= position <= len(cls.shortcut_names):
                return self._components[position]

        raise AttributeError(f"{cls.__name__!r} object has no attribute {item!r}")

    def __setattr__(self, key, value):
        cls = type(self)
        if len(key) == 1:
            if key in cls.shortcut_names:
                error = f"readonly attribute {key!r}"
            elif key.islower():
                error = f"a-z is protected namespace for {cls.__name__!r}"
            else:
                error = ""

            if error:
                raise AttributeError(error)

        super().__setattr__(key, value)

    @classmethod
    def from_bytes(cls, octets):
        type_code = chr(octets[0])
        memv = memoryview(octets[1:]).cast(type_code)
        return cls(memv)
