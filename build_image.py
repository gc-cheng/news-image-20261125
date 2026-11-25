#!/usr/bin/env python3
"""Build the news-image-20261125 front page deterministically with PIL.

1024x1024 newspaper front page, "THE WORLD TODAY", Wednesday 25 November
2026: 33 verified stories across 7 regions, every story with its own small
drawn illustration, plus a world-map locator strip. All text comes from the
verified news list in the task notes; no invented dates, numbers or quotes.
No network, no timestamps, no randomness: running this twice writes
byte-identical PNG bytes (verified by sha256).
"""
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

W = H = 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
GREY = (96, 92, 84)
RULE = (178, 172, 160)
RED = (178, 32, 22)
NAVY = (18, 38, 66)
BLUE = (29, 78, 137)
TEAL = (14, 90, 90)
GREEN = (34, 110, 72)
AMBER = (172, 102, 0)
PURPLE = (96, 64, 138)
MAPLAND = (203, 197, 186)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, max_w):
    """Greedy word wrap; explicit \n in text forces a line break."""
    out = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


def draw_lines(draw, x, y, text, fnt, max_w, fill=INK, leading=1.2, max_lines=None):
    lines = wrap_lines(draw, text, fnt, max_w)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".,") + "\u2026"
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


# ---------------------------------------------------------------- icons
# Every icon draws white on a coloured tile, centred at (cx, cy), size s.

def ico_medal(d, cx, cy, s):
    d.polygon([(cx - s * .18, cy + s * .05), (cx + s * .18, cy + s * .05),
               (cx + s * .32, cy + s * .42), (cx - s * .32, cy + s * .42)], fill=(255, 255, 255))
    d.ellipse([cx - s * .26, cy - s * .42, cx + s * .26, cy + s * .1], fill=(255, 255, 255))
    d.text((cx - s * .09, cy - s * .34), "*", font=font(SANS_B, int(s * .42)), fill=RED)


def ico_bird(d, cx, cy, s):
    d.ellipse([cx - s * .34, cy - s * .05, cx + s * .30, cy + s * .38], fill=(255, 255, 255))
    d.ellipse([cx + s * .10, cy - s * .36, cx + s * .38, cy - s * .08], fill=(255, 255, 255))
    d.polygon([(cx + s * .36, cy - s * .26), (cx + s * .52, cy - s * .18),
               (cx + s * .36, cy - s * .12)], fill=(255, 215, 0))
    d.arc([cx - s * .28, cy - s * .02, cx + s * .12, cy + s * .34], 200, 340, fill=RED, width=2)


def ico_radar(d, cx, cy, s):
    d.ellipse([cx - s * .36, cy - s * .36, cx + s * .36, cy + s * .36], outline=(255, 255, 255), width=2)
    d.ellipse([cx - s * .20, cy - s * .20, cx + s * .20, cy + s * .20], outline=(255, 255, 255), width=2)
    d.line([(cx, cy - s * .36), (cx, cy + s * .36)], fill=(255, 255, 255), width=2)
    d.line([(cx - s * .36, cy), (cx + s * .36, cy)], fill=(255, 255, 255), width=2)
    d.line([(cx, cy), (cx + s * .30, cy - s * .30)], fill=(255, 215, 0), width=3)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 215, 0))


def ico_lock(d, cx, cy, s):
    d.arc([cx - s * .18, cy - s * .38, cx + s * .18, cy - s * .02], 180, 360, fill=(255, 255, 255), width=3)
    d.rounded_rectangle([cx - s * .30, cy - s * .06, cx + s * .30, cy + s * .38], radius=4, fill=(255, 255, 255))
    d.ellipse([cx - 2, cy + s * .08, cx + 2, cy + s * .12], fill=NAVY)


def ico_clock(d, cx, cy, s):
    d.ellipse([cx - s * .36, cy - s * .36, cx + s * .36, cy + s * .36], outline=(255, 255, 255), width=3)
    d.line([(cx, cy), (cx, cy - s * .24)], fill=(255, 255, 255), width=3)
    d.line([(cx, cy), (cx + s * .20, cy + s * .08)], fill=(255, 255, 255), width=3)


