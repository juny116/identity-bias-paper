#!/usr/bin/env python3
"""Generate interface-confound figures from frozen CSV tables."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"

DATASETS = [
    ("aime", "AIME"),
    ("gpqa", "GPQA"),
    ("olympiad", "Olympiad"),
    ("mmlu_pro", "MMLU-Pro"),
]
JUDGES = [
    ("gemma-4-no-think", "Gemma-4"),
    ("gpt-oss-no-think", "gpt-oss"),
    ("qwen3-no-think", "qwen3"),
]
INTERFACES = [
    ("verdict_only", "Verdict\nonly"),
    ("rubric_verdict", "Rubric\nverdict"),
    ("score_then_verdict", "Score\nthen"),
    ("verdict_plus_repair", "Verdict\n+ repair"),
    ("repair_then_verdict", "Repair\nthen"),
]
PAIR_LABELS = {
    ("gemma-4-no-think", "gpt-oss-no-think"): "Gemma - gpt-oss",
    ("gemma-4-no-think", "qwen3-no-think"): "Gemma - qwen3",
    ("gpt-oss-no-think", "qwen3-no-think"): "gpt-oss - qwen3",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def set_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 220,
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def fig_heatmap() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.6), constrained_layout=True)
    norm = Normalize(vmin=50, vmax=95)
    last_im = None

    for ax, (tag, title) in zip(axes.flat, DATASETS):
        rows = read_csv(TABLES / f"ifc_{tag}_per_judge_interface.csv")
        lookup = {(r["judge"], r["interface"]): float(r["balanced_acc_pct"]) for r in rows}
        values = [
            [lookup[(judge, iface)] for iface, _ in INTERFACES]
            for judge, _ in JUDGES
        ]
        last_im = ax.imshow(values, cmap="viridis", norm=norm, aspect="auto")
        ax.set_title(title)
        ax.set_xticks(range(len(INTERFACES)), [label for _, label in INTERFACES])
        ax.set_yticks(range(len(JUDGES)), [label for _, label in JUDGES])
        ax.tick_params(axis="x", rotation=0)

        for y, row in enumerate(values):
            for x, val in enumerate(row):
                color = "white" if val < 68 else "black"
                ax.text(x, y, f"{val:.1f}", ha="center", va="center", color=color, fontsize=8)

        best_by_col = [max(range(len(JUDGES)), key=lambda j: values[j][i]) for i in range(len(INTERFACES))]
        for x, best_y in enumerate(best_by_col):
            ax.scatter([x], [best_y], marker="s", s=260, facecolors="none", edgecolors="white", linewidths=1.6)

    cbar = fig.colorbar(last_im, ax=axes.ravel().tolist(), shrink=0.86, pad=0.02)
    cbar.set_label("Balanced accuracy (%)")
    fig.suptitle("Balanced accuracy by judge, interface, and dataset", y=1.02, fontsize=12)
    fig.savefig(FIGURES / "fig_ifc_heatmap.png", bbox_inches="tight")
    plt.close(fig)


def fig_gap_slopes() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.8), sharey=True, constrained_layout=True)
    colors = {
        "Gemma - gpt-oss": "#1f77b4",
        "Gemma - qwen3": "#2ca02c",
        "gpt-oss - qwen3": "#d62728",
    }
    x = list(range(len(INTERFACES)))
    interface_order = [name for name, _ in INTERFACES]
    interface_labels = [label.replace("\n", " ") for _, label in INTERFACES]

    for ax, (tag, title) in zip(axes.flat, DATASETS):
        rows = read_csv(TABLES / f"ifc_{tag}_pairwise_gaps.csv")
        by_pair: dict[str, dict[str, dict[str, str]]] = {}
        for r in rows:
            pair = (r["judge_a"], r["judge_b"])
            label = PAIR_LABELS.get(pair)
            if label:
                by_pair.setdefault(label, {})[r["interface"]] = r

        for label, iface_rows in by_pair.items():
            ys = [float(iface_rows[i]["bacc_gap_pp"]) for i in interface_order]
            lo = [float(iface_rows[i]["ci_lo"]) for i in interface_order]
            hi = [float(iface_rows[i]["ci_hi"]) for i in interface_order]
            yerr = [[y - l for y, l in zip(ys, lo)], [h - y for y, h in zip(ys, hi)]]
            ax.errorbar(
                x,
                ys,
                yerr=yerr,
                marker="o",
                linewidth=1.6,
                capsize=3,
                color=colors[label],
                label=label,
            )
        ax.axhline(0, color="0.25", linewidth=1, linestyle="--")
        ax.set_title(title)
        ax.set_xticks(x, interface_labels, rotation=24, ha="right")
        ax.set_ylabel("Balanced-accuracy gap (pp)")
        ax.grid(axis="y", color="0.9", linewidth=0.8)

    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.03))
    fig.savefig(FIGURES / "fig_ifc_gap_slopes.png", bbox_inches="tight")
    plt.close(fig)


def fig_think() -> None:
    rows = read_csv(TABLES / "ifc_think_vs_nothink.csv")
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8), sharey=True, constrained_layout=True)
    width = 0.36

    for ax, dataset in zip(axes, ["aime", "gpqa"]):
        drows = [r for r in rows if r["dataset"] == dataset]
        lookup = {(r["condition"], r["judge"]): r for r in drows}
        xs = list(range(len(JUDGES)))
        no_vals = [float(lookup[("no_think", judge)]["interface_range_pp"]) for judge, _ in JUDGES]
        delib_vals = [float(lookup[("deliberation", judge)]["interface_range_pp"]) for judge, _ in JUDGES]
        ax.bar([i - width / 2 for i in xs], no_vals, width=width, label="No deliberation", color="#9ecae1")
        ax.bar([i + width / 2 for i in xs], delib_vals, width=width, label="Deliberation field", color="#fdae6b")
        ax.set_title(dataset.upper() if dataset == "aime" else "GPQA")
        ax.set_xticks(xs, [label for _, label in JUDGES])
        ax.set_ylabel("Interface range (pp)")
        ax.grid(axis="y", color="0.9", linewidth=0.8)
        for i, (nv, dv) in enumerate(zip(no_vals, delib_vals)):
            ax.text(i, max(nv, dv) + 0.35, "2→1\nrankings", ha="center", va="bottom", fontsize=7, color="0.25")

    axes[0].legend(frameon=False, loc="upper right")
    fig.suptitle("Deliberation-in-schema reduces interface sensitivity", y=1.04, fontsize=12)
    fig.savefig(FIGURES / "fig_ifc_think.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    set_style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig_heatmap()
    fig_gap_slopes()
    fig_think()
    print("wrote:")
    for name in ["fig_ifc_heatmap.png", "fig_ifc_gap_slopes.png", "fig_ifc_think.png"]:
        print(f"  {FIGURES / name}")


if __name__ == "__main__":
    main()
