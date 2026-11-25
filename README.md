# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/gc-cheng/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/gc-cheng/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

The World Today — Wednesday, 25 November 2026. make.fun bounty entry for **news-image-20261125**: sum up the world's news of Wednesday 25 November 2026 in one image.

The entry is a 1024×1024 newspaper front page, **THE WORLD TODAY**, drawn with Python/PIL (`build_image.py`, included here) from the verified news of the day — **33 stories in 7 regions, every story with its own drawn illustration**, plus a world-map locator strip:

- **Lead — China probes a Politburo member:** Shanghai party chief Chen Jining under investigation in a shock anti-graft probe (AP).
- **U.S./China — Huawei guilty in U.S. trial:** a jury convicts the tech giant of conspiracy to steal trade secrets and bank fraud.
- **Europe:** Zelenskiy confirms Ukraine's drone strike on a Russian ship in the Gulf of Finland; NATO to send early-warning aircraft to Poland; Sarkozy faces a corruption trial; a Russian warship is accused of jamming GPS off the UK; Real Madrid rout PSV 5–1; Gukesh holds Sindarov in the world chess championship; Britain sanctions the Houthis.
- **Middle East:** Houthis hit Riyadh's PIF tower (11 hurt); a Hamas security chief is killed in Gaza; Eisenkot clinches his first coalition pact; a U.S. envoy doubts military aid to Israel ends this year; Houthis advance to 60 km from Aden; Iraq seizes Kurdish oilfields; Iran's medicine shortage bites.
- **North America:** Trump awards Rudy Giuliani the Medal of Freedom and pardons the Thanksgiving turkeys; the CIA and ODNI suffer a cyber breach; radar faults ground Chicago flights; the Fort Hood shooter seeks a stay; Shein pays $100M to the FTC; a U.S. soldier admits selling military data to China.
- **Asia-Pacific:** North Korea threatens to shut its Swiss office; Russian jets enter Korea's air defence zone; India urges human oversight of AI weapons at the UN; Xiamen Air orders 50 Boeings; a Philippines impeachment verdict is expected in December.
- **Africa, Latin America, tech:** Senegal gets the AFCON title back; landmine casualties hit a five-year high of 7,000; gunmen hold 25 hostage in Cartagena; a car bomb wounds 23 in Colombia; software flaws pass 100,000 in 2026.

Sources: Reuters, AP, AFP, SCMP, The Hindu, NYT — all stories first reported 25 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the image stored as `entry.png` in this repo and writes it to `/output/entry.png` (`MAKEFUN_OUTPUT_DIR` outside the grader). No network, no timestamps, no randomness — two runs write byte-identical output. The image was drawn with Python/PIL by `build_image.py`, included here for provenance.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=3pf76s6q&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