def ico_money(d, cx, cy, s):
    d.rectangle([cx - s * .36, cy - s * .22, cx + s * .36, cy + s * .22], outline=(255, 255, 255), width=2)
    d.ellipse([cx - s * .14, cy - s * .14, cx + s * .14, cy + s * .14], outline=(255, 255, 255), width=2)
    d.text((cx - s * .07, cy - s * .13), "$", font=font(SANS_B, int(s * .30)), fill=(255, 255, 255))


def ico_helmet(d, cx, cy, s):
    d.pieslice([cx - s * .36, cy - s * .34, cx + s * .36, cy + s * .30], 180, 360, fill=(255, 255, 255))
    d.rectangle([cx - s * .42, cy + s * .06, cx + s * .42, cy + s * .14], fill=(255, 255, 255))
    d.text((cx - s * .09, cy - s * .30), "*", font=font(SANS_B, int(s * .34)), fill=NAVY)


def ico_ship(d, cx, cy, s):
    d.polygon([(cx - s * .38, cy + s * .08), (cx + s * .38, cy + s * .08),
               (cx + s * .24, cy + s * .36), (cx - s * .24, cy + s * .36)], fill=(255, 255, 255))
    d.line([(cx, cy + s * .08), (cx, cy - s * .34)], fill=(255, 255, 255), width=3)
    d.polygon([(cx, cy - s * .34), (cx + s * .26, cy - s * .22), (cx, cy - s * .10)], fill=(255, 215, 0))
    d.line([(cx - s * .44, cy + s * .42), (cx + s * .44, cy + s * .42)], fill=(255, 255, 255), width=2)


def ico_jet(d, cx, cy, s):
    d.polygon([(cx - s * .10, cy - s * .38), (cx + s * .34, cy + s * .30),
               (cx + s * .10, cy + s * .30), (cx - s * .02, cy + s * .02)], fill=(255, 255, 255))
    d.polygon([(cx - s * .38, cy + s * .10), (cx - s * .02, cy + s * .02),
               (cx - s * .02, cy + s * .22), (cx - s * .30, cy + s * .30)], fill=(255, 255, 255))


def ico_court(d, cx, cy, s):
    d.polygon([(cx - s * .38, cy - s * .30), (cx + s * .38, cy - s * .30),
               (cx, cy - s * .44)], fill=(255, 255, 255))
    for dx in (-.26, 0, .26):
        d.rectangle([cx + dx * s - 2, cy - s * .26, cx + dx * s + 2, cy + s * .30], fill=(255, 255, 255))
    d.rectangle([cx - s * .40, cy + s * .30, cx + s * .40, cy + s * .38], fill=(255, 255, 255))


def ico_satellite(d, cx, cy, s):
    d.rectangle([cx - s * .12, cy - s * .12, cx + s * .12, cy + s * .12], fill=(255, 255, 255))
    d.rectangle([cx - s * .42, cy - s * .08, cx - s * .16, cy + s * .08], outline=(255, 255, 255), width=2)
    d.rectangle([cx + s * .16, cy - s * .08, cx + s * .42, cy + s * .08], outline=(255, 255, 255), width=2)
    d.line([(cx, cy - s * .12), (cx + s * .14, cy - s * .34)], fill=(255, 255, 255), width=2)
    d.ellipse([cx + s * .10, cy - s * .38, cx + s * .18, cy - s * .30], fill=(255, 215, 0))


def ico_ball(d, cx, cy, s):
    d.ellipse([cx - s * .36, cy - s * .36, cx + s * .36, cy + s * .36], outline=(255, 255, 255), width=2)
    d.polygon([(cx, cy - s * .16), (cx + s * .15, cy - s * .05), (cx + s * .09, cy + s * .13),
               (cx - s * .09, cy + s * .13), (cx - s * .15, cy - s * .05)], fill=(255, 255, 255))
    d.line([(cx, cy - s * .36), (cx, cy - s * .16)], fill=(255, 255, 255), width=2)
    d.line([(cx - s * .34, cy - s * .10), (cx - s * .15, cy - s * .05)], fill=(255, 255, 255), width=2)
    d.line([(cx + s * .34, cy - s * .10), (cx + s * .15, cy - s * .05)], fill=(255, 255, 255), width=2)


