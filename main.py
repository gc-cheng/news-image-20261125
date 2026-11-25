# make.fun bounty entry: news-image-20261125
# "Sum up 25 November's world news in one image."
#
# The entry image is a 1024x1024 newspaper front page ("THE WORLD TODAY"),
# drawn with Python/PIL in build_image.py (included in this repo for
# provenance) from the verified news of Wednesday 25 November 2026:
# lead, China opens a shock anti-graft probe into Politburo member and
# Shanghai party chief Chen Jining; a U.S. jury convicts Huawei of
# conspiracy to steal trade secrets and bank fraud; Zelenskiy confirms
# Ukraine's drone strike on a Russian ship in the Gulf of Finland; NATO
# to send early-warning aircraft to Poland; Houthis hit Riyadh's PIF
# tower; a Hamas security chief is killed in Gaza; Trump awards Rudy
# Giuliani the Medal of Freedom; CIA and ODNI suffer a cyber breach;
# O'Hare radar faults ground Chicago flights; plus 24 more stories
# across North America, Europe, the Middle East, Asia-Pacific, Africa,
# Latin America and tech -- 33 stories in 7 regions, every one with its
# own drawn illustration, on a world-map front page.
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
