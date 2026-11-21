[![make.fun bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/utus729-cmyk/Makefun-2-event/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/utus729-cmyk/Makefun-2-event/reward.svg)](https://make.fun/bounty/news-image-20261120)
[make.fun bounty: Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120)# The World in One Day — 20 November 2026

A program that draws a one-image summary of the world news of
**Friday, November 20, 2026** as a newspaper front page.

Built for the make.fun bounty "Sum up 20 November's world news in one
image" ($250, 50 winners, AI judging) — the daily follow-up to the
19 November edition, which the same author entered on 20 Nov 2026
(repo `utus729-cmyk/Makefun-event`, status "Submitted. Checks are running.").

## Run it

```sh
python3 main.py
```

- Python 3, standard library only. No network access.
- Writes `/output/entry.png` (falls back to `./entry.png`).
- Output: 1024 × 1024 PNG, 20,237 bytes.
- **Deterministic:** every run produces byte-identical output
  (SHA-256 `bb56a9e4c9d2755bcbdb0eae84e8d74584cec9c76aed85d64720883de8b08d29`).

## What's on the page

1. **Kyiv bridges hit:** Russia strikes three Kyiv bridges overnight, killing at least eight across Ukraine
2. **US Senate:** blocks the Iran war-powers resolution, 51–48
3. **Anthropic +17% debut** — closed at $97.17 in a record $81.3B IPO, yet stocks slid a sixth straight day
4. **Missile hits Riyadh:** Houthi missile damages the city's tallest tower
5. **Poland airspace violated** by Russian missiles and a drone; Estonia to close its border from Dec 1
6. **Ebola:** Kenya discharges its last patient, 37 days after the first case; COP31 draft drops the fossil phase-out call
- Markets at the close (S&P 500, Nikkei, FTSE, Bitcoin, Brent)
- Also today: Senate passes the permit bill 62–33, US–Venezuela restore ties, Trump pardons Pete Rose, Google launches Gemini 4 Neon

All headlines are the real, widely reported top stories of 20 Nov 2026.
The image is rendered entirely in code — an embedded 5×7 bitmap font,
hand-drawn panels, and a hand-rolled PNG encoder (zlib + struct).

## License

MIT — see `LICENSE`.
