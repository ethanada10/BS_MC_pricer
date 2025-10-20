#!/usr/bin/env python
"""
Plot Monte Carlo convergence towards Black–Scholes for a European option.
Generates:
- plots/price_convergence.png  (MC estimates vs N, with BS as horizontal line)
- plots/stderr_convergence.png (standard error vs N, log-log)
- plots/convergence_results.csv (raw data)
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import csv
from bs_pricer.black_scholes import bs_price
from bs_pricer.monte_carlo import mc_price

def parse_args():
    p = argparse.ArgumentParser(description="Plot MC convergence to BS.")
    p.add_argument("--S0", type=float, default=100.0)
    p.add_argument("--K", type=float, default=100.0)
    p.add_argument("--T", type=float, default=1.0)
    p.add_argument("--r", type=float, default=0.02)
    p.add_argument("--sigma", type=float, default=0.2)
    p.add_argument("--option", choices=["call","put"], default="call")
    p.add_argument("--n-steps", type=int, default=1)
    p.add_argument("--min-exp", type=int, default=3, help="min exponent for N=10^exp")
    p.add_argument("--max-exp", type=int, default=6, help="max exponent for N=10^exp")
    p.add_argument("--antithetic", action="store_true", help="also compute antithetic")
    p.add_argument("--no-moment-matching", action="store_true", help="Disable moment matching.")
    p.add_argument("--outdir", type=str, default="plots")
    return p.parse_args()

def main():
    args = parse_args()
    bs = bs_price(args.S0, args.K, args.T, args.r, args.sigma, args.option)

    Ns = [int(10**e) for e in range(args.min_exp, args.max_exp + 1)]
    rows_plain = []
    rows_anti = []

    for N in Ns:
        res_plain = mc_price(args.S0, args.K, args.T, args.r, args.sigma,
                             option=args.option, n_paths=N, n_steps=args.n_steps,
                             antithetic=False, moment_matching=not args.no_moment_matching, seed=123)
        rows_plain.append((N, res_plain.price, res_plain.stderr))

        if args.antithetic:
            res_anti = mc_price(args.S0, args.K, args.T, args.r, args.sigma,
                                option=args.option, n_paths=N, n_steps=args.n_steps,
                                antithetic=True, moment_matching=not args.no_moment_matching, seed=123)
            rows_anti.append((N, res_anti.price, res_anti.stderr))

    # Save CSV
    out_csv = f"{args.outdir}/convergence_results.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        header = ["N", "mc_price_plain", "stderr_plain"]
        if args.antithetic:
            header += ["mc_price_antithetic", "stderr_antithetic"]
        w.writerow(header)
        for i, (N, p, se) in enumerate(rows_plain):
            row = [N, p, se]
            if args.antithetic:
                Na, pa, sea = rows_anti[i]
                row += [pa, sea]
            w.writerow(row)

    # Price convergence plot
    plt.figure()
    plt.axhline(y=bs)  # BS reference
    plt.xscale("log")
    xs = [N for (N, _, _) in rows_plain]
    ys = [p for (_, p, _) in rows_plain]
    plt.plot(xs, ys, marker="o", label="MC (plain)")
    if args.antithetic:
        xs2 = [N for (N, _, _) in rows_anti]
        ys2 = [p for (_, p, _) in rows_anti]
        plt.plot(xs2, ys2, marker="s", label="MC (antithetic)")
    plt.xlabel("Number of paths N (log scale)")
    plt.ylabel("Price")
    plt.title("Monte Carlo convergence to Black–Scholes price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{args.outdir}/price_convergence.png", dpi=160)

    # Standard error convergence plot (log-log)
    plt.figure()
    plt.xscale("log")
    plt.yscale("log")
    xs = [N for (N, _, _) in rows_plain]
    ys = [se for (_, _, se) in rows_plain]
    plt.plot(xs, ys, marker="o", label="MC stderr (plain)")
    if args.antithetic:
        xs2 = [N for (N, _, _) in rows_anti]
        ys2 = [se for (_, _, se) in rows_anti]
        plt.plot(xs2, ys2, marker="s", label="MC stderr (antithetic)")
    plt.xlabel("Number of paths N (log scale)")
    plt.ylabel("Standard error (log scale)")
    plt.title("MC standard error vs N (should ~ N^-0.5)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{args.outdir}/stderr_convergence.png", dpi=160)

    print(f"Saved:\n - {args.outdir}/price_convergence.png\n - {args.outdir}/stderr_convergence.png\n - {out_csv}")

if __name__ == "__main__":
    main()
