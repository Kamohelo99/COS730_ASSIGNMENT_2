# Traceability: Validator lifeline — validateFormat(data) → valid/invalid

class Validator:
    def validate_format(self, data: dict) -> bool:
        """
        Diagram: SubmissionController → Validator: validateFormat(data) 
        Returns valid/invalid signal back to SubmissionController.
        """
        required_fields = ["title", "abstract", "author_id", "content"]
        
        # Checking for presence and content of required fields
        for field in required_fields:
            if field not in data or not data[field]:
                print(f"  ├── [Validator] validate_format() -> FAILED (missing or empty: {field})")
                return False
        
        # Specific domain rule: Abstract length check
        if len(data.get("abstract", "")) < 50:
            print(f"  ├── [Validator] validate_format() -> FAILED (abstract too short: {len(data['abstract'])} chars)")
            return False
            
        print("  ├── [Validator] validate_format() -> SUCCESS")
        return True