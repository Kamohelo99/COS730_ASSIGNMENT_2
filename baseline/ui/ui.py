# Traceability: UI lifeline — submitResearchOutput(data), receives sendNotification()


from baseline.controllers.submission_controller import SubmissionController
from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

class UI:
    def __init__(self):
        self.controller = SubmissionController()

    def submit_research_output(self, data: dict):
        print("\n" + "=" * 70)
        print("SYSTEM LOG: Baseline Submission Process (Seed: 42)")
        print("=" * 70)
        print(f"[{ts()}] [UI] Action: submitResearchOutput() initiated.")
        result = self.controller.submit(data)
        print("=" * 70)
        return result