def ico_chess(d, cx, cy, s):
    d.ellipse([cx - s * .13, cy - s * .38, cx + s * .13, cy - s * .12], fill=(255, 255, 255))
    d.polygon([(cx - s * .10, cy - s * .10), (cx + s * .10, cy - s * .10),
               (cx + s * .24, cy + s * .30), (cx - s * .24, cy + s * .30)], fill=(255, 255, 255))
    d.rectangle([cx - s * .30, cy + s * .30, cx + s * .30, cy + s * .38], fill=(255, 255, 255))


def ico_ban(d, cx, cy, s):
    d.ellipse([cx - s * .36, cy - s * .36, cx + s * .36, cy + s * .36], outline=(255, 255, 255), width=3)
    d.line([(cx - s * .26, cy + s * .26), (cx + s * .26, cy - s * .26)], fill=(255, 255, 255), width=3)


def ico_tower(d, cx, cy, s):
    d.rectangle([cx - s * .14, cy - s * .30, cx + s * .14, cy + s * .38], fill=(255, 255, 255))
    d.rectangle([cx - s * .08, cy - s * .44, cx + s * .08, cy - s * .30], fill=(255, 255, 255))
    d.line([(cx, cy - s * .44), (cx, cy - s * .58)], fill=(255, 255, 255), width=2)
    for wy in (-.16, .02, .20):
        d.rectangle([cx - s * .07, cy + wy * s, cx + s * .07, cy + wy * s + 3], fill=NAVY)


def ico_target(d, cx, cy, s):
    for r in (.36, .24, .12):
        d.ellipse([cx - s * r, cy - s * r, cx + s * r, cy + s * r], outline=(255, 255, 255), width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 215, 0))


def ico_flag(d, cx, cy, s):
    d.line([(cx - s * .20, cy - s * .40), (cx - s * .20, cy + s * .40)], fill=(255, 255, 255), width=3)
    d.polygon([(cx - s * .20, cy - s * .40), (cx + s * .38, cy - s * .28),
               (cx - s * .20, cy - s * .12)], fill=(255, 215, 0))


def ico_aid(d, cx, cy, s):
    d.ellipse([cx - s * .36, cy - s * .36, cx + s * .36, cy + s * .36], outline=(255, 255, 255), width=2)
    d.rectangle([cx - s * .07, cy - s * .22, cx + s * .07, cy + s * .22], fill=(255, 255, 255))
    d.rectangle([cx - s * .22, cy - s * .07, cx + s * .22, cy + s * .07], fill=(255, 255, 255))


def ico_flame(d, cx, cy, s):
    d.polygon([(cx, cy - s * .42), (cx + s * .26, cy - s * .02), (cx + s * .20, cy + s * .30),
               (cx - s * .20, cy + s * .30), (cx - s * .26, cy - s * .02)], fill=(255, 255, 255))
    d.polygon([(cx, cy - s * .18), (cx + s * .12, cy + s * .02), (cx, cy + s * .22),
               (cx - s * .12, cy + s * .02)], fill=(255, 215, 0))


def ico_oil(d, cx, cy, s):
    d.polygon([(cx, cy - s * .40), (cx + s * .26, cy + s * .02), (cx + s * .20, cy + s * .30),
               (cx - s * .20, cy + s * .30), (cx - s * .26, cy + s * .02)], fill=(255, 255, 255))


def ico_pill(d, cx, cy, s):
    d.rounded_rectangle([cx - s * .38, cy - s * .16, cx + s * .38, cy + s * .16], radius=8, fill=(255, 255, 255))
    d.line([(cx, cy - s * .16), (cx, cy + s * .16)], fill=NAVY, width=2)


def ico_rocket(d, cx, cy, s):
    d.polygon([(cx, cy - s * .42), (cx + s * .16, cy - s * .02), (cx + s * .16, cy + s * .18),
               (cx - s * .16, cy + s * .18), (cx - s * .16, cy - s * .02)], fill=(255, 255, 255))
    d.polygon([(cx - s * .16, cy + s * .10), (cx - s * .30, cy + s * .30), (cx - s * .10, cy + s * .22)], fill=(255, 255, 255))
    d.polygon([(cx + s * .16, cy + s * .10), (cx + s * .30, cy + s * .30), (cx + s * .10, cy + s * .22)], fill=(255, 255, 255))
    d.polygon([(cx - s * .08, cy + s * .18), (cx + s * .08, cy + s * .18), (cx, cy + s * .42)], fill=(255, 215, 0))


