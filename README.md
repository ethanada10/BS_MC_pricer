# Black–Scholes vs Monte Carlo — Option Pricer in Python

A professional, educational project to price **European options (call/put)** with:

- **Black–Scholes closed-form** (with analytical Greeks)
- **Monte Carlo (GBM)** with **variance reduction** (antithetic variates + moment matching)
- **95% confidence intervals** and **runtime comparison**

This README is written to render **cleanly on GitHub** (no LaTeX required).

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Theory (Plain Text)](#theory-plain-text)
  - [Risk-Neutral Dynamics (GBM)](#risk-neutral-dynamics-gbm)
  - [Black–Scholes (European Call)](#blackscholes-european-call)
  - [Monte Carlo Pricing](#monte-carlo-pricing)
  - [Variance Reduction](#variance-reduction)
- [Convergence Plots](#convergence-plots)
- [Tests](#tests)
- [Repository Layout](#repository-layout)
- [Roadmap / Extensions](#roadmap--extensions)
- [Author](#author)
- [License](#license)

---

## Features

- Black–Scholes analytical pricing (call/put) + Greeks
- Monte Carlo pricer (plain, antithetic, moment-matched)
- Standard error and **95% confidence interval**
- Absolute/relative errors vs Black–Scholes
- **Wall-clock runtime** comparison
- Clean CLI and modular codebase

---

## Quick Start

```bash
# Python 3.10+ recommended
python -m venv .venv
# Windows: .venv\Scriptsctivate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Usage

Compare Black–Scholes and Monte Carlo prices for a European call:

```bash
python scripts/demo_compare.py   --S0 100 --K 100 --T 1 --r 0.02 --sigma 0.2   --n-paths 100000 --n-steps 252 --antithetic
```

**Outputs include:**
- Black–Scholes price (closed form)
- Monte Carlo price (plain & antithetic)
- Absolute and relative errors vs BS
- 95% confidence interval
- Runtime

---

## Theory (Plain Text)

The following formulas are expressed in **plain text/code blocks** so they render cleanly on GitHub.

### Risk-Neutral Dynamics (GBM)

```
dS = r * S * dt + sigma * S * dW
```

Terminal distribution under risk-neutral measure (with Z ~ N(0,1)):

```
S(T) = S0 * exp( (r - 0.5 * sigma^2) * T + sigma * sqrt(T) * Z )
```

### Black–Scholes (European Call)

```
C = S0 * Phi(d1) - K * exp(-r * T) * Phi(d2)

d1 = [ ln(S0/K) + (r + 0.5 * sigma^2) * T ] / ( sigma * sqrt(T) )
d2 = d1 - sigma * sqrt(T)
```

Where `Phi` is the CDF of the standard normal distribution.

### Monte Carlo Pricing

1. Simulate `N` terminal prices `S(T)` using the GBM formula above (or simulate full paths).
2. Compute the payoff:
   - Call: `max(S(T) - K, 0)`
   - Put : `max(K - S(T), 0)`
3. Discount the mean payoff:
   ```
   MC price = exp(-r * T) * average(payoff)
   ```
4. Estimate standard deviation, standard error, and a **95% confidence interval** for the MC estimator.

### Variance Reduction

- **Antithetic variates**: for each normal `Z`, also use `-Z`.
- **Moment matching**: shift/scale the sampled normals so sample mean ≈ 0 and sample std ≈ 1.

---

## Convergence Plots

Generate convergence figures and a CSV:

```bash
# from the project root
export PYTHONPATH="$PWD/src"
python scripts/plot_convergence.py   --S0 100 --K 100 --T 1 --r 0.02 --sigma 0.2 --antithetic
```

Outputs:
- `plots/price_convergence.png`
- `plots/stderr_convergence.png`

Each plot shows how the MC estimate and its standard error converge as the number of paths increases.

---

## Tests

```bash
pytest -q
```

- Validates that MC (large N) ≈ Black–Scholes within tolerance.

---

## Repository Layout

```
bs_mc_pricer/
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── src/
│   └── bs_pricer/
│       ├── __init__.py
│       ├── black_scholes.py
│       ├── monte_carlo.py
│       └── utils.py
├── scripts/
│   └── demo_compare.py
└── tests/
    └── test_black_scholes.py
```

---

## Roadmap / Extensions

- Monte Carlo Greeks (Likelihood Ratio, Pathwise)
- Exotic options (barriers, lookbacks)
- FastAPI microservice for pricing endpoints
- Dashboard (Dash/Plotly or Streamlit) with live controls

---

## Author

**Ethan Ada** — Quant Analyst 
GitHub: https://github.com/ethanada10

---

## License

This project is distributed under the terms of the **MIT License** (or update to your preferred license).
