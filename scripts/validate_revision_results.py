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

REQUIRED_XAI_METHODS = {
    "Grad-CAM",
    "SHAP",
    "LIME",
    "Integrated Gradients",
    "Score-CAM",
    "Eigen-CAM",
}

REQUIRED_AGENT_SEVERITIES = {"Normal", "Early", "Progressing", "Severe", "Overall"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def check_percent(value: float, field: str) -> None:
    require(0.0 <= float(value) <= 100.0, f"{field} must be in [0, 100].")


def check_ci(ci: list[float], field: str) -> None:
    require(isinstance(ci, list) and len(ci) == 2, f"{field} must be a two-value CI list.")
    lo, hi = map(float, ci)
    require(lo <= hi, f"{field} lower bound must be <= upper bound.")
    check_percent(lo, f"{field}[0]")
    check_percent(hi, f"{field}[1]")


def main() -> None:
    path = Path("data/provisional_revision_results.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS - data.keys()
    require(not missing, f"Missing keys: {sorted(missing)}")
    require(
        data["metadata"].get("status") == "provisional_author_replaceable",
        "metadata.status must remain explicit until final logs replace provisional values.",
    )

    baselines = data["baseline_latency"]
    require(len(baselines) == 10, "Expected 9 baselines plus X-ODA in baseline_latency.")
    require(len({row["model"] for row in baselines}) == 10, "baseline_latency models must be unique.")
    require(any(row["model"] == "X-ODA (VGG16)" for row in baselines), "Missing X-ODA (VGG16) row.")
    for row in baselines:
        for field in ["accuracy", "precision", "recall", "f1", "faithfulness"]:
            check_percent(row[field], f"baseline_latency.{row['model']}.{field}")
        require(float(row["latency_ms"]) > 0, f"{row['model']} latency must be positive.")

    ood_rows = data["ood_generalization"]
    require(len(ood_rows) == 2, "Expected primary optical and OOD CBCT rows.")
    require(
        {row["evaluation_set"] for row in ood_rows} == {"Primary optical test set", "OOD CBCT test set"},
        "OOD table must contain primary optical and OOD CBCT rows.",
    )
    for row in ood_rows:
        require(int(row["n"]) > 0, f"{row['evaluation_set']} n must be positive.")
        for field in ["accuracy", "macro_f1", "faithfulness"]:
            check_percent(row[field], f"ood_generalization.{row['evaluation_set']}.{field}")
            check_ci(row[f"{field}_ci"], f"ood_generalization.{row['evaluation_set']}.{field}_ci")

    xai_methods = {row["method"] for row in data["xai_benchmark"]}
    require(xai_methods == REQUIRED_XAI_METHODS, f"XAI methods mismatch: {sorted(xai_methods)}")
    for row in data["xai_benchmark"]:
        check_percent(row["faithfulness"], f"xai_benchmark.{row['method']}.faithfulness")
        require(0.0 <= float(row["expert_localization_agreement"]) <= 1.0, f"{row['method']} agreement must be in [0, 1].")
        require(float(row["latency_s"]) > 0, f"{row['method']} latency must be positive.")

    workflow = data["agent_workflow"]
    require({row["severity"] for row in workflow} == REQUIRED_AGENT_SEVERITIES, "Agent workflow severity rows mismatch.")
    non_overall_cases = sum(int(row["cases"]) for row in workflow if row["severity"] != "Overall")
    overall = next(row for row in workflow if row["severity"] == "Overall")
    require(int(overall["cases"]) == non_overall_cases, "Overall workflow cases must equal severity-row sum.")
    for row in workflow:
        check_percent(row["action_accuracy"], f"agent_workflow.{row['severity']}.action_accuracy")
        check_percent(row["false_finding_rate"], f"agent_workflow.{row['severity']}.false_finding_rate")
        require(float(row["latency_s"]) > 0, f"{row['severity']} latency must be positive.")

    require(len(data["user_study"]) == 4, "Expected four user-study outcomes.")
    for row in data["user_study"]:
        require("p<" in row["test"] or "p=" in row["test"], f"{row['outcome']} must include a p-value string.")
        require(isinstance(row["ci"], list) and len(row["ci"]) == 2, f"{row['outcome']} CI must have two bounds.")
    print("Revision result schema OK")


if __name__ == "__main__":
    main()
