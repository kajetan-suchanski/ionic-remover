from enum import Enum


class NamingConvention(Enum):
    KEBAB_CASE = 0
    CAMEL_CASE = 1


NAMING_CONVENTION_NAMES = [e.name for e in NamingConvention]
