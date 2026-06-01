from __future__ import annotations

import json
from pathlib import Path


REQUIRED_KEYS = {
    "metadata",
    "baseline_latency",
    "ood_generalization",
    "xai_benchmark",
    "agent_workflow",
    "user_study",
}


def main() -> None:
    path = Path("data/provisional_revision_results.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise SystemExit(f"Missing keys: {sorted(missing)}")
    if data["metadata"].get("status") != "provisional_author_replaceable":
        raise SystemExit("metadata.status must remain explicit until final logs replace provisional values.")
    if len(data["baseline_latency"]) != 10:
        raise SystemExit("Expected 9 baselines plus X-ODA in baseline_latency.")
    if len(data["ood_generalization"]) != 2:
        raise SystemExit("Expected primary optical and OOD CBCT rows.")
    print("Revision result schema OK")


if __name__ == "__main__":
    main()

