import json
from typing import Dict, List, Any

class DataQualityEvaluator:
    """
    Core Evaluation Engine for AIG Data Quality Platform.
    Evaluates datasets for Schema Completeness, Text Quality, and Format Integrity.
    """
    
    def __init__(self, dataset: List[Dict[str, Any]]):
        self.dataset = dataset
        self.total_records = len(dataset)

    def evaluate_completeness(self) -> Dict[str, Any]:
        """Calculates percentage of non-null fields across all records."""
        if not self.dataset:
            return {"score": 0.0, "status": "FAIL", "reason": "Empty dataset"}

        total_fields = 0
        null_fields = 0

        for record in self.dataset:
            for k, v in record.items():
                total_fields += 1
                if v is None or (isinstance(v, str) and v.strip() == ""):
                    null_fields += 1

        score = round(((total_fields - null_fields) / total_fields) * 100, 2) if total_fields else 0.0
        return {
            "metric": "Completeness",
            "score_pct": score,
            "null_count": null_fields,
            "total_fields": total_fields,
            "status": "PASS" if score >= 85.0 else "FAIL"
        }

    def evaluate_text_length(self, min_words: int = 3) -> Dict[str, Any]:
        """Checks text fields for overly short or low-quality responses."""
        short_responses = 0
        text_fields_checked = 0

        for record in self.dataset:
            for k, v in record.items():
                if isinstance(v, str):
                    text_fields_checked += 1
                    word_count = len(v.split())
                    if word_count < min_words:
                        short_responses += 1

        pass_rate = round(((text_fields_checked - short_responses) / text_fields_checked) * 100, 2) if text_fields_checked else 100.0
        return {
            "metric": "Text Substantiveness",
            "score_pct": pass_rate,
            "short_text_count": short_responses,
            "status": "PASS" if pass_rate >= 80.0 else "WARN"
        }

    def run_all(self) -> Dict[str, Any]:
        """Runs full suite of evaluations and returns consolidated results."""
        return {
            "summary": {
                "total_records": self.total_records,
            },
            "metrics": [
                self.evaluate_completeness(),
                self.evaluate_text_length()
            ]
        }

if __name__ == "__main__":
    sample_dataset = [
        {"prompt": "Generate a test report", "response": "This is a comprehensive test report generated successfully."},
        {"prompt": "Translate hello to Spanish", "response": "Hola"},
        {"prompt": "Summarize article", "response": None}
    ]

    engine = DataQualityEvaluator(sample_dataset)
    print(json.dumps(engine.run_all(), indent=4))