def ico_plane(d, cx, cy, s):
    d.ellipse([cx - s * .40, cy - s * .10, cx + s * .40, cy + s * .10], fill=(255, 255, 255))
    d.polygon([(cx - s * .05, cy - s * .08), (cx + s * .10, cy - s * .42),
               (cx + s * .18, cy - s * .42), (cx + s * .16, cy - s * .06)], fill=(255, 255, 255))
    d.polygon([(cx - s * .30, cy + s * .02), (cx - s * .14, cy + s * .34),
               (cx - s * .06, cy + s * .34), (cx - s * .10, cy + s * .04)], fill=(255, 255, 255))


def ico_robot(d, cx, cy, s):
    d.rectangle([cx - s * .26, cy - s * .22, cx + s * .26, cy + s * .30], outline=(255, 255, 255), width=2)
    d.line([(cx, cy - s * .22), (cx, cy - s * .40)], fill=(255, 255, 255), width=2)
    d.ellipse([cx - 2, cy - s * .44, cx + 2, cy - s * .40], fill=(255, 215, 0))
    d.ellipse([cx - s * .14, cy - s * .10, cx - s * .06, cy - s * .02], fill=(255, 255, 255))
    d.ellipse([cx + s * .06, cy - s * .10, cx + s * .14, cy - s * .02], fill=(255, 255, 255))
    d.line([(cx - s * .12, cy + s * .16), (cx + s * .12, cy + s * .16)], fill=(255, 255, 255), width=2)


def ico_ballot(d, cx, cy, s):
    d.rectangle([cx - s * .30, cy - s * .10, cx + s * .30, cy + s * .38], outline=(255, 255, 255), width=2)
    d.line([(cx - s * .16, cy - s * .10), (cx - s * .16, cy - s * .30)], fill=(255, 255, 255), width=2)
    d.line([(cx + s * .16, cy - s * .10), (cx + s * .16, cy - s * .30)], fill=(255, 255, 255), width=2)
    d.line([(cx - s * .18, cy + s * .10), (cx - s * .04, cy + s * .26), (cx + s * .22, cy - s * .02)],
           fill=(255, 215, 0), width=3)


def ico_trophy(d, cx, cy, s):
    d.polygon([(cx - s * .24, cy - s * .36), (cx + s * .24, cy - s * .36),
               (cx + s * .14, cy - s * .02), (cx - s * .14, cy - s * .02)], fill=(255, 255, 255))
    d.arc([cx - s * .38, cy - s * .36, cx - s * .10, cy - s * .02], 90, 270, fill=(255, 255, 255), width=2)
    d.arc([cx + s * .10, cy - s * .36, cx + s * .38, cy - s * .02], 270, 90, fill=(255, 255, 255), width=2)
    d.rectangle([cx - 2, cy - s * .02, cx + 2, cy + s * .24], fill=(255, 255, 255))
    d.rectangle([cx - s * .20, cy + s * .24, cx + s * .20, cy + s * .32], fill=(255, 255, 255))


def ico_mine(d, cx, cy, s):
    for k in range(8):
        import math
        a = k * math.pi / 4
        d.line([(cx + s * .30 * math.cos(a), cy + s * .30 * math.sin(a)),
                (cx + s * .44 * math.cos(a), cy + s * .44 * math.sin(a))], fill=(255, 255, 255), width=2)
    d.ellipse([cx - s * .26, cy - s * .26, cx + s * .26, cy + s * .26], fill=(255, 255, 255))
    d.ellipse([cx - s * .10, cy - s * .10, cx + s * .10, cy + s * .10], fill=NAVY)


def ico_alert(d, cx, cy, s):
    d.polygon([(cx, cy - s * .38), (cx + s * .38, cy + s * .30), (cx - s * .38, cy + s * .30)], fill=(255, 255, 255))
    d.text((cx - 3, cy - s * .16), "!", font=font(SANS_B, int(s * .44)), fill=RED)


