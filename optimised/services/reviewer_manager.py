class ReviewerManager:
    def get_available_reviewers(self, repository, researcher_id: str):
        # Traceability: [ReviewerManager] getAvailableReviewers()
        print("  ├── [ReviewerManager] getAvailableReviewers()") 
        
        all_reviewers = repository.fetch_reviewers() 
        
        # Internalized logic: filterConflicts and checkWorkload
        filtered = [r for r in all_reviewers if researcher_id not in r.conflicts]
        print("  │   ├── [ReviewerManager] filterConflicts() -> PASS") 
        
        available = [r for r in filtered if r.workload < 3]
        print(f"  │   └── [ReviewerManager] checkWorkload() -> PASS (Found {len(available)})") 
        return available

    def assign_review(self, reviewer, submission_id: str):
        # Traceability: [ReviewerManager] assignReview()
        reviewer.workload += 1
        print(f"  ├── [ReviewerManager] assignReview({reviewer.reviewer_id})") 