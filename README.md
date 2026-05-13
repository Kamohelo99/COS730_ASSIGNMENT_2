# COS730 Assignment 2 — Intelligent Submission & Review System

A Python-based Intelligent Submission and Review System. The project implements and empirically compares a **baseline** architecture against an **optimised** architecture, benchmarking key performance characteristics across both implementations.

---

## Project Structure

```
COS720_ASSIGNMENT_2/
│
├── baseline/                        # Baseline implementation
│   ├── controllers/
│   │   └── submission_controller.py # Handles submission flow logic
│   ├── models/
│   │   └── submission.py            # Submission data model
│   ├── services/
│   │   ├── database.py              # Database access layer
│   │   ├── evaluation_manager.py    # Manages submission evaluation
│   │   ├── notification_service.py  # Sends notifications to users
│   │   ├── reviewer_manager.py      # Assigns and manages reviewers
│   │   └── validator.py             # Validates submission data
│   ├── ui/
│   │   └── ui.py                    # CLI/UI interface
│   └── main.py                      # Baseline entry point
│
├── optimised/                       # Optimised implementation
│   ├── controllers/
│   │   └── submission_controller.py # Optimised submission controller
│   ├── models/
│   │   └── submission.py            # Optimised submission model
│   ├── services/
│   │   ├── evaluation_service.py    # Refactored evaluation service
│   │   ├── notification_service.py  # Optimised notification service
│   │   ├── reviewer_service.py      # Optimised reviewer service
│   │   └── validation_service.py   # Optimised validation service
│   └── main.py                      # Optimised entry point
│
├── benchmarks/                      # Performance benchmarking module
│   ├── results/                     # Stored benchmark output files
│   ├── benchmark_runner.py          # Runs benchmarks on both implementations
│   ├── count_methods.py             # Utility: counts methods across modules
│   └── __init__.py
│
├── tests/                           # Test suite
│   ├── test_baseline.py             # Unit/integration tests for baseline
│   ├── test_optimised.py            # Unit/integration tests for optimised
│   └── __init__.py
│
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## System Overview

The system models a university-style **submission and peer review pipeline**, where students submit work, reviewers are assigned, submissions are validated and evaluated, and notifications are dispatched throughout the process.

Two implementations are provided:

| Feature | Baseline | Optimised |
|---|---|---|
| Architecture style | Monolithic services | Separated service layer |
| Reviewer handling | `reviewer_manager.py` | `reviewer_service.py` |
| Evaluation handling | `evaluation_manager.py` | `evaluation_service.py` |
| Validation | `validator.py` | `validation_service.py` |
| DB layer | `database.py` (inline) | Abstracted in service layer |

---

## Getting Started

### Prerequisites

- Python 3.10+
- `pip` or `poetry`

### Installation

```bash
# Extract the submitted zip file
unzip COS720_ASSIGNMENT_2.zip
cd COS720_ASSIGNMENT_2

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Baseline

```bash
python -m baseline/main.py
```

### Running the Optimised Version

```bash
python -m optimised/main.py
```

---

## Running Tests

```bash
# Run all tests
pytest tests/

# Run baseline tests only
pytest tests/test_baseline.py

# Run optimised tests only
pytest tests/test_optimised.py

# With verbose output
pytest tests/ -v
```

---

## Running Benchmarks

```bash
# Run the full benchmark suite (compares both implementations)
python benchmarks/benchmark_runner.py

# Count methods across the codebase (compares both implementations)
python benchmarks/count_methods.py
```

Benchmark results are saved to `benchmarks/results/`.

---

## Design & Architecture

### Baseline Architecture

The baseline uses a **procedural service design** where each service (evaluation, notification, reviewer, validation) operates as a standalone module with direct dependencies. This was intentionally kept simple to serve as a performance and complexity baseline.

### Optimised Architecture

The optimised version applies the following improvements:

- **Single Responsibility Principle**: Each service has a clearly scoped role (`evaluation_service`, `reviewer_service`, `validation_service`)
- **Reduced coupling**: Services communicate through defined interfaces rather than direct imports
- **Improved testability**: Separation of concerns makes each service independently testable

### Decision Table

The system uses a decision table within the evaluation pipeline to determine submission outcomes based on multiple input conditions (e.g. completeness, deadline compliance, reviewer availability).

---

## Empirical Evaluation

Both implementations were benchmarked across the following metrics:

- **Method Call Count** 
- **Execution Time**
- **Source Lines of Code (SLOC)** 
- **MI and Public Methods**
- **Cyclomatic complexity** of core modules
- **Ease of Change Analysis**

Results are stored in `benchmarks/results/` and analysed in the accompanying assignment report.

---

## Author

**Kamohelo**
COS720 — Honours Software Engineering  
University of Pretoria
