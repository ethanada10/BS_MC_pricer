"""
Closed-form Black–Scholes pricer + analytical Greeks for European options.
"""
from math import log, sqrt, exp, erf, pi
from typing import Literal, Dict

OptionType = Literal["call", "put"]

def _phi(x: float) -> float:
    "Standard normal PDF."
    return (1.0 / sqrt(2.0 * pi)) * exp(-0.5 * x * x)

def _Phi(x: float) -> float:
    "Standard normal CDF via error function."
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def _d1(S0: float, K: float, T: float, r: float, sigma: float) -> float:
    return (log(S0 / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))

def _d2(d1: float, sigma: float, T: float) -> float:
    return d1 - sigma * sqrt(T)

def bs_price(S0: float, K: float, T: float, r: float, sigma: float, option: OptionType = "call") -> float:
    """
    Black–Scholes price for European call/put.
    """
    if T <= 0 or sigma <= 0:
        # Handle edge cases gracefully
        intrinsic_call = max(S0 - K, 0.0)
        intrinsic_put = max(K - S0, 0.0)
        return intrinsic_call if option == "call" else intrinsic_put

    d1 = _d1(S0, K, T, r, sigma)
    d2 = _d2(d1, sigma, T)
    if option == "call":
        return S0 * _Phi(d1) - K * exp(-r * T) * _Phi(d2)
    else:
        return K * exp(-r * T) * _Phi(-d2) - S0 * _Phi(-d1)

def bs_greeks(S0: float, K: float, T: float, r: float, sigma: float, option: OptionType = "call") -> Dict[str, float]:
    """
    Analytical Greeks (Delta, Gamma, Vega, Theta, Rho) for European options.
    Theta is per year; Vega is per 1 volatility point (i.e., dPrice/dSigma).
    """
    if T <= 0 or sigma <= 0:
        # Finite differences would be better, but keep simple here
        return {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}

    d1 = _d1(S0, K, T, r, sigma)
    d2 = _d2(d1, sigma, T)
    pdf_d1 = _phi(d1)
    disc = exp(-r * T)

    gamma = pdf_d1 / (S0 * sigma * sqrt(T))
    vega = S0 * pdf_d1 * sqrt(T)  # per absolute sigma (e.g., 0.01 = 1 vol point)
    if option == "call":
        delta = _Phi(d1)
        theta = -(S0 * pdf_d1 * sigma) / (2 * sqrt(T)) - r * K * disc * _Phi(d2)
        rho = K * T * disc * _Phi(d2)
    else:
        delta = _Phi(d1) - 1.0
        theta = -(S0 * pdf_d1 * sigma) / (2 * sqrt(T)) + r * K * disc * _Phi(-d2)
        rho = -K * T * disc * _Phi(-d2)

    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}
