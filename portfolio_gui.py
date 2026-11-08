"""
portfolio_gui.py
----------------
CodeAlpha Python Internship - Task 2: Stock Portfolio Tracker (3D-style window).

Opens in its own window and uses only Python's built-in tkinter - nothing to
install. The 3D look comes from gradients, drop shadows, bevelled buttons and
extruded text drawn on a Canvas.

Run:  python portfolio_gui.py

How to use:
    1. Click a stock tile (price list on the left)
    2. Type a quantity and press Enter or click ADD TO PORTFOLIO
    3. Watch the total investment update
    4. Save the result as .txt or .csv (saved next to this script)
"""

import os
import tkinter as tk

from portfolio_logic import Portfolio, money

# --------------------------------------------------------------------- layout
W, H = 1040, 660
LEFT_CARD = (30, 100, 430, 630)
RIGHT_CARD = (455, 100, 1010, 630)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------------- palette
BG_TOP, BG_BOTTOM = "#1d2b5e", "#080a1c"
CARD_TOP, CARD_BOTTOM = "#2b3270", "#141838"
GOLD = "#ffd166"
MUTED = "#9aa4d6"
GOOD = "#5dff9d"
BAD = "#ff6b7a"
SHADOW = "#05061a"
FONT = "Helvetica"


# ------------------------------------------------------------- colour helpers
def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in rgb)


def lerp(c1, c2, t):
    a, b = hex_to_rgb(c1), hex_to_rgb(c2)
    return rgb_to_hex([a[i] + (b[i] - a[i]) * t for i in range(3)])


def shade(color, amount):
    """amount > 0 lightens, amount < 0 darkens (range -1 .. 1)."""
    return lerp(color, "#ffffff", amount) if amount >= 0 else lerp(color, "#000000", -amount)


