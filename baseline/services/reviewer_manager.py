# Traceability: ReviewerManager lifeline — getAvailableReviewers(), filterConflicts(),
#               checkWorkload(), assignReview(), saveScore()

from baseline.models.submission import Reviewer
from baseline.services.database import Database
from typing import List

class ReviewerManager:
    def __init__(self, database: Database):
        self.database = database

    def get_available_reviewers(self) -> List[Reviewer]:
        """
        Diagram: SubmissionController → ReviewerManager: getAvailableReviewers()
        ReviewerManager then calls Database: fetchReviewers()
        SMELL: ReviewerManager is a pass-through — fetches then immediately filters
        """
        print("  ├── [ReviewerManager] Filtering available reviewers...")
        return self.database.fetch_reviewers()

    def filter_conflicts(self, reviewer_list: List[Reviewer], researcher_id: str) -> List[Reviewer]:
        """
        Diagram: ReviewerManager → Reviewer: filterConflicts(reviewerList)
        SMELL: Reviewer entity doing filtering that belongs in ReviewerManager
        """
        # Simulating delegating to each Reviewer object (as per diagram)
        filtered = [r for r in reviewer_list if researcher_id not in r.conflicts]
        print(f"  │   ├── Conflict Filter: PASS")
        return filtered

    def check_workload(self, reviewer_list: List[Reviewer]) -> List[Reviewer]:
        """
        Diagram: ReviewerManager → Reviewer: checkWorkload(reviewerList)
        SMELL: Again delegated to Reviewer, high coupling
        """
        available = [r for r in reviewer_list if r.workload < 3]
        ids = ", ".join(r.reviewer_id for r in available)
        print(f"  │   └── Workload Check:  PASS (Reviewers: {ids})")
        return available

    def assign_review(self, reviewer: Reviewer, submission_id: str):
        """
        Diagram: loop [assign reviewers] — SubmissionController → ReviewerManager: assignReview()
        Then ReviewerManager → Reviewer: assignReview()
        SMELL: Two hops to assign (controller → manager → reviewer object)
        """
        reviewer.workload += 1
        #print(f"  [ReviewerManager] Assigned reviewer {reviewer.reviewer_id} to {submission_id}")

    def save_score(self, submission_id: str, reviewer_id: str, score: float):
        """
        Diagram: loop [each reviewer] — Reviewer → ReviewerManager: saveScore(score)
        Then ReviewerManager → Database: saveScore(score)
        SMELL: Unnecessary relay through ReviewerManager just to reach Database
        """
        self.database.save_score(submission_id, reviewer_id, score)