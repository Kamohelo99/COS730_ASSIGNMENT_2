import pytest
import random
from unittest.mock import patch
from baseline.controllers.submission_controller import SubmissionController

RANDOM_SEED = 42

VALID_DATA = {
    "title": "Test Paper",
    "abstract": "This is a sufficiently long abstract that meets the minimum length requirement for validation purposes.",
    "author_id": "researcher_01",
    "content": "Content here"
}

INVALID_DATA = {
    "title": "",
    "abstract": "short",
    "author_id": "",
    "content": ""
}


def test_valid_submission_returns_decision():
    random.seed(RANDOM_SEED)
    ctrl = SubmissionController()
    result = ctrl.submit(VALID_DATA)
    assert result["status"] in ["accepted", "rejected", "revision"]
    assert "submission_id" in result


def test_invalid_submission_returns_error():
    ctrl = SubmissionController()
    result = ctrl.submit(INVALID_DATA)
    assert result["status"] == "error"
    assert "message" in result


def test_high_scores_lead_to_acceptance():
    ctrl = SubmissionController()
    with patch("random.uniform", return_value=9.0):
        result = ctrl.submit(VALID_DATA)
    assert result["status"] == "accepted"


def test_low_scores_lead_to_rejection():
    ctrl = SubmissionController()
    with patch("random.uniform", return_value=2.0):
        result = ctrl.submit(VALID_DATA)
    assert result["status"] == "rejected"


def test_mid_scores_lead_to_revision():
    ctrl = SubmissionController()
    with patch("random.uniform", return_value=5.5):
        result = ctrl.submit(VALID_DATA)
    assert result["status"] == "revision"


def test_seeded_run_is_deterministic():
    """Same seed must always produce the same decision"""
    random.seed(RANDOM_SEED)
    ctrl = SubmissionController()
    result_a = ctrl.submit(VALID_DATA)

    random.seed(RANDOM_SEED)
    ctrl = SubmissionController()
    result_b = ctrl.submit(VALID_DATA)

    assert result_a["status"] == result_b["status"]


def test_missing_abstract_is_rejected():
    ctrl = SubmissionController()
    data = {**VALID_DATA, "abstract": ""}
    result = ctrl.submit(data)
    assert result["status"] == "error"


def test_missing_content_is_rejected():
    ctrl = SubmissionController()
    data = {**VALID_DATA, "content": ""}
    result = ctrl.submit(data)
    assert result["status"] == "error"