# ------------------------------------------------------------------ the app
class PortfolioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CodeAlpha  |  3D Stock Portfolio Tracker")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=W, height=H,
                                highlightthickness=0, bg=BG_BOTTOM)
        self.canvas.pack()

        self.portfolio = Portfolio()
        self.selected = next(iter(self.portfolio.prices))
        self.message = "Pick a stock, enter a quantity, then add it."
        self.message_color = MUTED

        # clickable areas (rebuilt on every render)
        self.chip_boxes = {}
        self.remove_boxes = {}
        self.add_box = (70, 522, 390, 566)
        self.txt_box = (480, 574, 640, 614)
        self.csv_box = (655, 574, 815, 614)
        self.clear_box = (830, 574, 990, 614)

        self.draw_static()
        self.make_entry()
        self.render()

        self.bind("<Escape>", lambda e: self.destroy())
        self.canvas.bind("<Button-1>", self.on_click)
        self.center_window()
        self.qty_entry.focus_set()

    # ---------------------------------------------------------------- window
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - W) // 2
        y = (self.winfo_screenheight() - H) // 2
        self.geometry(f"{W}x{H}+{max(x, 0)}+{max(y, 0)}")

    def make_entry(self):
        """A real text box (tk.Entry) framed with a 3D 'pressed in' border."""
        c = self.canvas
        c.create_rectangle(128, 464, 332, 506, fill="#080a22", outline="", tags="static")
        c.create_line(128, 506, 332, 506, fill="#6a77d0", tags="static")
        self.qty_entry = tk.Entry(self, font=(FONT, 16, "bold"), justify="center",
                                  bd=0, relief="flat", bg="#f4f6ff", fg="#1d2250",
                                  insertbackground="#1d2250")
        c.create_window(230, 485, window=self.qty_entry, width=196, height=34,
                        tags="static")
        self.qty_entry.bind("<Return>", self.add_holding)

    # ------------------------------------------------------- drawing helpers
    def vgradient(self, x0, y0, x1, y1, top, bottom, tag):
        height = max(int(y1 - y0), 1)
        for i in range(height):
            self.canvas.create_rectangle(x0, y0 + i, x1, y0 + i + 1,
                                         fill=lerp(top, bottom, i / height),
                                         outline="", tags=tag)

    def text3d(self, x, y, text, size, color, depth, tag, anchor="center"):
        font = (FONT, size, "bold")
        for i in range(depth, 0, -1):
            self.canvas.create_text(x + i, y + i, text=text, font=font,
                                    fill=lerp(shade(color, -0.75),
                                              shade(color, -0.45), i / depth),
                                    anchor=anchor, tags=tag)
        self.canvas.create_text(x, y, text=text, font=font, fill=color,
                                anchor=anchor, tags=tag)

    def card(self, box):
        x0, y0, x1, y1 = box
        self.canvas.create_rectangle(x0 + 8, y0 + 12, x1 + 8, y1 + 12,
                                     fill="#04051a", outline="", tags="static")
        self.vgradient(x0, y0, x1, y1, CARD_TOP, CARD_BOTTOM, "static")
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#4756b8",
                                     width=2, tags="static")

    def button3d(self, box, label, top, bottom, edge, text_color="#ffffff",
                 size=13, depth=6):
        x0, y0, x1, y1 = box
        c = self.canvas
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        c.create_rectangle(x0 + 3, y0 + depth + 4, x1 + 3, y1 + depth + 4,
                           fill=SHADOW, outline="", tags="dynamic")
        c.create_rectangle(x0, y0 + depth, x1, y1 + depth, fill=edge,
                           outline="", tags="dynamic")
        self.vgradient(x0, y0, x1, y1, top, bottom, "dynamic")
        c.create_line(x0, y0, x1, y0, fill=shade(top, 0.55), tags="dynamic")
        c.create_text(cx + 1, cy + 2, text=label, font=(FONT, size, "bold"),
                      fill=shade(edge, -0.2), tags="dynamic")
        c.create_text(cx, cy, text=label, font=(FONT, size, "bold"),
                      fill=text_color, tags="dynamic")

    # ------------------------------------------------------ static scenery
    def draw_static(self):
        c = self.canvas
        self.vgradient(0, 0, W, H, BG_TOP, BG_BOTTOM, "static")
        self.text3d(W / 2, 46, "STOCK PORTFOLIO TRACKER", 30, GOLD, 7, "static")
        c.create_text(W / 2, 82,
                      text="Pick a stock  >  enter quantity  >  see your total investment",
                      font=(FONT, 11), fill=MUTED, tags="static")
        self.card(LEFT_CARD)
        self.card(RIGHT_CARD)

        c.create_text(230, 126, text="MARKET PRICES", font=(FONT, 12, "bold"),
                      fill=MUTED, tags="static")
        c.create_text(230, 452, text="QUANTITY", font=(FONT, 10, "bold"),
                      fill=MUTED, tags="static")
        c.create_text(732, 126, text="YOUR HOLDINGS", font=(FONT, 12, "bold"),
                      fill=MUTED, tags="static")

        # column headings
        for x, label, anchor in ((490, "STOCK", "w"), (620, "QTY", "e"),
                                 (720, "PRICE", "e"), (900, "VALUE", "e")):
            c.create_text(x, 158, text=label, font=(FONT, 9, "bold"),
                          fill="#7580c4", anchor=anchor, tags="static")

        c.create_text(W / 2, 646, text="CodeAlpha Python Internship  -  Task 2      |      Esc = quit",
                      font=(FONT, 9), fill="#6e78b8", tags="static")

    # ---------------------------------------------------- dynamic drawing
    def render(self):
        self.canvas.delete("dynamic")
        self.draw_chips()
        self.draw_add_panel()
        self.draw_holdings()
        self.draw_total()
        self.draw_buttons()

    def draw_chips(self):
        c = self.canvas
        self.chip_boxes = {}
        w, h, depth = 165, 62, 6
        for i, (symbol, price) in enumerate(self.portfolio.prices.items()):
            col, row = i % 2, i // 2
            x0 = 55 + col * 190
            y0 = 152 + row * 86
            chosen = symbol == self.selected
            top, bottom, edge = (("#ffe29a", "#f2a72c", "#a86a0c") if chosen
                                 else ("#5b6bd6", "#34409a", "#1a2160"))
            txt, sub = (("#3a2400", "#6b4300") if chosen else ("#ffffff", "#c9d0ff"))
            lift = 4 if chosen else 0           # selected tile looks pressed in

            c.create_rectangle(x0 + 4, y0 + depth + 6, x0 + w + 4, y0 + h + depth + 6,
                               fill=SHADOW, outline="", tags="dynamic")
            c.create_rectangle(x0, y0 + depth, x0 + w, y0 + h + depth - lift,
                               fill=edge, outline="", tags="dynamic")
            self.vgradient(x0, y0 + lift, x0 + w, y0 + h, top, bottom, "dynamic")
            c.create_line(x0, y0 + lift, x0 + w, y0 + lift, fill=shade(top, 0.55),
                          tags="dynamic")
            c.create_text(x0 + w / 2, y0 + lift + 22, text=symbol,
                          font=(FONT, 16, "bold"), fill=txt, tags="dynamic")
            c.create_text(x0 + w / 2, y0 + lift + 44, text=money(price),
                          font=(FONT, 11), fill=sub, tags="dynamic")
            self.chip_boxes[symbol] = (x0, y0, x0 + w, y0 + h + depth)

    def draw_add_panel(self):
        c = self.canvas
        c.create_text(230, 428, text=f"Selected:  {self.selected}",
                      font=(FONT, 13, "bold"), fill=GOLD, tags="dynamic")
        self.button3d(self.add_box, "ADD TO PORTFOLIO", "#5be39a", "#1f9e58",
                      "#10633a", size=13)
        c.create_text(230, 596, text=self.message, font=(FONT, 10, "bold"),
                      fill=self.message_color, width=350, tags="dynamic")

    def draw_holdings(self):
        c = self.canvas
        self.remove_boxes = {}
        rows = self.portfolio.rows()

        if not rows:
            c.create_text(732, 300, text="No stocks added yet", font=(FONT, 16, "bold"),
                          fill="#5f6ab0", tags="dynamic")
            c.create_text(732, 330, text="Choose a stock tile on the left to begin",
                          font=(FONT, 11), fill="#5f6ab0", tags="dynamic")
            return

        for i, (symbol, qty, price, value) in enumerate(rows):
            y0 = 174 + i * 50
            y1 = y0 + 40
            c.create_rectangle(480 + 3, y0 + 8, 990 + 3, y1 + 8, fill=SHADOW,
                               outline="", tags="dynamic")
            c.create_rectangle(480, y0 + 5, 990, y1 + 5, fill="#171d52",
                               outline="", tags="dynamic")
            self.vgradient(480, y0, 990, y1, "#44519f", "#2c377f", "dynamic")
            c.create_line(480, y0, 990, y0, fill="#7d8be0", tags="dynamic")
            c.create_rectangle(480, y0, 486, y1, fill=GOLD, outline="", tags="dynamic")

            mid = (y0 + y1) / 2
            c.create_text(498, mid, text=symbol, anchor="w",
                          font=(FONT, 14, "bold"), fill="#ffffff", tags="dynamic")
            c.create_text(620, mid, text=f"{qty:,}", anchor="e",
                          font=(FONT, 13), fill="#e4e8ff", tags="dynamic")
            c.create_text(720, mid, text=money(price), anchor="e",
                          font=(FONT, 13), fill="#c9d0ff", tags="dynamic")
            c.create_text(900, mid, text=money(value), anchor="e",
                          font=(FONT, 13, "bold"), fill=GOLD, tags="dynamic")

            # little 3D remove button
            bx0, by0, bx1, by1 = 954, y0 + 6, 980, y0 + 32
            c.create_rectangle(bx0, by0 + 4, bx1, by1 + 4, fill="#7a1620",
                               outline="", tags="dynamic")
            self.vgradient(bx0, by0, bx1, by1, "#ff8a96", "#c2323f", "dynamic")
            c.create_text((bx0 + bx1) / 2, (by0 + by1) / 2, text="x",
                          font=(FONT, 13, "bold"), fill="#ffffff", tags="dynamic")
            self.remove_boxes[symbol] = (bx0, by0, bx1, by1 + 4)

    def draw_total(self):
        c = self.canvas
        x0, y0, x1, y1 = 480, 484, 990, 556
        c.create_rectangle(x0 + 5, y0 + 10, x1 + 5, y1 + 10, fill=SHADOW,
                           outline="", tags="dynamic")
        c.create_rectangle(x0, y0 + 6, x1, y1 + 6, fill="#0b3a25",
                           outline="", tags="dynamic")
        self.vgradient(x0, y0, x1, y1, "#27895a", "#145236", "dynamic")
        c.create_line(x0, y0, x1, y0, fill="#6be0a3", tags="dynamic")

        c.create_text(500, y0 + 24, text="TOTAL INVESTMENT", anchor="w",
                      font=(FONT, 12, "bold"), fill="#b8f5d4", tags="dynamic")
        shares = self.portfolio.total_shares()
        kinds = len(self.portfolio.holdings)
        c.create_text(500, y0 + 48,
                      text=f"{kinds} stock{'s' if kinds != 1 else ''}  |  {shares:,} shares",
                      anchor="w", font=(FONT, 10), fill="#8fdcb4", tags="dynamic")
        self.text3d(970, y0 + 36, money(self.portfolio.total_investment()),
                    26, GOOD, 4, "dynamic", anchor="e")

    def draw_buttons(self):
        self.button3d(self.txt_box, "SAVE .TXT", "#6bb5ff", "#2f6fd6", "#1a3f8f", size=12)
        self.button3d(self.csv_box, "SAVE .CSV", "#ffbe5c", "#f07f1d", "#a8520b", size=12)
        self.button3d(self.clear_box, "CLEAR ALL", "#ff8a96", "#c2323f", "#7a1620", size=12)

    # ---------------------------------------------------------------- actions
    def set_message(self, text, color):
        self.message, self.message_color = text, color

    def add_holding(self, event=None):
        raw = self.qty_entry.get()
        try:
            symbol, qty = self.portfolio.add(self.selected, raw)
        except ValueError as error:
            self.set_message(str(error), BAD)
        else:
            self.set_message(f"Added {qty:,} x {symbol}", GOOD)
            self.qty_entry.delete(0, tk.END)
        self.render()

    def save(self, kind):
        if self.portfolio.is_empty():
            self.set_message("Add at least one stock before saving.", BAD)
        else:
            name = "portfolio.txt" if kind == "txt" else "portfolio.csv"
            path = os.path.join(BASE_DIR, name)
            try:
                if kind == "txt":
                    self.portfolio.save_txt(path)
                else:
                    self.portfolio.save_csv(path)
                self.set_message(f"Saved {name} next to this program.", GOOD)
            except OSError as error:
                self.set_message(f"Could not save: {error}", BAD)
        self.render()

    def clear_all(self):
        self.portfolio.clear()
        self.set_message("Portfolio cleared.", MUTED)
        self.render()

    # ---------------------------------------------------------------- clicks
    @staticmethod
    def inside(box, x, y):
        x0, y0, x1, y1 = box
        return x0 <= x <= x1 and y0 <= y <= y1

    def on_click(self, event):
        x, y = event.x, event.y

        for symbol, box in self.chip_boxes.items():
            if self.inside(box, x, y):
                self.selected = symbol
                self.set_message(f"{symbol} selected. Enter a quantity.", MUTED)
                self.render()
                self.qty_entry.focus_set()
                return

        for symbol, box in self.remove_boxes.items():
            if self.inside(box, x, y):
                self.portfolio.remove(symbol)
                self.set_message(f"Removed {symbol}.", MUTED)
                self.render()
                return

        add = (self.add_box[0], self.add_box[1], self.add_box[2], self.add_box[3] + 6)
        if self.inside(add, x, y):
            self.add_holding()
        elif self.inside(self.txt_box, x, y):
            self.save("txt")
        elif self.inside(self.csv_box, x, y):
            self.save("csv")
        elif self.inside(self.clear_box, x, y):
            self.clear_all()


def main():
    PortfolioApp().mainloop()


if __name__ == "__main__":
    main()
