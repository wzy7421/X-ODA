from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


TABLE_MAP = {
    "baseline_latency": "table2_baseline_latency.csv",
    "ood_generalization": "table3_ood_generalization.csv",
    "xai_benchmark": "table4_xai_benchmark.csv",
    "agent_workflow": "table5_agent_workflow.csv",
    "user_study": "table6_user_study_stats.csv",
}


def to_markdown(df: pd.DataFrame) -> str:
    headers = [str(col) for col in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def load_results(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_tables(data: dict, out_dir: Path) -> None:
    for key, filename in TABLE_MAP.items():
        df = pd.DataFrame(data[key])
        df.to_csv(out_dir / filename, index=False, encoding="utf-8-sig")
        (out_dir / filename.replace(".csv", ".md")).write_text(
            to_markdown(df),
            encoding="utf-8",
        )


def plot_user_study(data: dict, out_dir: Path) -> None:
    rows = data["user_study"]
    labels = [row["outcome"] for row in rows]
    manual = np.array([row["manual"] for row in rows], dtype=float)
    xoda = np.array([row["xoda"] for row in rows], dtype=float)

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.3), dpi=300)
    palette = {"manual": "#6b7280", "xoda": "#0f766e"}
    for ax, label, m, x in zip(axes, labels, manual, xoda):
        ax.bar([0, 1], [m, x], color=[palette["manual"], palette["xoda"]], width=0.62)
        ax.set_xticks([0, 1], ["Manual", "X-ODA"], rotation=20)
        ax.set_title(label, fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e5e7eb", linewidth=0.8)
        ax.set_axisbelow(True)
        ymax = max(m, x) * 1.25
        ax.set_ylim(0, ymax)
        ax.text(0, m + ymax * 0.03, f"{m:g}", ha="center", fontsize=8)
        ax.text(1, x + ymax * 0.03, f"{x:g}", ha="center", fontsize=8)
    fig.suptitle("Fig. 9. User-study outcomes for manual review vs X-ODA-assisted review", fontsize=11)
    fig.tight_layout()
    fig.savefig(out_dir / "fig9_user_study_summary.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("data/provisional_revision_results.json"))
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    data = load_results(args.results)
    write_tables(data, args.out)
    plot_user_study(data, args.out)
    print(f"Wrote revision outputs to {args.out.resolve()}")


if __name__ == "__main__":
    main()
