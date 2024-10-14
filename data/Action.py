from dataclasses import dataclass
from typing import Optional

from enums.ActionType import ActionType


@dataclass
class Action:
    action_type: ActionType
    folder_name: Optional[str] = None
