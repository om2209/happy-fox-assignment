from dataclasses import dataclass
from typing import List

from data.Action import Action
from data.Rule import Rule
from enums.RuleSetPredicate import RuleSetPredicate


@dataclass
class RuleSet:
    predicate: RuleSetPredicate
    rules: List[Rule]
    actions: List[Action]
