from django.db import models

# Create your models here.
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timezone
import uuid

class BaseEntity(ABC):
    
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }

class Validate_enum:
    def validate_enum(self, value, enum_class, field_name):
        try:
            enum_class(value)
        except ValueError:
            valid = [e.value for e in enum_class]
            raise ValueError(
                f"Invalid {field_name} '{value}'. "
                f"Must be one of {valid}"
            )

class Reporter(BaseEntity, Validate_enum): 

    class Team(Enum):
        BACKEND = "backend"
        FRONTEND = "frontend"
        DEVOPS = "devops"

    
    def __init__(self, name, email, team):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.team = team
        
    def _validate_required_fields(self):

        errors = {}

        if not self.name:
            errors["name"] = "This field is required."

        if not self.email:
            errors["email"] = "This field is required."
        elif '@' not in self.email:
            errors["email"] = "Invalid email"
        
        if not self.team:
            errors["team"] = "This field is required"

        if errors:
            raise ValueError(errors)

    def validate(self):
        self._validate_required_fields()
        super().validate_enum(self.team, self.Team, "team")


class Issue(BaseEntity, Validate_enum):
    class Status(Enum):
        OPEN = "open"
        IN_PROGRESS = "in_progress"
        RESOLVED = "resolved"
        CLOSED = "closed"

    class Priority(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

    def __init__(self, title, description, status, priority, reporter_id):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = datetime.now(timezone.utc)


    def _validate_required_fields(self):

        errors = {}

        if not self.title:
            errors["title"] = "This field is required."

        if not self.description:
            errors["description"] = "This field is required."

        if not self.priority:
            errors["priority"] = "This field is required."

        if not self.status:
            errors["status"] = "This field is required."

        if not self.reporter_id:
            errors["reporter_id"] = "This field is required."

        if errors:
            raise ValueError(errors)

    
    def validate(self):
        self._validate_required_fields()
        super().validate_enum(self.status, self.Status, "status")
        super().validate_enum(self.priority, self.Priority, "priority")
    
    def describe(self):
        return f"{self.title} [{self.priority}]"

class CriticalIssue(Issue):
    def describe(self):
        return f"[URJENT] {self.title} - needs immediate attention"
    
class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} - low priority, handle when free"