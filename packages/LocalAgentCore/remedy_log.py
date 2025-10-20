
import datetime
import uuid
from typing import Optional, Dict, Any

class RemedyLog:
    def __init__(
        self,
        timestamp: datetime.datetime,
        user_id: Optional[str] = None,
        module: Optional[str] = None,
        instrument_ids: Optional[list[str]] = None,
        workflow_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        log_level: str = "INFO", # e.g. INFO, WARNING, ERROR
        message: Optional[str] = None
    ):
        self.timestamp = timestamp
        self.user_id = user_id
        self.module = module
        self.instrument_ids = instrument_ids
        self.workflow_id = workflow_id or str(uuid.uuid4())  # Generate a unique workflow ID if not provided
        self.data = data or {}
        self.log_level = log_level
        self.message = message

    def __repr__(self):
        return f"RemedyLog(timestamp={self.timestamp}, user_id={self.user_id}, module={self.module}, workflow_id={self.workflow_id}, log_level={self.log_level}, message={self.message})"

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "module": self.module,
            "instrument_ids": self.instrument_ids,
            "workflow_id": self.workflow_id,
            "data": self.data,
            "log_level": self.log_level,
            "message": self.message,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            user_id=data.get("user_id"),
            module=data.get("module"),
            instrument_ids=data.get("instrument_ids"),
            workflow_id=data.get("workflow_id"),
            data=data.get("data"),
            log_level=data.get("log_level"),
            message=data.get("message"),
        )
