# Traceability: Validator lifeline — validateFormat(data) → valid/invalid

class Validator:
    def validate_format(self, data: dict) -> bool:
        """
        Diagram: SubmissionController → Validator: validateFormat(data)
        Returns valid/invalid signal back to SubmissionController.
        Intentional smell: validation logic is thin, all rules are checked here
        even though some belong to domain logic.
        """
        required_fields = ["title", "abstract", "author_id", "content"]
        for field in required_fields:
            if field not in data or not data[field]:
                print(f"  ├── [Validator] validate_format() -> FAILED (missing: {field})")
                return False
        if len(data.get("abstract", "")) < 50:
            print("  ├── [Validator] validate_format() -> FAILED (abstract too short)")
            return False
        print("  ├── [Validator] validate_format() -> SUCCESS")
        return True