"""
portfolio_logic.py
------------------
Core logic for the CodeAlpha Stock Portfolio Tracker.

No input()/print() lives here, so the same code powers both the console
version (portfolio_console.py) and the 3D window version (portfolio_gui.py).

Concepts used: dictionary, basic arithmetic, input validation, file handling
(.txt and .csv).
"""

import csv
from datetime import datetime

# Task requirement: a hardcoded dictionary of stock prices (in US dollars).
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 135,
    "MSFT": 330,
    "AMZN": 145,
    "NVDA": 450,
}

MAX_QUANTITY = 1_000_000


def money(value):
    """Format a number as dollars, e.g. 1234.5 -> '$1,234.50'."""
    return f"${value:,.2f}"


class Portfolio:
    """Stores the user's holdings and works out the total investment."""

    def __init__(self, prices=None):
        self.prices = dict(prices or STOCK_PRICES)
        self.holdings = {}          # symbol -> quantity

    # ---------------------------------------------------------- editing
    def add(self, symbol, quantity):
        """Add shares. Raises ValueError with a friendly message if invalid."""
        symbol = str(symbol).strip().upper()
        if symbol not in self.prices:
            available = ", ".join(self.prices)
            raise ValueError(f"'{symbol}' is not available. Choose from: {available}")

        try:
            quantity = int(str(quantity).strip())
        except ValueError:
            raise ValueError("Quantity must be a whole number (e.g. 10).") from None

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if quantity > MAX_QUANTITY:
            raise ValueError(f"Quantity cannot be more than {MAX_QUANTITY:,}.")

        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        return symbol, quantity

    def remove(self, symbol):
        self.holdings.pop(symbol, None)

    def clear(self):
        self.holdings.clear()

    # ----------------------------------------------------------- results
    def rows(self):
        """List of (symbol, quantity, price, value) for every holding."""
        return [(s, q, self.prices[s], q * self.prices[s])
                for s, q in self.holdings.items()]

    def total_investment(self):
        return sum(value for _, _, _, value in self.rows())

    def total_shares(self):
        return sum(self.holdings.values())

    def is_empty(self):
        return not self.holdings

    # ------------------------------------------------------ file handling
    def to_text(self):
        """A neat text report of the portfolio."""
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            "STOCK PORTFOLIO REPORT",
            f"Generated: {stamp}",
            "=" * 52,
            f"{'Stock':<8}{'Qty':>8}{'Price':>14}{'Value':>20}",
            "-" * 52,
        ]
        for symbol, qty, price, value in self.rows():
            lines.append(f"{symbol:<8}{qty:>8,}{money(price):>14}{money(value):>20}")
        lines += [
            "-" * 52,
            f"{'TOTAL INVESTMENT':<30}{money(self.total_investment()):>22}",
            "",
        ]
        return "\n".join(lines)

    def save_txt(self, path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.to_text())
        return path

    def save_csv(self, path):
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Stock", "Quantity", "Price", "Value"])
            for symbol, qty, price, value in self.rows():
                writer.writerow([symbol, qty, f"{price:.2f}", f"{value:.2f}"])
            writer.writerow([])
            writer.writerow(["TOTAL INVESTMENT", "", "", f"{self.total_investment():.2f}"])
        return path