def ico_bomb(d, cx, cy, s):
    d.ellipse([cx - s * .28, cy - s * .08, cx + s * .28, cy + s * .40], fill=(255, 255, 255))
    d.line([(cx + s * .10, cy - s * .08), (cx + s * .26, cy - s * .30)], fill=(255, 255, 255), width=2)
    d.text((cx + s * .20, cy - s * .46), "*", font=font(SANS_B, int(s * .34)), fill=(255, 215, 0))


def ico_bug(d, cx, cy, s):
    d.ellipse([cx - s * .18, cy - s * .10, cx + s * .18, cy + s * .36], fill=(255, 255, 255))
    d.ellipse([cx - s * .10, cy - s * .34, cx + s * .10, cy - s * .12], fill=(255, 255, 255))
    for dy in (-.02, .12, .26):
        d.line([(cx - s * .18, cy + dy * s), (cx - s * .42, cy + (dy - .12) * s)], fill=(255, 255, 255), width=2)
        d.line([(cx + s * .18, cy + dy * s), (cx + s * .42, cy + (dy - .12) * s)], fill=(255, 255, 255), width=2)


ICONS = {
    "medal": ico_medal, "bird": ico_bird, "radar": ico_radar, "lock": ico_lock,
    "clock": ico_clock, "money": ico_money, "helmet": ico_helmet, "ship": ico_ship,
    "jet": ico_jet, "court": ico_court, "satellite": ico_satellite, "ball": ico_ball,
    "chess": ico_chess, "ban": ico_ban, "tower": ico_tower, "target": ico_target,
    "flag": ico_flag, "aid": ico_aid, "flame": ico_flame, "oil": ico_oil,
    "pill": ico_pill, "rocket": ico_rocket, "plane": ico_plane, "robot": ico_robot,
    "ballot": ico_ballot, "trophy": ico_trophy, "mine": ico_mine, "alert": ico_alert,
    "bomb": ico_bomb, "bug": ico_bug,
}

