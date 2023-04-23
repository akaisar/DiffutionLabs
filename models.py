from typing import List, Any
from dataclasses import dataclass


@dataclass
class Event:
    event: Any

@dataclass
class Log:
    events: List[Event]

@dataclass
class Transaction:
    logs: List[Log]

@dataclass
class Block:
    transactions: List[Transaction]
