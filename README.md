# COS730 Assignment 2 — Intelligent Submission & Review System

A Python-based Intelligent Submission and Review System implementing and empirically
comparing a **baseline** architecture against an **optimised** architecture. The project
demonstrates measurable improvements in execution time, method call count, code complexity,
and maintainability through targeted structural refactoring.

-----

## Project Structure

```
COS730_ASSIGNMENT_2/
│
├── baseline/ # Baseline implementation (faithfully mirrors sequence diagram)
│ ├── controllers/
│ │ └── submission_controller.py # Central orchestrator — drives full submission flow
│ ├── models/
│ │ └── submission.py # Submission and Reviewer dataclasses
│ ├── services/
│ │ ├── database.py # Monolithic database — serves submissions, reviewers, scores
│ │ ├── evaluation_manager.py # Three public self-calls: calculateAverage, checkConsensus, applyRules
│ │ ├── notification_service.py # Three separate outcome methods: notifyAcceptance/Rejection/Revision
│ │ ├── reviewer_manager.py # Two-pass filtering: filterConflicts then checkWorkload
│ │ └── validator.py # Format validation — returns boolean signal
│ ├── ui/
│ │ └── ui.py # UI relay lifeline — forwards calls to SubmissionController
│ └── main.py # Baseline entry point
│
├── optimised/ # Optimised implementation (based on redesigned sequence diagram)
│ ├── controllers/
│ │ └── submission_controller.py # Slim seven-step coordinator — no internal logic
│ ├── models/
│ │ └── submission.py # Submission and Reviewer dataclasses
│ ├── services/
│ │ ├── repositories.py # SubmissionRepository + ReviewerRepository (replaces monolithic DB)
│ │ ├── evaluation_manager.py # Single start_evaluation() entry point; internal steps are private
│ │ ├── notification_service.py # Unified send_notification(decision) dispatcher
│ │ ├── reviewer_manager.py # Single-pass get_available_reviewers() — conflict + workload internalised
│ │ └── validator.py # Format validation — returns boolean signal
│ └── main.py # Optimised entry point
│
├── benchmarks/ # Performance benchmarking module
│ ├── benchmark_runner.py # Runs and compares both implementations across 1000 runs
│ └── __init__.py
│
├── tests/ # Test suite
│ ├── test_baseline.py #  test cases for baseline implementation
│ ├── test_optimised.py #  test cases including functional equivalence test
│ └── __init__.py
│
├── requirements.txt # Python dependencies
└── README.md
```

-----

## System Overview

The system models a university-style submission and peer review pipeline where a researcher
submits work, reviewers are assigned and evaluated, scores are collected, and a final
outcome is determined and communicated. Two implementations are provided:

|Feature |Baseline |Optimised |
|------------------|------------------------------------------------------------|------------------------------------------------|
|Entry point |`UI` relay → `SubmissionController` |Direct `SubmissionController` |
|Persistence layer |Monolithic `Database` class |`SubmissionRepository` + `ReviewerRepository` |
|Reviewer filtering|Two separate passes: `filterConflicts()` + `checkWorkload()`|Single-pass `get_available_reviewers()` |
|Evaluation |Three public self-calls exposed at controller level |Single `start_evaluation()` — internals private |
|Notification |Three outcome-specific methods |Unified `send_notification(decision)` dispatcher|
|Controller fan-out|6 lifelines |5 components, one call each |

-----

## Architecture Differences

### Baseline Architecture

The baseline faithfully implements the provided sequence diagram, preserving all
interactions, lifelines, and responsibility allocations — including intentional design smells:

- **UI Middleman:** The `UI` class acts as a passive relay between the Researcher and
`SubmissionController`, adding call-stack depth without contributing any logic.
- **Monolithic Database:** A single `Database` class is accessed by `SubmissionController`,
`ReviewerManager`, and `EvaluationManager` for unrelated purposes, creating hidden coupling.
- **Split reviewer filtering:** `filterConflicts()` and `checkWorkload()` are separate calls
that each iterate the full reviewer list independently.
- **Exposed evaluation internals:** `calculateAverage()`, `checkConsensus()`, and
`applyRules()` are three public self-calls visible at the controller level.
- **Fragmented notifications:** Three separate methods `notifyAcceptance()`,
`notifyRejection()`, and `notifyRevision()` require the caller to know the decision type.

### Optimised Architecture

The optimised implementation addresses each identified smell through targeted refactoring:

- **UI eliminated:** The Researcher interacts directly with `SubmissionController`,
removing the Middleman relay and reducing call-stack depth on every execution path.
- **Database decomposed:** `SubmissionRepository` owns submission persistence;
`ReviewerRepository` owns reviewer retrieval. Each component depends only on its
relevant repository.
- **Filtering consolidated:** `ReviewerManager.get_available_reviewers()` performs conflict
and workload checks in a single method, internalising both concerns.
- **Evaluation encapsulated:** `_calculate_average()`, `_check_consensus()`, and
`_apply_rules()` are private methods. The controller calls `start_evaluation()` and
receives a decision string — with no knowledge of the internal computation steps.
- **Notification unified:** `send_notification(decision)` owns the routing logic internally.
Adding a new outcome type requires only a new branch — no interface change, no controller
modification.

-----

## Decision Logic

The evaluation pipeline implements a three-rule decision table:

|Condition |Rule 1 |Rule 2 |Rule 3 |Rule 4 |
|-------------------------------|------------|------------|------------|------------|
|Average score ≥ 7.0 |Y |Y |N |N |
|Average score < 4.0 |N |N |Y |N |
|Consensus reached (range ≤ 2.0)|Y |N |— |— |
|**Decision** |**Accepted**|**Revision**|**Rejected**|**Revision**|

This is implemented in `EvaluationManager._apply_rules()`:

```python
def _apply_rules(self, avg, consensus):
if avg >= 7.0 and consensus: return "accepted" # Rule 1
if avg < 4.0: return "rejected" # Rule 3
return "revision" # Rules 2 and 4
```

-----

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/Kamohelo99/COS730_ASSIGNMENT_2.git
cd COS730_ASSIGNMENT_2
pip install -r requirements.txt
```

### Running the Baseline

```bash
python -m baseline.main
```

### Running the Optimised Version

```bash
python -m optimised.main
```

-----

## Running Tests

```bash
# Run all tests
pytest tests/

# Run baseline tests only
pytest tests/test_baseline.py -v

# Run optimised tests only
pytest tests/test_optimised.py -v
```

Both test suites are executed under a fixed random seed of 42 for deterministic results.
The optimised suite includes all 8 baseline test cases.

-----

## Running Benchmarks

```bash
# Run full benchmark suite — compares both implementations over 1000 runs
python -m benchmarks.benchmark_runner

```

-----

## Empirical Results

Both implementations were benchmarked under identical conditions with seed 42 across
1,000 repeated runs:

|Metric |Baseline|Optimised|Change |
|--------------------------|--------|---------|-------|
|Mean Execution Time |1.061ms |0.920ms |−13.3% |
|Method Calls |153 |113 |−26.1% |
|SLOC |55 |39 |−29.1% |
|Cyclomatic Complexity (CC)|4 |4 |0% |
|Maintainability Index (MI)|87.28% |88.32% |+1.04pp|
|Halstead Volume |272.48 |168.56 |−38.1% |
|Halstead Difficulty |1.47 |0 |−100% |
|Efferent Coupling (CBO) |5 |5 |0% |

CC and CBO remaining constant confirms the optimisation targeted structural redundancy
without altering business logic or introducing new dependencies.

-----

## Author

**Kamohelo** — u25721616
COS730 Honours Software Engineering
University of Pretoria