# ------------------------------------------------------------- the stories
# (region, tag, icon, headline, summary) — all verified in the 25 Nov 2026
# morning editions (Reuters, AP, AFP, SCMP, The Hindu, NYT, Manila Times).
GRID = [
    ("N AMERICA", BLUE, "medal", "TRUMP HONOURS\nGIULIANI",
     "Trump awards Giuliani the Medal of Freedom."),
    ("N AMERICA", BLUE, "bird", "TURKEYS\nSPARED",
     "Trump pardons two turkeys for Thanksgiving."),
    ("N AMERICA", BLUE, "radar", "O'HARE RADAR\nCHAOS",
     "Radar fault grounds Chicago flights again."),
    ("N AMERICA", BLUE, "lock", "CIA\nBREACH",
     "U.S. spy agencies hit by cyberattack; data exposed."),
    ("N AMERICA", BLUE, "clock", "FORT HOOD\nSTAY BID",
     "Hasan seeks delay to his Dec 3 execution."),
    ("N AMERICA", BLUE, "money", "SHEIN PAYS\n$100M",
     "Retailer settles FTC claims of deceptive practices."),
    ("N AMERICA", BLUE, "helmet", "SOLDIER SOLD\nSECRETS",
     "Soldier admits selling military data to China."),
    ("EUROPE", NAVY, "ship", "UKRAINE\nHITS SHIP",
     "Zelenskiy confirms Gulf of Finland drone strike."),
    ("EUROPE", NAVY, "jet", "NATO JETS\nFOR POLAND",
     "NATO sends early-warning jets to Poland."),
    ("EUROPE", NAVY, "court", "SARKOZY\nTO TRIAL",
     "Sarkozy faces corruption trial in April 2027."),
    ("EUROPE", NAVY, "satellite", "GPS JAMMED\nOFF UK",
     "Russian warship accused of jamming UK flights."),
    ("EUROPE", NAVY, "ball", "MADRID ROUT\nPSV 5\u20131",
     "Bellingham and Mbapp\u00e9 star in 5\u20131 rout."),
    ("EUROPE", NAVY, "chess", "GUKESH\nHOLDS ON",
     "Champion holds Sindarov under time pressure."),
    ("EUROPE", NAVY, "ban", "BRITAIN SANCTIONS\nHOUTHIS",
     "UK blacklists rebels and four top officials."),
    ("MIDEAST", RED, "tower", "HOUTHIS\nHIT TOWER",
     "Houthi missile hits PIF tower; 11 hurt."),
    ("MIDEAST", RED, "target", "HAMAS CHIEF\nKILLED",
     "Security chief dies in Israeli strike on Gaza City."),
    ("MIDEAST", RED, "flag", "EISENKOT'S\nFIRST PACT",
     "Ex-general clinches first coalition deal."),
    ("MIDEAST", RED, "aid", "AID DOUBT\nFOR ISRAEL",
     "Envoy unsure U.S. aid to Israel ends this year."),
    ("MIDEAST", RED, "flame", "HOUTHIS\nNEAR ADEN",
     "Rebels 60 km from Aden; army says city holds."),
    ("MIDEAST", RED, "oil", "IRAQ SEIZES KURD\nOILFIELDS",
     "Baghdad orders federal forces into Kurdish-run fields."),
    ("MIDEAST", RED, "pill", "IRAN'S MEDICINE\nCRISIS",
     "Pharmacies shut as drug shortages bite patients."),
    ("ASIA", TEAL, "rocket", "NORTH KOREA\nTHREAT",
     "Pyongyang threatens to shut Swiss office."),
    ("ASIA", TEAL, "plane", "RUSSIAN JETS\nIN KOREA",
     "Seoul says Russian planes entered its air defence zone."),
    ("ASIA", TEAL, "robot", "HUMAN RULE\nFOR AI WAR",
     "India urges human oversight of AI weapons at the UN."),
    ("ASIA", TEAL, "jet", "50 BOEINGS FOR\nXIAMEN AIR",
     "China Southern unit buys 50 737-8 jets."),
    ("ASIA", TEAL, "ballot", "DUTERTE\nTRIAL DATES",
     "Impeachment verdict expected in December."),
    ("AFRICA", GREEN, "trophy", "SENEGAL GETS\nCUP BACK",
     "CAS returns AFCON title 10 months after chaotic final."),
    ("AFRICA", GREEN, "mine", "LANDMINE TOLL\nHITS 7,000",
     "Myanmar and Syria top a five-year high in casualties."),
    ("LATAM", AMBER, "alert", "CARTAGENA\nHOSTAGES",
     "Gunmen hold 25 hostage in Cartagena."),
    ("LATAM", AMBER, "bomb", "CAR BOMB\nWOUNDS 23",
     "Blast injures at least 23 in Colombia."),
    ("TECH", PURPLE, "bug", "100,000 BUGS\nIN 2026",
     "Software flaws pass 100,000 in 2026."),
]

REGIONS = [
    ("N. AMERICA", BLUE), ("EUROPE", NAVY), ("MIDEAST", RED),
    ("ASIA-PACIFIC", TEAL), ("AFRICA", GREEN), ("LATIN AMERICA", AMBER),
    ("TECH", PURPLE),
]

# Simplified continent outlines, (lon, lat) pairs.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73), (-75, 62),
     (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20), (-78, -5), (-80, 2)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (48, 11), (51, 0), (40, -10), (35, -18), (28, -33), (18, -35),
     (12, -18), (8, 4), (-8, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 68), (50, 60),
     (40, 55), (35, 50), (30, 46), (28, 44), (23, 40), (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37)],
    [(40, 68), (50, 70), (60, 69), (70, 72), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (178, 66), (170, 60), (162, 55), (158, 50), (142, 45), (140, 38),
     (130, 35), (127, 40), (120, 32), (110, 20), (105, 10), (100, 8), (95, 15),
     (90, 22), (85, 20), (80, 8), (77, 8), (72, 20), (66, 25), (60, 25), (55, 26),
     (50, 29), (48, 30), (44, 29), (40, 36), (38, 36), (35, 36)],
    [(114, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (136, -12), (130, -13), (126, -14), (122, -17), (114, -20)],
]
# (lon, lat, region colour) — where the day's stories happened.
DOTS = [
    (116, 40, TEAL), (-77, 39, BLUE), (-87, 42, BLUE), (0, 51, NAVY),
    (30, 50, NAVY), (47, 25, RED), (34, 31, RED), (44, 33, RED),
    (127, 37, TEAL), (77, 28, TEAL), (121, 15, TEAL), (-17, 15, GREEN),
    (-74, 5, AMBER),
]

