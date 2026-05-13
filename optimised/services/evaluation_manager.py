class EvaluationManager:
    def __init__(self, notification_service):
        self.notification_service = notification_service
        self._scores = {}

    def receive_score(self, submission_id: str, reviewer_id: str, score: float):
        # Traceability: [Reviewer Actor] -> submitScore(score)
        if submission_id not in self._scores:
            self._scores[submission_id] = {}
        self._scores[submission_id][reviewer_id] = score
        print(f"      ├── [EvaluationManager] saveScore() -> {score} from {reviewer_id}") 

    def start_evaluation(self, researcher_id: str, submission_id: str):
        # Traceability: [EvaluationManager] startEvaluation()
        print(f"  └── [EvaluationManager] startEvaluation({submission_id})") 
        
        scores = self._scores.get(submission_id, {})
        avg = self._calculate_average(scores)
        cons = self._check_consensus(scores) 
        decision = self._apply_rules(avg, cons) 
        
        print(f"      └── [EvaluationManager] notifyDecision({decision})") 
        self.notification_service.send_notification(researcher_id, submission_id, decision) 
        return decision

    def _calculate_average(self, scores):
        vals = list(scores.values())
        avg = sum(vals) / len(vals) if vals else 0.0
        print(f"      ├── [EvaluationManager] calculateAverage() -> {avg:.2f}") 
        return avg

    def _check_consensus(self, scores):
        vals = list(scores.values())
        reached = (max(vals) - min(vals)) <= 2.0 if vals else False
        print(f"      ├── [EvaluationManager] checkConsensus() -> {'YES' if reached else 'NO'}") 
        return reached

    def _apply_rules(self, avg, consensus):
        if avg >= 7.0 and consensus: return "accepted"
        if avg < 4.0: return "rejected"
        return "revision" 