from dataclasses import dataclass
from typing import Optional


@dataclass
class Email:
    id: Optional[int]
    sender: str
    subject: str
    received_date: str
    message: str
    labels: str
    is_read: bool
