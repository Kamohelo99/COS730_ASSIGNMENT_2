import pytest
import random
from unittest.mock import patch
from optimised.controllers.submission_controller import SubmissionController

RANDOM_SEED = 42

VALID_DATA = {
    "title": "Deep Learning for NLP",
    "abstract": "This is a sufficiently long abstract that meets the minimum length requirement for validation purposes.",
    "author_id": "researcher_01",
    "content": "Full content here..."
}

INVALID_DATA = {
    "title": "Short",
    "abstract": "Too short",
    "author_id": "researcher_02",
    "content": ""
}

def test_valid_submission_returns_decision():
    """Matches Interaction 16: startEvaluation returns a decision string."""
    random.seed(RANDOM_SEED)
    ctrl = SubmissionController()
    # In the optimized version, we return the decision or a success status
    result = ctrl.submit(VALID_DATA)
    # If your controller returns the status dict:
    assert result["status"] == "success"
    assert result["decision"] in ["accepted", "rejected", "revision"]

def test_invalid_submission_returns_error():
    """Matches Interaction 7: notifyError/returnError."""
    ctrl = SubmissionController()
    result = ctrl.submit(INVALID_DATA)
    assert result["status"] == "error"
    assert "message" in result

def test_high_scores_lead_to_acceptance():
    """Verifies Interaction 27: applyRules() -> accepted."""
    ctrl = SubmissionController()
    with patch("random.uniform", return_value=9.0):
        result = ctrl.submit(VALID_DATA)
    assert result["decision"] == "accepted"

def test_low_scores_lead_to_rejection():
    """Verifies Interaction 27: applyRules() -> rejected."""
    ctrl = SubmissionController()
    with patch("random.uniform", return_value=2.0):
        result = ctrl.submit(VALID_DATA)
    assert result["decision"] == "rejected"

def test_mid_scores_lead_to_revision():
    """Verifies Interaction 27: applyRules() -> revision."""
    ctrl = SubmissionController()
    with patch("random.uniform", return_value=5.5):
        result = ctrl.submit(VALID_DATA)
    assert result["decision"] == "revision"

def test_missing_abstract_is_rejected():
    """Matches the Validator's logic in Interaction 5."""
    ctrl = SubmissionController()
    data = {**VALID_DATA, "abstract": ""}
    result = ctrl.submit(data)
    assert result["status"] == "error"

def test_missing_content_is_rejected():
    """Matches the Validator's logic in Interaction 5."""
    ctrl = SubmissionController()
    data = {**VALID_DATA, "content": ""}
    result = ctrl.submit(data)
    assert result["status"] == "error"

def test_functional_equivalence_with_baseline():
    """
    Ensures that for the same score, both the baseline God Controller
    and the Optimized Service-Oriented approach arrive at the same conclusion.
    """
    from baseline.controllers.submission_controller import SubmissionController as BaseCtrl

    for score, expected in [(9.0, "accepted"), (2.0, "rejected"), (5.5, "revision")]:
        # Reset seeds to ensure reviewer selection/scores are comparable if needed
        random.seed(RANDOM_SEED)
        with patch("random.uniform", return_value=score):
            baseline_result = BaseCtrl().submit(VALID_DATA)
            
            random.seed(RANDOM_SEED)
            optimised_result = SubmissionController().submit(VALID_DATA)

        # Baseline usually returns status as the decision; check your baseline/optimized return formats
        b_status = baseline_result["status"] if isinstance(baseline_result, dict) else baseline_result
        o_status = optimised_result["decision"]
        
        assert b_status == o_status, f"Mismatch at {score}: Baseline={b_status}, Optimised={o_status}"