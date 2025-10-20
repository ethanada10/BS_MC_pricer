import math
from bs_pricer.black_scholes import bs_price
from bs_pricer.monte_carlo import mc_price

def test_mc_converges_to_bs():
    S0, K, T, r, sigma = 100.0, 100.0, 1.0, 0.02, 0.2
    bs = bs_price(S0,K,T,r,sigma,"call")
    mc = mc_price(S0,K,T,r,sigma,"call", n_paths=400_000, n_steps=1, antithetic=True, seed=123)
    # Within 3 standard errors is very likely
    assert abs(mc.price - bs) <= 3.0 * mc.stderr
