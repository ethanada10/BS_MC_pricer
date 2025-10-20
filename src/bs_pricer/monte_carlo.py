"""
Monte Carlo pricer for European options under GBM with variance reduction.
"""
from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Literal, Tuple, Dict
import numpy as np

OptionType = Literal["call", "put"]

@dataclass
class MCResult:
    price: float
    stderr: float
    ci95: Tuple[float, float]
    elapsed_sec: float
    meta: Dict[str, float]

def _payoff(ST: np.ndarray, K: float, option: OptionType) -> np.ndarray:
    if option == "call":
        return np.maximum(ST - K, 0.0)
    else:
        return np.maximum(K - ST, 0.0)

def _simulate_terminal(S0: float, r: float, sigma: float, T: float, Z: np.ndarray) -> np.ndarray:
    mu = (r - 0.5 * sigma * sigma) * T
    vol = sigma * np.sqrt(T)
    return S0 * np.exp(mu + vol * Z)

def mc_price(
    S0: float, K: float, T: float, r: float, sigma: float,
    option: OptionType = "call",
    n_paths: int = 100_000,
    n_steps: int = 1,
    antithetic: bool = False,
    moment_matching: bool = True,
    seed: int | None = 42,
) -> MCResult:
    """
    Monte Carlo GBM pricer.
    - If n_steps==1, simulate terminal directly (fastest, unbiased).
    - antithetic: use Z and -Z to reduce variance.
    - moment_matching: force sample mean≈0 and std≈1.
    """
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)

    # Draw shocks
    N = n_paths if not antithetic else (n_paths // 2)
    Z = rng.normal(size=N)

    if moment_matching:
        Z = (Z - Z.mean()) / (Z.std(ddof=1) + 1e-12)

    if antithetic:
        Z = np.concatenate([Z, -Z], axis=0)

    if n_steps <= 1:
        ST = _simulate_terminal(S0, r, sigma, T, Z)
    else:
        # Pathwise GBM (Euler exact for GBM increments)
        dt = T / n_steps
        nudt = (r - 0.5 * sigma * sigma) * dt
        sigsdt = sigma * np.sqrt(dt)
        S = np.full(Z.shape[0], S0, dtype=float)
        # For multi-step we need a matrix of normals
        Z_steps = rng.normal(size=(Z.shape[0], n_steps))
        if moment_matching:
            Z_steps = (Z_steps - Z_steps.mean()) / (Z_steps.std(ddof=1) + 1e-12)
        for j in range(n_steps):
            S *= np.exp(nudt + sigsdt * Z_steps[:, j])
        ST = S

    payoff = _payoff(ST, K, option)
    disc = np.exp(-r * T)
    disc_payoff = disc * payoff

    price = disc_payoff.mean()
    std = disc_payoff.std(ddof=1)
    stderr = std / np.sqrt(disc_payoff.shape[0])
    ci95 = (price - 1.96 * stderr, price + 1.96 * stderr)
    elapsed = time.perf_counter() - t0

    return MCResult(
        price=price,
        stderr=stderr,
        ci95=ci95,
        elapsed_sec=elapsed,
        meta={
            "n_paths": float(n_paths if not antithetic else 2*(n_paths//2)),
            "n_steps": float(n_steps),
            "antithetic": float(bool(antithetic)),
            "moment_matching": float(bool(moment_matching)),
            "std": float(std),
        },
    )
