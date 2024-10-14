from dataclasses import dataclass
from datetime import datetime
from typing import Union

from enums.DatePredicate import DatePredicate
from enums.FieldType import FieldType
from enums.StringPredicate import StringPredicate


@dataclass
class Rule:
    field: FieldType
    predicate: Union[StringPredicate, DatePredicate]
    value: Union[str, int]
