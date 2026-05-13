import random
from datetime import datetime
from optimised.services.validator import Validator
from optimised.services.repositories import SubmissionRepository, ReviewerRepository
from optimised.services.reviewer_manager import ReviewerManager
from optimised.services.evaluation_manager import EvaluationManager
from optimised.services.notification_service import NotificationService

def ts():
    return datetime.now().strftime("%H:%M:%S")

class SubmissionController:
    def __init__(self):
        self.validator = Validator()
        self.sub_repo = SubmissionRepository()
        self.rev_repo = ReviewerRepository()
        self.rev_mgr = ReviewerManager()
        self.notifier = NotificationService()
        self.eval_mgr = EvaluationManager(self.notifier)

    def submit(self, data: dict):
        # Traceability: Researcher Actor initiates (Diagram Interaction 4)
        print(f"[{ts()}] [SubmissionController] Processing submission...")
        
        # 1. Validator: validateFormat(data) (Diagram Interaction 5)
        if not self.validator.validate_format(data):
            # Traceability: alt [invalid] branch (Diagram Interaction 6 & 7)
            print(f"[{ts()}] [SubmissionController] Submission rejected at validation.")
            return {"status": "error", "message": "Invalid submission format"}

        # 2. alt [valid]: saveSubmission(data) (Diagram Interaction 12)
        sub_id = self.sub_repo.save_submission(data)

        # 3. getAvailableReviewers() (Diagram Interaction 14)
        available = self.rev_mgr.get_available_reviewers(self.rev_repo, data["author_id"])
        assigned = available[:3]
        
        # 4. loop [assign reviewers] (Diagram Interaction 22)
        for r in assigned:
            self.rev_mgr.assign_review(r, sub_id)

        # 5. loop [each reviewer]: ACTOR interaction (Diagram Interaction 25)
        print(f"  ├── [Loop] [Actor: Reviewer] Submitting scores...")
        for r in assigned:
            simulated_score = round(random.uniform(5.0, 9.5), 1)
            print(f"      [Actor: Reviewer {r.reviewer_id}] submitScore({simulated_score})")
            self.eval_mgr.receive_score(sub_id, r.reviewer_id, simulated_score)

        # 6. startEvaluation() (Diagram Interaction 16)
        decision = self.eval_mgr.start_evaluation(data["author_id"], sub_id)
        
        # 7. Update repository status
        self.sub_repo.update_status(sub_id, decision)

        return {
            "status": "success",
            "submission_id": sub_id,
            "decision": decision
        }