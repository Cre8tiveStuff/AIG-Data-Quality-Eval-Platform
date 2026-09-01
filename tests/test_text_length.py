import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.evaluators import DataQualityEvaluator


def test_text_length_all_substantive():
    dataset = [
        {"response": "This is a perfectly good response."},
        {"response": "Another solid answer here."},
    ]
    evaluator = DataQualityEvaluator(dataset)
    result = evaluator.evaluate_text_length(min_words=3)

    assert result["short_text_count"] == 0
    assert result["score_pct"] == 100.0
    assert result["status"] == "PASS"


def test_text_length_some_short():
    dataset = [
        {"response": "Hola"},
        {"response": "This is a good long answer."},
    ]
    evaluator = DataQualityEvaluator(dataset)
    result = evaluator.evaluate_text_length(min_words=3)

    assert result["short_text_count"] == 1
    assert result["status"] == "WARN"


def test_text_length_custom_min_words_threshold():
    dataset = [
        {"response": "Short answer here"},
    ]
    evaluator = DataQualityEvaluator(dataset)

    result_strict = evaluator.evaluate_text_length(min_words=5)
    assert result_strict["short_text_count"] == 1

    result_lenient = evaluator.evaluate_text_length(min_words=2)
    assert result_lenient["short_text_count"] == 0


def test_text_length_no_text_fields():
    dataset = [
        {"score": 42, "active": True},
    ]
    evaluator = DataQualityEvaluator(dataset)
    result = evaluator.evaluate_text_length()

    assert result["score_pct"] == 100.0
    assert result["status"] == "PASS"