# Traceability: SubmissionController lifeline — the central orchestrator in the diagram

from baseline.services.validator import Validator
from baseline.services.database import Database
from baseline.services.reviewer_manager import ReviewerManager
from baseline.services.evaluation_manager import EvaluationManager
from baseline.services.notification_service import NotificationService
from datetime import datetime
import random

def ts():
    return datetime.now().strftime("%H:%M:%S")

class SubmissionController:
    """
    SMELL: God controller — orchestrates most interactions, knows about
    all services, and contains all flow logic. Violates SRP.
    """
    def __init__(self):
        self.validator = Validator()
        self.database = Database()
        self.reviewer_manager = ReviewerManager(self.database)
        self.notification_service = NotificationService()
        self.evaluation_manager = EvaluationManager(self.notification_service)

    def submit(self, data: dict) -> dict:
        """
        Diagram: UI → SubmissionController: submit(data)
        Orchestrates the full sequence from validation to notification.
        """
        researcher_id = data.get("author_id", "unknown")
        print(f"[{ts()}] [SubmissionController] Processing submission...")

        # --- Validator: validateFormat(data) ---
        is_valid = self.validator.validate_format(data)

        # --- alt [invalid] ---
        if not is_valid:
            print(f"[{ts()}] [SubmissionController] Submission rejected at validation.")
            return {"status": "error", "message": "Invalid submission format"}

        # --- alt [valid] ---
        # Database: saveSubmission(data) → confirmation
        submission_id = self.database.save_submission(data)

        # --- getAvailableReviewers() ---
        reviewer_list = self.reviewer_manager.get_available_reviewers()

        # --- ReviewerManager → Reviewer: filterConflicts, checkWorkload ---
        filtered = self.reviewer_manager.filter_conflicts(reviewer_list, researcher_id)
        filtered = self.reviewer_manager.check_workload(filtered)

        # --- loop [assign reviewers] ---
        # loop [assign reviewers]: SubmissionController -> ReviewerManager
        assigned_reviewers = filtered[:3]  # assign up to 3
        ids = ", ".join(r.reviewer_id for r in assigned_reviewers)
        print(f"  ├── [ReviewerManager] assign_review() -> {ids}")
        for reviewer in assigned_reviewers:
            self.reviewer_manager.assign_review(reviewer, submission_id)

        # --- startEvaluation() ---
        print(f"  └── [EvaluationManager] startEvaluation()...")

        # --- loop [each reviewer] → submitScore → saveScore ---
     
        
        for i, reviewer in enumerate(assigned_reviewers):
            # Simulated score generation
            score = round(random.uniform(3.0, 10.0), 1)
            is_last_reviewer = (i == len(assigned_reviewers) - 1)
            branch = "└──" if is_last_reviewer else "├──"
            print(f"      ├── [Reviewer {reviewer.reviewer_id}] submitScore({score})")
            print(f"      │   {branch} [Database] save_score() -> Score {score} saved for {reviewer.reviewer_id}")

            #Relay interaction: Manager receives score and forwards to Database
            self.reviewer_manager.save_score(submission_id, reviewer.reviewer_id, score)

        # --- EvaluationManager self-calls ---
        scores = self.database.get_scores(submission_id)
        
        
        decision = self.evaluation_manager.evaluate_and_notify(researcher_id, submission_id, scores)

        # Update DB
        self.database.update_submission_status(submission_id, decision)
        return {
            "status": decision, # Baseline often uses the decision as the status
            "submission_id": submission_id
        }

