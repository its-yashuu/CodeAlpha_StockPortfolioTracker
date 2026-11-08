# CodeAlpha_StockPortfolioTracker

**CodeAlpha Python Programming Internship — Task 2: Stock Portfolio Tracker**

Build a portfolio by entering stock symbols and quantities. The program looks up each price in a
hardcoded dictionary, calculates the total investment, and can save the result as `.txt` or `.csv`.

| File | What it is |
|------|------------|
| `portfolio_console.py` | Text-based version (the original task scope) |
| `portfolio_gui.py` | Professional **3D-style window** version that opens on its own screen |
| `portfolio_logic.py` | Shared logic: price dictionary, validation, totals, file saving |

## Features

- Hardcoded price dictionary: `AAPL`, `TSLA`, `GOOGL`, `MSFT`, `AMZN`, `NVDA`
- User enters stock name and quantity
- Total investment calculated automatically
- Adding the same stock twice combines the quantities
- Input validation: unknown stock, non-numeric, zero or negative quantity
- Optional save to `portfolio.txt` or `portfolio.csv`
- 3D window version: clickable price tiles, glossy buttons, live holdings table, big total display, remove buttons

## How to run

Requires **Python 3.8+**. No external libraries — `tkinter` ships with Python.

```bash
# 3D window version
python portfolio_gui.py

# Console version
python portfolio_console.py
```

On Mac/Linux use `python3` instead of `python`.
**Linux:** if you get `No module named tkinter`, run `sudo apt install python3-tk`.

## Example (console)

```
Stock symbol: AAPL
Quantity:     10
>> Added 10 x AAPL

Stock symbol: TSLA
Quantity:     5
>> Added 5 x TSLA

Stock symbol: done

TOTAL INVESTMENT                    $3,050.00
```

## Concepts used

dictionary, input/output, basic arithmetic, file handling (`.txt`, `.csv`), exceptions, classes, `tkinter`.

## Project structure

```
CodeAlpha_StockPortfolioTracker/
├── portfolio_logic.py
├── portfolio_console.py
├── portfolio_gui.py
└── README.md
```

## Author

Yashaswini S — CodeAlpha Python Programming Intern
