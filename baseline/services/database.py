# Traceability: Database lifeline — saveSubmission(data), fetchReviewers()

from baseline.models.submission import Submission, Reviewer
from typing import List
import uuid

class Database:
    def __init__(self):
        self._submissions = {}
        self._reviewers = {
            "r1": Reviewer("r1", "Alice", "ML", workload=1, conflicts=["researcher_99"]),
            "r2": Reviewer("r2", "Bob",   "CV", workload=3, conflicts=[]),
            "r3": Reviewer("r3", "Carol", "NLP", workload=0, conflicts=[]),
            "r4": Reviewer("r4", "Dave",  "ML", workload=2, conflicts=["researcher_42"]),
        }
        self._scores = {}

    def save_submission(self, data: dict) -> str:
            """
            Diagram: SubmissionController → Database: saveSubmission(data)
            Returns confirmation (submission_id).
            """
            submission_id = str(uuid.uuid4())[:8]
            self._submissions[submission_id] = Submission(
                submission_id=submission_id,
                researcher_id=data["author_id"],
                data=data
            )
            print(f"  ├── [Database] save_submission() -> ID: {submission_id}")
            return submission_id

    def fetch_reviewers(self) -> List[Reviewer]:
        """
        Diagram: ReviewerManager → Database: fetchReviewers()
        Returns full reviewer list.
        """
        return list(self._reviewers.values())

    def save_score(self, submission_id: str, reviewer_id: str, score: float):
        """
        Diagram: Database ← saveScore(score) from ReviewerManager loop
        """
        if submission_id not in self._scores:
            self._scores[submission_id] = {}
        self._scores[submission_id][reviewer_id] = score
        #print(f"  [Database] Saved score {score} from reviewer {reviewer_id}")

    def get_scores(self, submission_id: str) -> dict:
        return self._scores.get(submission_id, {})

    def update_submission_status(self, submission_id: str, status: str):
        if submission_id in self._submissions:
            self._submissions[submission_id].status = status