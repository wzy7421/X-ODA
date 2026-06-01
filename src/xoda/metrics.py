from __future__ import annotations

import numpy as np


def bootstrap_ci(values, n_boot: int = 1000, alpha: float = 0.05, seed: int = 2026):
    """Return percentile bootstrap confidence interval for a 1D numeric vector."""
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size == 0:
        raise ValueError("values must be a non-empty 1D vector")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, arr.size, size=(n_boot, arr.size))
    means = arr[idx].mean(axis=1)
    lo, hi = np.percentile(means, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def relative_confidence_drop(original_confidence: float, masked_confidence: float) -> float:
    """Occlusion faithfulness as relative drop in prediction confidence."""
    if original_confidence <= 0:
        raise ValueError("original_confidence must be positive")
    return (original_confidence - masked_confidence) / original_confidence

