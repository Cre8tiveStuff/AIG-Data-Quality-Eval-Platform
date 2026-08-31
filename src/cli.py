import argparse
import json
import sys
from pathlib import Path

# Import our custom modules from the src package
from src.loaders import load_dataset
from src.evaluators import DataQualityEvaluator

def main():
    # 1. Initialize the Argument Parser with a description
    parser = argparse.ArgumentParser(
        description="AIG Data Quality Evaluation Platform - CLI Tool"
    )

    # 2. Define Command Line Arguments (Flags)
    parser.add_argument(
        "-i", "--input", 
        type=str, 
        required=True, 
        help="Path to the input dataset file (.json, .jsonl, .csv)"
    )
    
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default=None, 
        help="Path to save the output evaluation JSON report (optional)"
    )

    parser.add_argument(
        "--min-words", 
        type=int, 
        default=3, 
        help="Minimum word count threshold for text quality evaluation (default: 3)"
    )

    # 3. Parse arguments supplied by the user in the terminal
    args = parser.parse_args()

    # 4. Load dataset using src/loaders.py
    try:
        print(f"[*] Loading dataset from: {args.input}")
        dataset = load_dataset(args.input)
        print(f"[+] Successfully loaded {len(dataset)} records.")
    except Exception as e:
        print(f"[!] Error loading dataset: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Run evaluation using src/evaluators.py
    print("[*] Running data quality evaluations...")
    evaluator = DataQualityEvaluator(dataset)
    
    # Calculate custom text quality with user-defined min_words flag
    completeness = evaluator.evaluate_completeness()
    text_quality = evaluator.evaluate_text_length(min_words=args.min_words)
    
    results = {
        "summary": {"total_records": evaluator.total_records},
        "metrics": [completeness, text_quality]
    }

    # 6. Format and display/save results
    formatted_output = json.dumps(results, indent=4)
    print("\n=== Evaluation Results ===")
    print(formatted_output)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(formatted_output, encoding="utf-8")
        print(f"\n[+] Results successfully saved to: {args.output}")

if __name__ == "__main__":
    main()