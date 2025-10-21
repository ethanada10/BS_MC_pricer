🧮 Black–Scholes vs Monte Carlo — Complete Option Pricer (Python)
A complete educational project to price European options (call/put) using:
🔹 Closed-form Black–Scholes model (with analytical Greeks)
🔹 Monte Carlo (GBM) simulation with variance reduction techniques
🔹 95% confidence intervals and runtime comparison
Perfect for GitHub portfolio projects or quantitative finance learning.
⚙️ Features
Black–Scholes analytical formula
Monte Carlo pricer (plain, antithetic, and moment-matched)
Computation of mean, standard deviation, and confidence interval
Comparison metrics (absolute & relative errors vs BS)
Execution time benchmarking
Full CLI + modular code structure
📦 Installation
# Python 3.10+ recommended
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
🚀 Usage
Compare Black–Scholes and Monte Carlo prices for a European call:
python scripts/demo_compare.py \
  --S0 100 --K 100 --T 1 --r 0.02 --sigma 0.2 \
  --n-paths 100000 --n-steps 252 --antithetic
The script outputs:
💰 Black–Scholes closed-form price
💰 Monte Carlo price (plain & antithetic)
📉 Absolute and relative errors
📊 95% confidence interval
⏱️ Runtime comparison
🧠 Theoretical background
1. Risk-neutral dynamics (Geometric Brownian Motion)
The underlying price S(t) follows:
dS = r·S·dt + σ·S·dW
At maturity T:
S(T) = S₀ × exp[(r − 0.5σ²)T + σ√T·Z], where Z ~ N(0, 1)
2. Black–Scholes closed-form formula
European Call Option:
C = S₀·Φ(d₁) − K·e^(−rT)·Φ(d₂)
where:
d₁ = [ln(S₀/K) + (r + 0.5σ²)T] / (σ√T)
d₂ = d₁ − σ√T
Φ(x): Cumulative distribution function (CDF) of the standard normal.
3. Monte Carlo pricing
1️⃣ Simulate N terminal prices S(T) under GBM.
2️⃣ Compute the payoff:
Call: max(S_T − K, 0)
Put: max(K − S_T, 0)
3️⃣ Discount the mean payoff:
MC price = e^(−rT) × average(payoff)
4️⃣ Estimate standard deviation, standard error, and 95% confidence interval.
4. Variance reduction
Antithetic variates: use both Z and −Z to reduce sampling noise.
Moment matching: rescale Z so that mean ≈ 0 and std ≈ 1.
🧪 Testing
Run unit tests:
pytest -q
✔️ Ensures that the Monte Carlo estimate (for large N) converges to the Black–Scholes price within tolerance.
🗂️ Repository structure
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
📈 Convergence plots
Generate convergence data and plots:
export PYTHONPATH="$PWD/src"
python scripts/plot_convergence.py \
  --S0 100 --K 100 --T 1 --r 0.02 --sigma 0.2 --antithetic
Outputs:
plots/price_convergence.png
plots/stderr_convergence.png
Each plot shows how Monte Carlo price and standard error converge to the theoretical Black–Scholes value as the number of paths increases.
📊 Example comparison
Method	Price	Std. Err.	95% CI width	Runtime (s)
Black–Scholes (exact)	10.45	–	–	< 0.001
Monte Carlo (plain)	10.48	0.04	±0.08	0.52
Monte Carlo (antithetic)	10.46	0.03	±0.06	0.53
📌 Push to GitHub
git init
git add .
git commit -m "feat: BS vs Monte Carlo pricer with variance reduction"
git branch -M main
git remote add origin <YOUR_REPO_URL>
git push -u origin main
💡 Optional extensions
Want to go further?
⚙️ Monte Carlo Greeks (Likelihood Ratio / Pathwise)
💣 Barrier and Lookback options
🌐 FastAPI microservice with pricing endpoints
📊 Dash or Streamlit app for visualization
👨‍💻 Author
Ethan Ada
MSc Data Science & AI — Quantitative Finance Enthusiast
📈 GitHub: @ethanada10
