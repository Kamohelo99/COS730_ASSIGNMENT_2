import random
from optimised.controllers.submission_controller import SubmissionController

RANDOM_SEED = 42

def main():
    controller = SubmissionController()
    
    # Valid submission
    print("=" * 70)
    print("TEST 1: Valid Submission")
    print("=" * 70)
    print(f"SYSTEM LOG: Optimized Submission Process (Seed: {RANDOM_SEED})")
    print("=" * 70)
    random.seed(RANDOM_SEED)
    controller.submit({
        "title": "Deep Learning for NLP",
        "abstract": "This paper explores the application of transformer models in natural language processing tasks including classification and generation.",
        "author_id": "researcher_01",
        "content": "Full paper content here..."
    })

    # Invalid submission
    print("\n" + "=" * 70)
    print("TEST 2: Invalid Submission")
    print("=" * 70)
    print(f"SYSTEM LOG: Optimized Submission Process (Seed: {RANDOM_SEED})")
    print("=" * 70)
    random.seed(RANDOM_SEED)
    controller.submit({
        "title": "Short",
        "abstract": "Too short",
        "author_id": "researcher_02",
        "content": ""
    })

    if __name__ == "__main__":
        main()