# ------------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 30
X1 = W - M

# Masthead
d.text((M, 14), "THE WORLD TODAY", font=font(SERIF_B, 56), fill=INK)
d.text((M, 80), "WEDNESDAY, 25 NOVEMBER 2026  \u2022  33 STORIES  \u2022  7 REGIONS",
       font=font(SANS_B, 19), fill=RED)
d.line([(M, 112), (X1, 112)], fill=INK, width=4)
d.line([(M, 118), (X1, 118)], fill=INK, width=1)

# ---- Lead row: China (left), Huawei (middle), drawn scene (right) ----
LY = 128
d.rectangle([(M, LY), (M + 190, LY + 28)], fill=RED)
d.text((M + 10, LY + 4), "LEAD  \u2022  CHINA", font=font(SANS_B, 17), fill=(255, 255, 255))
draw_lines(d, M, LY + 38, "China probes a\nPolitburo member", font(SERIF_B, 42), 460, leading=1.05)
draw_lines(d, M, LY + 140,
           "Shanghai party chief Chen Jining is under investigation in a shock "
           "anti-graft probe, AP reports. The rare probe of a sitting Politburo "
           "member rattles Beijing.",
           font(SANS, 18), 460, leading=1.28, max_lines=4)

hx = 510
d.rectangle([(hx, LY), (hx + 170, LY + 28)], fill=NAVY)
d.text((hx + 10, LY + 4), "U.S.  \u2022  CHINA", font=font(SANS_B, 17), fill=(255, 255, 255))
draw_lines(d, hx, LY + 38, "Huawei guilty\nin U.S. trial", font(SERIF_B, 27), 250, leading=1.05)
draw_lines(d, hx, LY + 108,
           "A U.S. jury convicts the tech giant of conspiracy to steal trade "
           "secrets and bank fraud.",
           font(SANS, 15), 250, leading=1.28, max_lines=4)
# small chip pictogram under the Huawei summary
chip_x, chip_y = hx + 4, LY + 196
d.rounded_rectangle([chip_x, chip_y, chip_x + 34, chip_y + 34], radius=5, fill=NAVY)
d.rectangle([chip_x + 10, chip_y + 10, chip_x + 24, chip_y + 24], outline=(255, 255, 255), width=2)
for px in (14, 24):
    d.line([(chip_x + px, chip_y + 4), (chip_x + px, chip_y + 10)], fill=(255, 255, 255), width=2)
    d.line([(chip_x + px, chip_y + 24), (chip_x + px, chip_y + 30)], fill=(255, 255, 255), width=2)
    d.line([(chip_x + 4, chip_y + px), (chip_x + 10, chip_y + px)], fill=(255, 255, 255), width=2)
    d.line([(chip_x + 24, chip_y + px), (chip_x + 30, chip_y + px)], fill=(255, 255, 255), width=2)

# drawn scene panel: flag, star and hall columns over navy
px0, py0, pw, ph = 780, LY, 214, 234
d.rectangle([(px0, py0), (px0 + pw, py0 + ph)], fill=NAVY)
d.line([(px0 + 24, py0 + 26), (px0 + 24, py0 + 150)], fill=(255, 255, 255), width=3)
d.polygon([(px0 + 24, py0 + 26), (px0 + 96, py0 + 40), (px0 + 24, py0 + 58)], fill=RED)
d.text((px0 + 118, py0 + 30), "\u2605", font=font(SANS_B, 30), fill=(255, 215, 0))
for i in range(5):
    cx0 = px0 + 22 + i * 36
    d.rectangle([cx0, py0 + 150, cx0 + 16, py0 + 196], fill=(235, 230, 220))
