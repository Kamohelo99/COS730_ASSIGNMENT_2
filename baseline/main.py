import random
from baseline.ui.ui import UI

RANDOM_SEED = 42

def main():

    # Valid submission
    print("=" * 70)
    print("TEST 1: Valid Submission")
    random.seed(RANDOM_SEED)
    ui = UI()
    ui.submit_research_output({
        "title": "Deep Learning for NLP",
        "abstract": "This paper explores the application of transformer models in natural language processing tasks including classification and generation.",
        "author_id": "researcher_01",
        "content": "Full paper content here..."
    })

    # Invalid submission
    print("\n" + "=" * 70)
    print("TEST 2: Invalid Submission")
    random.seed(RANDOM_SEED)
    ui = UI()
    ui.submit_research_output({
        "title": "Short",
        "abstract": "Too short",
        "author_id": "researcher_02",
        "content": ""
    })

if __name__ == "__main__":
    main()