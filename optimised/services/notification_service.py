from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

class NotificationService:
    def notify_acceptance(self, researcher_id: str, submission_id: str):
        # Traceability: alt [accepted] -> NotificationService: notifyAcceptance()
        print(f"  [NotificationService] ACCEPTED: Notified {researcher_id} for {submission_id}")

    def notify_rejection(self, researcher_id: str, submission_id: str):
        # Traceability: alt [rejected] -> NotificationService: notifyRejection()
        print(f"[{ts()}] [NotificationService] Sending REJECTION to {researcher_id}.")

    def notify_revision(self, researcher_id: str, submission_id: str):
        # Traceability: alt [revision] -> NotificationService: notifyRevision()
        print(f"[{ts()}] [NotificationService] Sending REVISION REQUEST to {researcher_id}.")

    def send_notification(self, researcher_id: str, submission_id: str, decision: str):
        """
        Fixed signature: Accepts 3 arguments (+ self = 4 total)
        Routes to the correct notify method based on the decision.
        """
        if decision == "accepted":
            self.notify_acceptance(researcher_id, submission_id)
        elif decision == "rejected":
            self.notify_rejection(researcher_id, submission_id)
        else:
            self.notify_revision(researcher_id, submission_id)