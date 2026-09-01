import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.evaluators import DataQualityEvaluator


def test_evaluate_completeness_all_fields_present():
    dataset = [
        {"prompt": "Hello", "response": "World"},
        {"prompt": "Test", "response": "Value"},
    ]
    evaluator = DataQualityEvaluator(dataset)
    result = evaluator.evaluate_completeness()

    assert result["score_pct"] == 100.0
    assert result["null_count"] == 0
    assert result["status"] == "PASS"


def test_evaluate_completeness_with_nulls():
    dataset = [
        {"prompt": "Hello", "response": None},
        {"prompt": "Test", "response": "Value"},
    ]
    evaluator = DataQualityEvaluator(dataset)
    result = evaluator.evaluate_completeness()

    assert result["null_count"] == 1
    assert result["total_fields"] == 4
    assert result["score_pct"] == 75.0


def test_evaluate_completeness_empty_dataset():
    evaluator = DataQualityEvaluator([])
    result = evaluator.evaluate_completeness()

    assert result["score"] == 0.0
    assert result["status"] == "FAIL"