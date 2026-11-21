#!/usr/bin/env python3
"""
THE WORLD IN ONE DAY - Friday, November 20, 2026
A one-image summary of the day's world news, drawn entirely in code.

Standard library only. No network. Fully deterministic: running this
program any number of times produces byte-identical output.

Output: /output/entry.png  (falls back to ./entry.png)
Canvas: 1024 x 1024, well under 1 MiB.
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- font
# 5x7 bitmap font, rows top-to-bottom, '#' = ink.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".....", "..#.."),
    ",": (".....", ".....", ".....", ".....", "..#..", "..#..", ".#..."),
    ":": (".....", "..#..", ".....", ".....", ".....", "..#..", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#.##."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "*": (".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."),
}

# ---------------------------------------------------------------- canvas
PAPER = (247, 243, 233)
CARD = (255, 255, 255)
INK = (18, 18, 20)
RED = (178, 34, 34)
NAVY = (16, 42, 74)
GOLD = (176, 124, 28)
GREEN = (30, 130, 76)
GREY = (96, 96, 100)
BLACK = (10, 10, 12)
CREAM = (247, 243, 233)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set_px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            if 0 <= yy < self.h:
                base = (yy * self.w) * 3
                for xx in range(x, x + w):
                    if 0 <= xx < self.w:
                        i = base + xx * 3
                        self.px[i:i + 3] = bytes(color)

    def outline(self, x, y, w, h, color, t=2):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def line_h(self, x, y, w, color, t=2):
        self.rect(x, y, w, t, color)

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set_px(xx, yy, color)

    def ring(self, cx, cy, r, color, t=3):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - t) * (r - t) <= d2 <= (r + t) * (r + t):
                    self.set_px(xx, yy, color)

    def tri_up(self, cx, cy, s, color):
        for row in range(s):
            half = row
            for xx in range(cx - half, cx + half + 1):
                self.set_px(xx, cy - s + 1 + row, color)

    def tri_down(self, cx, cy, s, color):
        for row in range(s):
            half = row
            for xx in range(cx - half, cx + half + 1):
                self.set_px(xx, cy + s - 1 - row, color)

    # ------------------------------------------------------------ text
    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text(self, x, y, s, scale, color):
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for gy, row in enumerate(glyph):
                for gx, cell in enumerate(row):
                    if cell == "#":
                        self.rect(x + gx * scale, y + gy * scale,
                                  scale, scale, color)
            x += 6 * scale
        return x

    def text_c(self, cx, y, s, scale, color):
        x = cx - self.text_w(s, scale) // 2
        self.text(x, y, s, scale, color)

    def wrap(self, s, scale, max_w):
        words = s.split(" ")
        lines = []
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if self.text_w(trial, scale) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def text_wrap(self, x, y, s, scale, color, max_w, leading):
        lines = self.wrap(s, scale, max_w)
        for ln in lines:
            self.text(x, y, ln, scale, color)
            y += leading
        return y


# ---------------------------------------------------------------- png
def save_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(bytes(png))
    return len(png)


# ---------------------------------------------------------------- art
def kicker(cv, x, y, num, label, color):
    cv.text(x, y, num, 3, GOLD)
    cv.text(x + 48, y + 4, label, 2, color)


def draw(cv):
    M = 36            # margin
    CW = W - 2 * M    # content width = 952

    cv.rect(0, 0, W, H, PAPER)

    # ---------------------------------------------------------- masthead
    cv.text_c(W // 2, 34, "GLOBAL NEWS SUMMARY", 2, RED)
    cv.text_c(W // 2, 60, "THE WORLD IN ONE DAY", 7, INK)
    cv.text_c(W // 2, 126, "FRIDAY - NOVEMBER 20, 2026", 3, NAVY)
    cv.text_c(W // 2, 156, "EVERY TOP STORY OF THE DAY - ON A SINGLE PAGE", 2, GREY)
    cv.line_h(M, 182, CW, INK, 5)
    cv.line_h(M, 192, CW, INK, 2)

    # ---------------------------------------------------------- ticker
    cv.rect(M, 206, CW, 62, BLACK)
    seg = [
        ("MARKETS:", GOLD),
        ("  S&P 500 7,176 ", CREAM), ("-2.02%", (240, 110, 110)),
        ("  NIKKEI ", CREAM), ("-4.8%", (240, 110, 110)),
        ("  FTSE 10,453 ", CREAM), ("-0.93%", (240, 110, 110)),
    ]
    x = M + 16
    for s, c in seg:
        x = cv.text(x, 216, s, 2, c)
    seg2 = [
        ("BITCOIN $61,700 ", CREAM), ("LOWEST SINCE JULY", (240, 110, 110)),
        ("  BRENT $90.05 ", CREAM), ("+0.68%", (120, 220, 150)),
    ]
    x = M + 16
    for s, c in seg2:
        x = cv.text(x, 240, s, 2, c)

    # ---------------------------------------------------------- lead row
    LY, LH = 284, 282
    # left: top story
    cv.rect(M, LY, 596, LH, CARD)
    cv.outline(M, LY, 596, LH, INK, 3)
    cv.text(M + 20, LY + 18, "01", 5, GOLD)
    cv.text(M + 118, LY + 26, "TOP STORY - KYIV", 2, RED)
    hy = LY + 62
    for ln in ("RUSSIA STRIKES", "THREE KYIV", "BRIDGES OVERNIGHT"):
        cv.text(M + 20, hy, ln, 4, INK)
        hy += 37
    cv.line_h(M + 20, LY + 212, 220, RED, 4)
    cv.text_wrap(M + 20, LY + 222, "MISSILES AND DRONES HIT THREE BRIDGES "
                 "AND CUT POWER, KILLING AT LEAST EIGHT ACROSS UKRAINE "
                 "AFTER PUTIN VOWED REVENGE.", 2, INK, 556, 19)
    # right: summit
    RX = 648
    cv.rect(RX, LY, 340, LH, CARD)
    cv.outline(RX, LY, 340, LH, INK, 3)
    cv.text(RX + 20, LY + 18, "02", 5, GOLD)
    cv.text(RX + 118, LY + 26, "US SENATE", 2, NAVY)
    hy = LY + 62
    for ln in ("SENATE BLOCKS", "IRAN WAR-POWERS", "VOTE 51-48"):
        cv.text(RX + 20, hy, ln, 3, INK)
        hy += 30
    cv.line_h(RX + 20, LY + 160, 160, NAVY, 4)
    cv.text_wrap(RX + 20, LY + 174, "THE SENATE REJECTED A BID TO HALT US "
                 "FIGHTING WITH IRAN. TRUMP SAYS HE IS IN NO RUSH ON "
                 "THE NEXT STEP.", 2, INK, 300, 20)

    # ---------------------------------------------------------- card grid
    cards = [
        ("03", "TECH + MARKETS", RED, "ANTHROPIC +17% DEBUT",
         "THE AI MAKER CLOSED AT $97.17 IN A RECORD $81.3B IPO - YET "
         "STOCKS SLID A SIXTH STRAIGHT DAY."),
        ("04", "MIDDLE EAST", RED, "MISSILE HITS RIYADH",
         "A HOUTHI MISSILE DAMAGED RIYADH'S TALLEST TOWER, BLOWING OUT "
         "WINDOWS ACROSS SEVEN FLOORS."),
        ("05", "EUROPE", NAVY, "POLAND AIRSPACE HIT",
         "RUSSIA VIOLATED POLISH AIRSPACE WITH MISSILES AND A DRONE. "
         "ESTONIA CLOSES ITS BORDER FROM DEC 1."),
        ("06", "HEALTH + CLIMATE", NAVY, "EBOLA: LAST PATIENT",
         "KENYA DISCHARGED ITS LAST EBOLA PATIENT, 37 DAYS AFTER THE "
         "FIRST CASE. COP31 DROPS FOSSIL PHASE-OUT."),
    ]
    GY = 582
    for i, (num, kick, kc, head, body) in enumerate(cards):
        cx = M + (i % 2) * 484
        cy = GY + (i // 2) * 158
        cv.rect(cx, cy, 468, 146, CARD)
        cv.outline(cx, cy, 468, 146, INK, 2)
        kicker(cv, cx + 16, cy + 14, num, kick, kc)
        cv.text(cx + 16, cy + 50, head, 3, INK)
        cv.text_wrap(cx + 16, cy + 88, body, 2, INK, 436, 19)

    # ---------------------------------------------------------- also today
    AY = 916
    cv.text(M, AY, "ALSO TODAY", 2, RED)
    cv.line_h(M + 130, AY + 5, CW - 130, INK, 2)
    items = [
        "* SENATE PASSES PERMIT BILL 62-33",
        "* US-VENEZUELA RESTORE TIES",
        "* TRUMP PARDONS PETE ROSE",
        "* GOOGLE LAUNCHES GEMINI 4 NEON",
    ]
    for i, it in enumerate(items):
        ix = M + (i % 2) * 484
        iy = AY + 26 + (i // 2) * 24
        cv.text(ix, iy, it, 2, INK)

    # ---------------------------------------------------------- footer
    cv.line_h(M, 986, CW, INK, 2)
    cv.text_c(W // 2, 996, "ONE DAY - ONE PLANET - 20.11.2026", 2, GREY)


def main():
    cv = Canvas(W, H, PAPER)
    draw(cv)
    try:
        os.makedirs("/output", exist_ok=True)
        path = "/output/entry.png"
        n = save_png(cv, path)
    except OSError:
        path = "entry.png"
        n = save_png(cv, path)
    print("wrote", path, n, "bytes")


if __name__ == "__main__":
    main()
