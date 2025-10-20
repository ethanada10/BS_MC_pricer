# 🧮 Black–Scholes vs Monte Carlo — Complete Option Pricer (Python)

A **ready-to-push** educational project to price **European options (call/put)** with:
- **Closed-form Black–Scholes** (+ analytical Greeks)
- **Monte Carlo** (GBM) with **variance reduction** (antithetic variates + moment matching)
- **95% confidence intervals** and **runtime comparison**

Perfect to push on **GitHub** and to **highlight the difference** between BS and MC.

---

## 📦 Quick setup

```bash
# Python 3.10+ recommended
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

## 🚀 Quick usage (scripts)

Compare BS vs MC on a European call (parameters via CLI):
```bash
python scripts/demo_compare.py --S0 100 --K 100 --T 1 --r 0.02 --sigma 0.2     --n-paths 100000 --n-steps 252 --antithetic
```

This prints:
- BS price (closed form)
- MC price (plain and antithetic if requested)
- Absolute/relative errors vs BS
- 95% confidence interval for MC
- Wall-clock runtime

## 🧠 Short theory

Risk‑neutral GBM for the underlying:
\[ dS_t = r S_t\,dt + \sigma S_t\,dW_t,\quad S_T = S_0\exp\!\left((r-\tfrac{1}{2}\sigma^2)T + \sigma\sqrt{T}Z\right). \]

Black–Scholes (European call):
\[ C = S_0\,\Phi(d_1) - K e^{-rT}\,\Phi(d_2), \]
with
\[ d_1 = \frac{\ln(S_0/K) + (r + \tfrac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}. \]

Monte Carlo idea:
1) Simulate \(N\) GBM paths (or directly \(S_T\)).  
2) Compute payoff \(\max(S_T-K,0)\) (call) or \(\max(K-S_T,0)\) (put).  
3) Discount: \( \hat{C} = e^{-rT}\, \frac{1}{N}\sum_i \text{payoff}_i \).  
4) Estimate std, standard error, and a 95% CI.

**Variance reduction**: antithetic variates (use \(Z\) and \(-Z\)) and **moment matching** (center/scale the \(Z\) to sample mean≈0, std≈1).

## 🧪 Tests

```bash
pytest -q
```
- Asserts that MC (large N) ≈ BS within a tolerance.

## 🗂️ Repository layout

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

## 📌 Push to GitHub

```bash
git init
git add .
git commit -m "feat: BS vs Monte Carlo pricer (antithetic + moment matching)"
git branch -M main
git remote add origin <YOUR_REPO_URL>
git push -u origin main
```

---

👉 Want extras (MC Greeks via LR/Pathwise, exotics like barriers/lookbacks, or a FastAPI microservice)? Ask away!


## 📈 Convergence plots

Generate convergence figures and a CSV:
```bash
# from the project root
export PYTHONPATH="$PWD/src"
python scripts/plot_convergence.py --S0 100 --K 100 --T 1 --r 0.02 --sigma 0.2 --antithetic
```
Outputs:
- `plots/price_convergence.png`
- `plots/stderr_convergence.png`
- `plots/convergence_results.csv`
