# make.fun bounty entry: news-image-20261125
# "Sum up 25 November's world news in one image."
#
# The entry image is a 1024x1024 newspaper front page ("THE WORLD IN
# ONE DAY"), drawn with Python/PIL in build_image.py (included in this
# repo for provenance) from the verified news of Wednesday 25 November
# 2026 -- 50 stories in 10 regions and 20 fields, every one happened or
# first reported on that day: the U.S. proposes tariffs of up to 35% on
# 14 economies; AI doubts sink Asian chip stocks (Kospi -6.2%); Pakistan's
# first astronaut docks at China's Tiangong station; Russian strikes cut
# power in 5 Ukrainian regions; the UK energy cap rises 26% in January;
# the Solomons sign a security pact with Australia; plus 37 more stories
# in a numbered list, a UTC timeline, a stat strip and a pinned world map.
# Each of the 13 biggest stories carries its own drawn scene and an
# OFFICIAL / CONFIRMED / REPORTED tag; a date check names the near-miss
# stories left out because they belong to other days (Chen Jining probe
# and the Huawei verdict are 24 November).
#
# The image itself is stored in this repo as entry.png (1024x1024, under
# 1 MiB). This program, Python 3.13 standard library only, copies it to
# /output/entry.png. No network, no timestamps, no randomness -- two runs
# write identical bytes.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
