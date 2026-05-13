# Traceability: Data models for Researcher, Submission, Reviewer entities in diagram

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Submission:
    submission_id: str
    researcher_id: str
    data: dict
    status: str = "pending"     # pending | accepted | rejected | revision

@dataclass
class Reviewer:
    reviewer_id: str
    name: str
    domain: str
    workload: int = 0   # number of active reviews
    conflicts: List[str] = field(default_factory=list) # researcher IDs with conflict