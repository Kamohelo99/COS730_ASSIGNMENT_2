import uuid
from optimised.models.submission import Submission, Reviewer

class SubmissionRepository:
    def __init__(self):
        self._submissions = {}

    def save_submission(self, data: dict) -> str:
        # Traceability: [SubmissionRepository] saveSubmission(data)
        submission_id = str(uuid.uuid4())[:8]
        self._submissions[submission_id] = Submission(
            submission_id=submission_id,
            researcher_id=data["author_id"],
            data=data
        )
        print(f"  ├── [SubmissionRepository] save_submission() -> ID: {submission_id}")
        return submission_id

    def update_status(self, submission_id: str, status: str):
        if submission_id in self._submissions:
            self._submissions[submission_id].status = status

class ReviewerRepository:
    def __init__(self):
        
        self._reviewers = {
            "r1": Reviewer("r1", "Alice", "ML", workload=1, conflicts=["researcher_99"]),
            "r2": Reviewer("r2", "Bob",   "CV", workload=3, conflicts=[]),
            "r3": Reviewer("r3", "Carol", "NLP", workload=0, conflicts=[]),
            "r4": Reviewer("r4", "Dave",  "ML", workload=2, conflicts=["researcher_42"]),
        }

    def fetch_reviewers(self) -> list:
        # Traceability: [ReviewerRepository] fetchReviewers()
        print("  │   ├── [ReviewerRepository] fetchReviewers()")
        return list(self._reviewers.values())