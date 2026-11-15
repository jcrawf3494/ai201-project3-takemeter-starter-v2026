"""Three measured trials of the Capstone criteria using a real trained model.

Run twice on the same checkpoint: --phase before, then --phase after following
one diagnosed change. Never treat mock test results as production metrics.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

from takemeter_inference import LABELS, InvalidOpinion, classify_opinion, load_trained_model

# Synthetic inputs only: safe to report sanitized log records in the README.
OPINIONS = [
    "Cooking classes should be required in every school.",
    "I enjoy rainy walks more than sunny afternoons.",
    "Public transit should run more frequently on weekends.",
    "I like having breakfast food for dinner.",
    "Movies are getting unnecessarily long.",
    "Remote work policies should offer flexible hours.",
    "People overrate expensive coffee.",
    "I prefer handwritten notes to digital notebooks.",
    "School lunches should offer more vegetarian options.",
    "Video games can help people develop problem-solving skills.",
]
INVALID = ["", " ", None, "A" * 3001, "B" * 3500, " C" * 2000]


def trial(predictor, number: int, log_path: Path) -> dict:
    valid = matched = under_five = invalid_rejected = 0
    latencies_ms = []
    first = len(log_path.read_text(encoding="utf-8").splitlines()) if log_path.exists() else 0

    for opinion in OPINIONS:
        # The direct path must invoke the same actual trained model, not a mock.
        direct_label, _ = predictor(opinion.strip())
        output = classify_opinion(opinion, predictor, log_path=log_path)
        if output["label"] in LABELS and math.isfinite(output["confidence"]) and 0 <= output["confidence"] <= 1:
            valid += 1
        if output["label"] == direct_label:
            matched += 1
        entry = json.loads(log_path.read_text(encoding="utf-8").splitlines()[-1])
        duration = entry["duration_ms"]
        latencies_ms.append(duration)
        if duration < 5000:
            under_five += 1

    for bad in INVALID:
        try:
            classify_opinion(bad, predictor, log_path=log_path)
        except InvalidOpinion:
            invalid_rejected += 1

    new_records = [
        json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()[first:]
    ]
    complete = sum(
        1 for record in new_records
        if all(key in record for key in ("timestamp", "input", "output", "duration_ms", "status", "error"))
        and "length" in record["input"] and record["input"].get("sha256")
        and isinstance(record["duration_ms"], (int, float))
    )
    return {
        "trial": number,
        "valid_predictions": f"{valid}/10",
        "invalid_rejections": f"{invalid_rejected}/6",
        "structured_logs": f"{complete}/{len(new_records)}",
        "under_5_seconds": f"{under_five}/10",
        "model_agreement": f"{matched}/10",
        "mean_wall_seconds_per_request": statistics.mean(latencies_ms) / 1000,
        "total_wall_seconds": sum(latencies_ms) / 1000,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="./deployment_model")
    parser.add_argument("--phase", required=True, choices=["before", "after"])
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    predictor = load_trained_model(args.model)
    predictor(OPINIONS[0])  # warm-up, exclude first model load
    log_path = Path(f"logs/{args.phase}_trial_events.jsonl")
    if log_path.exists():
        log_path.unlink()
    records = [trial(predictor, number, log_path) for number in range(1, 4)]
    mean_s = statistics.mean(row["mean_wall_seconds_per_request"] for row in records)
    summary = {
        "phase": args.phase,
        "model": args.model,
        "trials": records,
        "mean_wall_seconds_per_valid_request": mean_s,
        "log_file": str(log_path),
    }
    output = Path(args.out or f"capstone_results_{args.phase}.json")
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |")
    print("|---|---|---|---|---|---|")
    checks = [
        ("Valid predictions", "10/10", "valid_predictions", lambda s: s == "10/10"),
        ("Invalid inputs rejected", "6/6", "invalid_rejections", lambda s: s == "6/6"),
        ("Structured records", "16/16", "structured_logs", lambda s: s == "16/16"),
        ("Predictions under 5 seconds", ">=9/10", "under_5_seconds", lambda s: int(s.split("/")[0]) >= 9),
        ("Matches direct model", "10/10", "model_agreement", lambda s: s == "10/10"),
    ]
    for name, target, key, passes in checks:
        vals = [row[key] for row in records]
        verdict = "MET" if all(passes(value) for value in vals) else "MISSED"
        print(f"| {name} | {target} | {vals[0]} | {vals[1]} | {vals[2]} | {verdict} |")
    print(f"\nMeasured mean warm wall time: {mean_s:.4f} seconds/request")
    print(f"At 100 requests/day: {100 * mean_s:.2f} seconds of warm inference wall time/day")
    print(f"Summary: {output}; log file: {log_path}")
    print("Keep private model/input logs and credentials out of GitHub.")


if __name__ == "__main__":
    main()
