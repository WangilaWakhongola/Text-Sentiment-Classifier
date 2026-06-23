"""
CLI runner for batch sentiment classification from a CSV file.

Usage:
    python run.py --input sample_data.csv --text-col text --output results.csv
"""

import argparse
import csv
import sys
import time
from classifier import classify_batch


def load_csv(filepath: str, text_col: str) -> tuple[list[str], list[dict]]:
    """Load texts from a CSV file. Returns (texts, original_rows)."""
    texts = []
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if text_col not in reader.fieldnames:
            print(f"[ERROR] Column '{text_col}' not found in CSV.")
            print(f"        Available columns: {', '.join(reader.fieldnames)}")
            sys.exit(1)
        for row in reader:
            texts.append(row[text_col])
            rows.append(row)
    return texts, rows


def save_csv(filepath: str, rows: list[dict], results: list[dict], original_fields: list[str]):
    """Save original rows + classification results to a new CSV."""
    out_fields = original_fields + ["sentiment", "confidence", "reason"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for row, result in zip(rows, results):
            writer.writerow({**row, **result})


def print_summary(results: list[dict]):
    """Print a quick summary of classification results."""
    from collections import Counter
    counts = Counter(r["sentiment"] for r in results)
    total = len(results)
    print("\n--- Summary ---")
    for label in ["positive", "negative", "neutral", "error"]:
        count = counts.get(label, 0)
        pct = (count / total * 100) if total else 0
        bar = "█" * int(pct / 5)
        print(f"  {label:<10} {count:>4}  ({pct:5.1f}%)  {bar}")
    print(f"  {'TOTAL':<10} {total:>4}")


def main():
    parser = argparse.ArgumentParser(description="Batch sentiment classifier using Claude API.")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--text-col", default="text", help="Name of the column containing text (default: 'text')")
    parser.add_argument("--output", default="results.csv", help="Path to output CSV file (default: results.csv)")
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds to wait between API calls (default: 0.2)")
    args = parser.parse_args()

    print(f"[INFO] Loading '{args.input}'...")
    texts, rows = load_csv(args.input, args.text_col)
    print(f"[INFO] Loaded {len(texts)} rows. Starting classification...\n")

    results = []
    for i, text in enumerate(texts, 1):
        print(f"  [{i}/{len(texts)}] {text[:60]}{'...' if len(text) > 60 else ''}", end=" ")
        try:
            from classifier import classify_text
            result = classify_text(text)
            print(f"-> {result['sentiment']} ({result['confidence']:.0%})")
        except Exception as e:
            result = {"sentiment": "error", "confidence": 0.0, "reason": str(e)}
            print(f"-> error: {e}")
        results.append(result)
        if i < len(texts):
            time.sleep(args.delay)

    original_fields = list(rows[0].keys()) if rows else []
    save_csv(args.output, rows, results, original_fields)
    print(f"\n[INFO] Results saved to '{args.output}'")
    print_summary(results)


if __name__ == "__main__":
    main()
