# Traceability: EvaluationManager lifeline — calculateAverage(), checkConsensus(),
#               applyRules() → decision alt [accepted | rejected | revision]

from typing import List

class EvaluationManager:
    def __init__(self, notification_service):
        self._average = 0.0
        self._consensus = False
        self.notification_service = notification_service

    def calculate_average(self, scores: dict) -> float:
        """
        Diagram: EvaluationManager: calculateAverage() (self-call after scores loop)
        SMELL: Called as a self-message but receives no parameters — relies on side effect state
        """
        values = list(scores.values())
        self._average = sum(values) / len(values) if values else 0.0
        print(f"      ├── [EvaluationManager] calculate_average() -> {self._average:.2f}")
        return self._average

    
    def check_consensus(self, scores: dict) -> bool:
        """
        Diagram: EvaluationManager: checkConsensus() self-call
        SMELL: Called separately from calculateAverage even though it uses same data
        """

        values = list(scores.values())
        self._consensus = (max(values) - min(values)) <= 2.0 if values else False
        status = "REACHED" if self._consensus else "NOT REACHED"
        print(f"      ├── [EvaluationManager] check_consensus()   -> {status}")
        return self._consensus

    def apply_rules(self) -> str:
        """
        Diagram: EvaluationManager: applyRules() self-call
        Then alt [accepted | rejected | revision]
        SMELL: Three separate self-calls (calculateAverage, checkConsensus, applyRules)
               that should be one cohesive evaluate() method
        """
        if self._average >= 7.0 and self._consensus:  # Rule 1
            decision = "ACCEPTED"
        elif self._average < 4.0:  # Rule 3
            decision = "REJECTED"
        else:
            decision = "REVISION"  # Rule 2 and 4
        print(f"      └── [EvaluationManager] apply_rules()       -> {decision}")
        return decision.lower()
    
    def evaluate_and_notify(self, researcher_id: str, submission_id: str, scores: dict):
        """Handles  the logic and triggers the notification service """
        self.calculate_average(scores) 
        self.check_consensus(scores) 
        decision = self.apply_rules()

        # Determine decision
        if self._average >= 7.0 and self._consensus:
            decision = "accepted"
        elif self._average < 4.0:
            decision = "rejected"
        else:
            decision = "revision"

        print(f"      └── [EvaluationManager] Decision: {decision}. Triggering notification...")
        
        #send decision notification
        self.notification_service.send_notification(researcher_id, submission_id, decision)
        return decision