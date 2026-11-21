# Session log — The World in One Day, 20 November 2026

## What was built

A Python program (`main.py`, standard library only, no network) that draws
a one-image newspaper-style summary of the world news of Friday,
20 November 2026, and writes it to `/output/entry.png`
(1024 × 1024 PNG, deterministic — repeated runs are byte-identical).

## How it was built

1. Researched the top stories of 20 Nov 2026 from public news roundups
   (One Turn News day page for 20 Nov 2026, Teh World News roundup,
   Daily News video summary for 20 Nov 2026).
2. Adapted the verified 19 November edition program
   (`~/workspace/makefun-news/main.py`, already submitted and accepted
   for bounty news-image-20261119) to the 20 November stories:
   Kyiv bridge strikes, Senate Iran war-powers vote 51–48, Anthropic
   +17% Nasdaq debut, Houthi missile hitting Riyadh's tallest tower,
   Poland airspace violation, Kenya's last Ebola patient discharged,
   COP31 draft dropping the fossil phase-out call, plus the market
   ticker (S&P 500 7,176 −2.02%, Nikkei −4.8%, FTSE 10,453 −0.93%,
   Bitcoin ~$61,700, Brent $90.05 +0.68%).
3. Ran the program twice and compared SHA-256 hashes to confirm the
   output is byte-identical (deterministic, as the bounty requires).
   Final run: `/output/entry.png`, 20,237 bytes, 1024 × 1024 RGB PNG,
   SHA-256 `bb56a9e4c9d2755bcbdb0eae84e8d74584cec9c76aed85d64720883de8b08d29`.
   First visual check found body text spilling past panel borders in
   all six story panels; all six bodies were shortened to fit and the
   program was re-run twice — second visual check passed, every story,
   ticker value and footer fully inside the canvas and its panels.

## Notes

- All headlines are real, widely reported stories of 20 Nov 2026.
- No paid services, no API keys, no network calls in the program.
- Entry target: make.fun bounty "Sum up 20 November's world news in
  one image" ($250, 50 winners, AI judging). Submission steps (GitHub
  repo created after the bounty opened, badge in README, About section,
  official transcript bundle, Phantom signature) are the same as the
  19 November entry and are done by the user from their phone.
