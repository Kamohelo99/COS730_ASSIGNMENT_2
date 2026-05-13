from dataclasses import dataclass, field
from typing import List

@dataclass
class Submission:
    submission_id: str
    researcher_id: str
    data: dict
    status: str = "pending"

@dataclass
class Reviewer:
    reviewer_id: str
    name: str
    domain: str
    workload: int = 0
    conflicts: List[str] = field(default_factory=list)