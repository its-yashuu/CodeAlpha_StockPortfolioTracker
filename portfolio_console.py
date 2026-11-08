"""
portfolio_console.py
--------------------
CodeAlpha Python Internship - Task 2: Stock Portfolio Tracker (console version).

Run:  python portfolio_console.py
"""

import os

from portfolio_logic import Portfolio, money

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def show_prices(portfolio):
    print("\nAvailable stocks")
    print("-" * 24)
    for symbol, price in portfolio.prices.items():
        print(f"  {symbol:<8}{money(price):>12}")
    print()


def show_portfolio(portfolio):
    print("\n" + "=" * 52)
    print("            YOUR STOCK PORTFOLIO")
    print("=" * 52)
    if portfolio.is_empty():
        print("  (no stocks added)")
    else:
        print(f"{'Stock':<8}{'Qty':>8}{'Price':>14}{'Value':>20}")
        print("-" * 52)
        for symbol, qty, price, value in portfolio.rows():
            print(f"{symbol:<8}{qty:>8,}{money(price):>14}{money(value):>20}")
    print("-" * 52)
    print(f"{'TOTAL INVESTMENT':<30}{money(portfolio.total_investment()):>22}")
    print("=" * 52)


def collect_stocks(portfolio):
    print("Type a stock symbol and a quantity.")
    print("Commands:  'list' = show prices   'done' = finish\n")

    while True:
        symbol = input("Stock symbol: ").strip()
        if symbol.lower() == "done":
            break
        if symbol.lower() == "list":
            show_prices(portfolio)
            continue
        if not symbol:
            continue

        quantity = input("Quantity:     ").strip()
        try:
            name, qty = portfolio.add(symbol, quantity)
            print(f">> Added {qty:,} x {name}\n")
        except ValueError as error:
            print(f">> {error}\n")


def offer_to_save(portfolio):
    if portfolio.is_empty():
        return
    choice = input("\nSave results? (txt / csv / both / no): ").strip().lower()
    if choice in ("txt", "both"):
        path = portfolio.save_txt(os.path.join(BASE_DIR, "portfolio.txt"))
        print(f">> Saved {path}")
    if choice in ("csv", "both"):
        path = portfolio.save_csv(os.path.join(BASE_DIR, "portfolio.csv"))
        print(f">> Saved {path}")


def main():
    print("=" * 52)
    print("        STOCK PORTFOLIO TRACKER")
    print("=" * 52)

    portfolio = Portfolio()
    show_prices(portfolio)
    collect_stocks(portfolio)
    show_portfolio(portfolio)
    offer_to_save(portfolio)
    print("\nThanks for using the tracker. Goodbye!")


if __name__ == "__main__":
    main()
