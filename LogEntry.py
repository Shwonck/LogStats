from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    ip: str
    timestamp: datetime
    method: str
    endpoint: str
    protocol: str
    status: int
    bytes: int
    response_time: float