d.rectangle([px0 + 14, py0 + 196, px0 + 200, py0 + 204], fill=(235, 230, 220))
d.text((px0 + 14, py0 + 206), "CHEN JINING", font=font(SANS_B, 15), fill=(255, 255, 255))
d.text((px0 + 14, py0 + 221), "SHANGHAI PARTY CHIEF", font=font(SANS, 11), fill=(190, 200, 215))

d.line([(M, 372), (X1, 372)], fill=INK, width=2)

# ---- World map strip with region legend ----
MY0, MY1 = 380, 452
MX0, MX1 = M, 742


def map_xy(lon, lat):
    x = MX0 + (lon + 170) / 360.0 * (MX1 - MX0)
    y = MY0 + (75 - lat) / 130.0 * (MY1 - MY0)
    return x, y


for poly in CONTINENTS:
    d.polygon([map_xy(lon, lat) for lon, lat in poly], fill=MAPLAND, outline=(150, 144, 132))
for lon, lat, colour in DOTS:
    x, y = map_xy(lon, lat)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=colour, outline=(255, 255, 255), width=1)
d.text((MX0, MY0 - 2), "", font=font(SANS_B, 10), fill=GREY)

lx = 758
d.text((lx, MY0 + 2), "REGIONS", font=font(SANS_B, 13), fill=RED)
for i, (name, colour) in enumerate(REGIONS):
    cx = lx + (i % 2) * 118
    cy = MY0 + 20 + (i // 2) * 16
    d.rectangle([cx, cy, cx + 11, cy + 11], fill=colour)
    d.text((cx + 16, cy - 1), name, font=font(SANS_B, 11), fill=INK)

d.line([(M, 462), (X1, 462)], fill=INK, width=2)

# ---- Grid: 31 stories, 8 cols x 4 rows, last cell = sources ----
GY0 = 472
CELL_W, CELL_H = 113, 125
GAP = 8
for i, (tag, colour, icon, head, summ) in enumerate(GRID):
    cx0 = M + (i % 8) * (CELL_W + GAP)
    cy0 = GY0 + (i // 8) * (CELL_H + GAP)
    d.rectangle([(cx0, cy0), (cx0 + CELL_W, cy0 + CELL_H)], outline=RULE, width=1)
    d.rounded_rectangle([cx0 + 7, cy0 + 7, cx0 + 33, cy0 + 33], radius=4, fill=colour)
    ICONS[icon](d, cx0 + 20, cy0 + 20, 26)
    d.text((cx0 + 39, cy0 + 13), tag, font=font(SANS_B, 10), fill=colour)
    ty = draw_lines(d, cx0 + 7, cy0 + 40, head, font(SERIF_B, 12), CELL_W - 14,
                    leading=1.08, max_lines=3)
    draw_lines(d, cx0 + 7, ty + 1, summ, font(SANS, 10), CELL_W - 14,
               fill=GREY, leading=1.25, max_lines=3)

# sources box in the 32nd cell
sx0 = M + (31 % 8) * (CELL_W + GAP)
sy0 = GY0 + (31 // 8) * (CELL_H + GAP)
d.rectangle([(sx0, sy0), (sx0 + CELL_W, sy0 + CELL_H)], outline=RULE, width=1)
d.text((sx0 + 8, sy0 + 8), "SOURCES", font=font(SANS_B, 11), fill=RED)
draw_lines(d, sx0 + 8, sy0 + 26,
           "Reuters \u2022 AP \u2022 AFP \u2022 SCMP \u2022 The Hindu \u2022 NYT",
           font(SANS, 10), CELL_W - 16, leading=1.3, max_lines=4)
draw_lines(d, sx0 + 8, sy0 + 82,
           "All stories first reported 25 Nov 2026.",
           font(SANS, 10), CELL_W - 16, fill=GREY, leading=1.3, max_lines=3)

# ---- Footer ----
d.line([(M, 996), (X1, 996)], fill=INK, width=1)
foot = "THE WORLD TODAY  \u2014  Wednesday, 25 November 2026  \u2014  One day. 33 stories. 7 regions."
fw = d.textlength(foot, font=font(SANS, 13))
d.text(((W - fw) / 2, 1004), foot, font=font(SANS, 13), fill=GREY)

img.save(HERE / "entry.png", "PNG", optimize=True)
print("saved entry.png")
