from enum import Enum


class ResultElement(Enum):
    DIV = 0
    REACT_COMPONENT = 1


RESULT_ELEMENT_NAMES = [e.name for e in ResultElement]
