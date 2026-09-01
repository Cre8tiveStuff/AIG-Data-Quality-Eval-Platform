import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.evaluators import DataQualityEvaluator


def test_completeness_treats_nan_as_missing():
    """Regression test: pandas (e.g. from parquet/csv) represents missing
    values as float('nan'), not None. This must be counted as missing too."""
    dataset = [
        {"prompt": "Hello", "response": float("nan")},
        {"prompt": "Test", "response": "Value"},
    ]
    evaluator = DataQualityEvaluator(dataset)
    result = evaluator.evaluate_completeness()

    assert result["null_count"] == 1
    assert result["total_fields"] == 4
    assert result["score_pct"] == 75.0


def test_completeness_still_handles_none_and_empty_string():
    """Make sure the original None/empty-string checks still work
    alongside the new NaN check."""
    dataset = [
        {"a": None, "b": "", "c": "value", "d": float("nan")},
    ]
    evaluator = DataQualityEvaluator(dataset)
    result = evaluator.evaluate_completeness()

    assert result["null_count"] == 3
    assert result["total_fields"] == 4