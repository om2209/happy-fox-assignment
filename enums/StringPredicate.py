from enum import Enum


class StringPredicate(Enum):
    EQUALS = "equals"
    DOES_NOT_EQUAL = "does_not_equal"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "does_not_contain"
