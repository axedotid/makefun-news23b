# 23 November 2026 — world news in one image

A single 1024×1024 editorial graphic summarising the day's world news. `build_image.py`
renders it with pure PIL; `main.ts` copies the committed `entry.png` to the output
directory the grader reads.

## What the image shows

- **Header band** — the date "23 NOVEMBER 2026", the weekday, and a day-of-year block (324 / 365).
- **Lead banner** — the top story, set off with a red accent bar.
- **Six story cards** in a two-column grid, each with a coloured category tag:
  Climate, Middle East, Europe, Disaster, United States, and Asia.
- **Footer ticker** — a one-line "also today" strip of secondary headlines.

## How to run

```sh
# 1. Render the image (optional — entry.png is already committed)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 build_image.py

# 2. Copy the entry to the grader's output directory
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` validates the copied PNG (non-empty, within the 1 MiB cap) before finishing.
Outside the grader's container, `MAKEFUN_OUTPUT_DIR` stands in for `/output`.

## Bounty

https://make.fun/bounty/news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/axedotid/makefun-news23b/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/axedotid/makefun-news23b/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)