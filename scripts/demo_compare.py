#!/usr/bin/env python
"""
CLI demo to compare Black–Scholes (closed form) vs Monte Carlo.
"""
import argparse
from tabulate import tabulate
from bs_pricer.black_scholes import bs_price, bs_greeks
from bs_pricer.monte_carlo import mc_price

def parse_args():
    p = argparse.ArgumentParser(description="Compare Black–Scholes vs Monte Carlo for European options.")
    p.add_argument("--S0", type=float, required=True)
    p.add_argument("--K", type=float, required=True)
    p.add_argument("--T", type=float, required=True, help="Maturity in years")
    p.add_argument("--r", type=float, required=True, help="Risk-free rate (cc)")
    p.add_argument("--sigma", type=float, required=True, help="Vol (annualized)")
    p.add_argument("--option", choices=["call", "put"], default="call")
    p.add_argument("--n-paths", type=int, default=100000)
    p.add_argument("--n-steps", type=int, default=1)
    p.add_argument("--antithetic", action="store_true")
    p.add_argument("--no-moment-matching", action="store_true", help="Disable moment matching.")
    return p.parse_args()

def main():
    args = parse_args()

    bs = bs_price(args.S0, args.K, args.T, args.r, args.sigma, args.option)
    greeks = bs_greeks(args.S0, args.K, args.T, args.r, args.sigma, args.option)

    mc_plain = mc_price(
        args.S0, args.K, args.T, args.r, args.sigma,
        option=args.option,
        n_paths=args.n_paths,
        n_steps=args.n_steps,
        antithetic=False,
        moment_matching=not args.no_moment_matching,
        seed=42,
    )

    mc_anti = None
    if args.antithetic:
        mc_anti = mc_price(
            args.S0, args.K, args.T, args.r, args.sigma,
            option=args.option,
            n_paths=args.n_paths,
            n_steps=args.n_steps,
            antithetic=True,
            moment_matching=not args.no_moment_matching,
            seed=42,
        )

    rows = []
    rows.append(["Black–Scholes", f"{bs:.6f}", "—", "—", "—"])
    rows.append([
        "MC (plain)",
        f"{mc_plain.price:.6f}",
        f"{abs(mc_plain.price - bs):.6f}",
        f"{abs(mc_plain.price - bs)/bs*100:.4f}%",
        f"[{mc_plain.ci95[0]:.6f}, {mc_plain.ci95[1]:.6f}]"
    ])
    if mc_anti:
        rows.append([
            "MC (antithetic)",
            f"{mc_anti.price:.6f}",
            f"{abs(mc_anti.price - bs):.6f}",
            f"{abs(mc_anti.price - bs)/bs*100:.4f}%",
            f"[{mc_anti.ci95[0]:.6f}, {mc_anti.ci95[1]:.6f}]"
        ])

    print("\n=== Prices ===")
    print(tabulate(rows, headers=["Method", "Price", "Abs Error vs BS", "Rel Error", "95% CI"], tablefmt="github"))

    print("\n=== Greeks (analytical) ===")
    grec_rows = [[k, f"{v:.6f}"] for k, v in greeks.items()]
    print(tabulate(grec_rows, headers=["Greek", "Value"], tablefmt="github"))

    print("\n=== Runtimes (seconds) ===")
    rt_rows = [["MC (plain)", f"{mc_plain.elapsed_sec:.4f}"]]
    if mc_anti:
        rt_rows.append(["MC (antithetic)", f"{mc_anti.elapsed_sec:.4f}"])
    print(tabulate(rt_rows, headers=["Method", "Seconds"], tablefmt="github"))

if __name__ == "__main__":
    main()