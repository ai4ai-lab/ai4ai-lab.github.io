#!/usr/bin/env python3
"""Append new Google Scholar publications to _bibliography/papers.bib.

Existing entries are never modified. A paper is added only if its Scholar
citation id has not been processed before and its title does not match an
entry already in the .bib file. Every processed id is recorded in
_bibliography/.scholar_seen.json, so an auto-added entry you delete by hand
will not come back.

Fetches Scholar directly; run it from your own computer (see bin/scholar_sync_local.sh).
SERPAPI_API_KEY environment variable is set, falls back to SerpApi.

Usage:
  python bin/scholar_sync.py                 # add new papers
  python bin/scholar_sync.py --dry-run       # print what would be added
  python bin/scholar_sync.py --mark-all-seen # record everything on Scholar now
                                             # as seen, add nothing
"""

import argparse
import difflib
import json
import os
import random
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_bibliography" / "papers.bib"
SEEN = ROOT / "_bibliography" / ".scholar_seen.json"
SOCIALS = ROOT / "_data" / "socials.yml"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Venue substring (lowercase) -> abbr, matching the style already in papers.bib.
# First match wins, so more specific patterns come first.
VENUE_ABBR = [
    ("arxiv", "arXiv"),
    ("medrxiv", "medRxiv"),
    ("biorxiv", "bioRxiv"),
    ("international conference on learning representations", "ICLR"),
    ("iclr", "ICLR"),
    ("international conference on machine learning", "ICML"),
    ("icml", "ICML"),
    ("neural information processing systems", "NeurIPS"),
    ("neurips", "NeurIPS"),
    ("artificial intelligence and statistics", "AISTATS"),
    ("aistats", "AISTATS"),
    ("uncertainty in artificial intelligence", "UAI"),
    ("aaai", "AAAI"),
    ("ijcai", "IJCAI"),
    ("transactions on machine learning research", "TMLR"),
    ("journal of machine learning research", "JMLR"),
    ("journal of artificial intelligence research", "JAIR"),
    ("machine learning for healthcare", "MLHC"),
    ("machine learning for health", "ML4H"),
    ("conference on health, inference, and learning", "CHIL"),
    ("amia", "AMIA"),
    ("conference on language modeling", "COLM"),
    ("reinforcement learning conference", "RLC"),
    ("reinforcement learning journal", "RLC"),
    (" rlc", "RLC"),
    ("computer vision and pattern recognition", "CVPR"),
    ("nature communications", "Nat Commun"),
    ("nature medicine", "Nat Med"),
    ("npj digital medicine", "npj Digit Med"),
    ("lancet digital health", "Lancet Digit Health"),
    ("plos one", "PLOS ONE"),
    ("anaesthesia", "Anaesthesia"),
    ("entropy", "Entropy"),
]

FIELD_ORDER = [
    "title", "author", "journal", "booktitle", "volume", "number", "pages",
    "publisher", "year", "abbr", "bibtex_show", "google_scholar_id",
]


# ---------------------------------------------------------------- utilities

def warn(msg, level="warning"):
    """Print to stderr and, on GitHub Actions, as an annotation on the run."""
    print(msg, file=sys.stderr)
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::{level}::{msg}")


def norm_title(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[{}\\]", "", t).lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def bib_escape(s):
    return s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")


def read_scholar_id():
    if os.environ.get("SCHOLAR_ID"):
        return os.environ["SCHOLAR_ID"]
    m = re.search(r"^scholar_userid:\s*([\w-]+)", SOCIALS.read_text(), re.M)
    if not m:
        sys.exit("No scholar_userid in _data/socials.yml and SCHOLAR_ID not set.")
    return m.group(1)


def existing_bib(text):
    """Return (normalised titles, citation keys) of entries in the .bib file."""
    keys = set(re.findall(r"^@\w+\{([^,\s]+),", text, re.M))
    titles = []
    for m in re.finditer(r"\btitle\s*=\s*\{", text, re.I):
        i, depth = m.end(), 1
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        titles.append(norm_title(text[m.end():i - 1]))
    return titles, keys


def matches_existing(title, titles):
    n = norm_title(title)
    if n in titles:
        return True
    return any(difflib.SequenceMatcher(None, n, t).ratio() > 0.92 for t in titles)


def abbr_for(venue):
    v = venue.lower()
    workshop = "workshop" in v
    for pat, ab in VENUE_ABBR:
        if pat in v:
            return f"{ab} Workshop" if workshop and ab not in ("arXiv",) else ab
    return None


def format_authors(raw):
    """'S Parbhoo, FD Velez' -> 'Parbhoo, S and Velez, FD'."""
    out = []
    for a in [x.strip() for x in raw.split(",") if x.strip()]:
        if a in ("...", "…"):
            out.append("others")
            continue
        parts = a.split()
        out.append(a if len(parts) == 1 else f"{parts[-1]}, {' '.join(parts[:-1])}")
    return " and ".join(out)


def make_key(authors, year, title, used):
    first = authors.split(" and ")[0].split(",")[0]
    first = re.sub(r"[^A-Za-z]", "", unicodedata.normalize("NFKD", first)) or "Anon"
    stop = {"a", "an", "the", "on", "of", "for", "to", "in", "and", "with", "towards"}
    words = [w for w in re.findall(r"[A-Za-z]+", title) if w.lower() not in stop]
    base = f"{first}{year}{words[0].capitalize() if words else ''}"
    key, n = base, 1
    while key in used:
        n += 1
        key = f"{base}{chr(ord('a') + n - 2)}"
    used.add(key)
    return key


# ---------------------------------------------------------------- fetching

class Blocked(Exception):
    pass


class DirectScholar:
    BASE = "https://scholar.google.com/citations"

    def __init__(self, user):
        self.user = user
        self.s = requests.Session()
        self.s.headers.update(HEADERS)

    def _get(self, params):
        r = self.s.get(self.BASE, params=params, timeout=30)
        if r.status_code in (403, 429) or "gs_captcha" in r.text or "unusual traffic" in r.text:
            raise Blocked(f"Scholar blocked the request (HTTP {r.status_code})")
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")

    def list_articles(self):
        out, start = [], 0
        while True:
            soup = self._get({"user": self.user, "hl": "en", "cstart": start,
                              "pagesize": 100, "sortby": "pubdate"})
            rows = soup.select("tr.gsc_a_tr")
            for row in rows:
                a = row.select_one("a.gsc_a_at")
                if not a:
                    continue
                href = a.get("href") or a.get("data-href") or ""
                m = re.search(r"citation_for_view=[\w-]+:([\w-]+)", href)
                grays = row.select("div.gs_gray")
                year = row.select_one(".gsc_a_y span")
                out.append({
                    "id": m.group(1) if m else None,
                    "title": a.get_text(strip=True),
                    "authors": grays[0].get_text(strip=True) if grays else "",
                    "venue": grays[1].get_text(" ", strip=True) if len(grays) > 1 else "",
                    "year": year.get_text(strip=True) if year else "",
                })
            more = soup.select_one("#gsc_bpf_more")
            if len(rows) < 100 or (more is not None and more.has_attr("disabled")):
                return out
            start += 100
            time.sleep(random.uniform(2, 4))

    def details(self, cid):
        soup = self._get({"view_op": "view_citation", "hl": "en", "user": self.user,
                          "citation_for_view": f"{self.user}:{cid}"})
        fields = {}
        for row in soup.select("#gsc_oci_table .gs_scl"):
            k = row.select_one(".gsc_oci_field")
            v = row.select_one(".gsc_oci_value")
            if k and v:
                fields[k.get_text(strip=True).lower()] = v.get_text(" ", strip=True)
        return fields


class SerpApiScholar:
    BASE = "https://serpapi.com/search.json"

    def __init__(self, user, key):
        self.user, self.key = user, key

    def _get(self, **params):
        params.update(engine="google_scholar_author", author_id=self.user,
                      api_key=self.key, hl="en")
        r = requests.get(self.BASE, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise RuntimeError(f"SerpApi: {data['error']}")
        return data

    def list_articles(self):
        out, start = [], 0
        while True:
            arts = self._get(num=100, start=start, sort="pubdate").get("articles", [])
            for a in arts:
                cid = a.get("citation_id", "")
                out.append({
                    "id": cid.split(":")[-1] or None,
                    "title": a.get("title", ""),
                    "authors": a.get("authors", ""),
                    "venue": a.get("publication", ""),
                    "year": str(a.get("year", "")),
                })
            if len(arts) < 100:
                return out
            start += 100

    def details(self, cid):
        c = self._get(view_op="view_citation",
                      citation_id=f"{self.user}:{cid}").get("citation", {})
        mapping = {"authors": "authors", "publication_date": "publication date",
                   "journal": "journal", "conference": "conference", "book": "book",
                   "volume": "volume", "issue": "issue", "pages": "pages",
                   "publisher": "publisher"}
        return {v: str(c[k]) for k, v in mapping.items() if c.get(k)}


# ---------------------------------------------------------------- entries

def build_entry(item, info, used_keys):
    title = item["title"]
    authors = format_authors(info.get("authors") or item["authors"])
    journal = info.get("journal")
    conf = info.get("conference") or info.get("book")
    venue_text = journal or conf or item["venue"]
    # Scholar sometimes omits the year; fall back to the date field, then the venue name.
    year = item["year"]
    for text in (info.get("publication date", ""), venue_text):
        if not year:
            year = (re.findall(r"(?:19|20)\d{2}", text) or [""])[0]

    is_preprint = bool(re.search(r"arxiv|medrxiv|biorxiv|preprint", venue_text, re.I))
    if conf and not journal:
        etype, venue_field = "inproceedings", ("booktitle", conf)
    else:
        venue = journal or re.sub(r",?\s*\d{4}\s*$", "", item["venue"]).strip()
        etype, venue_field = "article", ("journal", venue)

    f = {"title": title, "author": authors, "year": year}
    if venue_field[1]:
        f[venue_field[0]] = venue_field[1]
    if not is_preprint:
        for src, dst in (("volume", "volume"), ("issue", "number"),
                         ("pages", "pages"), ("publisher", "publisher")):
            if info.get(src):
                f[dst] = info[src].replace("-", "--") if dst == "pages" else info[src]
    ab = abbr_for(venue_text)
    if ab:
        f["abbr"] = ab
    f["bibtex_show"] = "true"
    if item["id"]:
        f["google_scholar_id"] = item["id"]

    key = make_key(authors, year or "XXXX", title, used_keys)
    lines = [f"@{etype}{{{key},"]
    for k in FIELD_ORDER:
        if f.get(k):
            v = f[k] if k in ("bibtex_show",) else bib_escape(f[k])
            lines.append(f"  {k}={{{v}}},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--mark-all-seen", action="store_true")
    ap.add_argument("--max-new", type=int, default=20,
                    help="cap on papers added per run (detail pages are rate-limited)")
    args = ap.parse_args()

    user = read_scholar_id()
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    bib_text = BIB.read_text()
    titles, keys = existing_bib(bib_text)

    sources = [DirectScholar(user)]
    if os.environ.get("SERPAPI_API_KEY"):
        sources.append(SerpApiScholar(user, os.environ["SERPAPI_API_KEY"]))

    src, items, last_err = None, None, None
    for s in sources:
        try:
            items = s.list_articles()
            src = s
            break
        except (Blocked, requests.RequestException, RuntimeError) as e:
            last_err = e
            warn(f"{type(s).__name__}: {e}")
    if items is None:
        warn(f"Could not read the Scholar profile: {last_err}", "error")
        sys.exit(1)
    print(f"{len(items)} items on Scholar profile {user} (via {type(src).__name__})")

    new, newly_seen = [], set()
    for it in items:
        if not it["id"] or it["id"] in seen:
            continue
        if args.mark_all_seen or matches_existing(it["title"], titles):
            newly_seen.add(it["id"])
            continue
        new.append(it)

    if len(new) > args.max_new:
        print(f"{len(new)} new papers; adding the {args.max_new} most recent this run")
        new = new[: args.max_new]

    entries = []
    for i, it in enumerate(new):
        try:
            info = src.details(it["id"])
        except Blocked as e:
            warn(f"Stopped fetching details: {e}. Remaining papers will be added next run.")
            break
        except Exception as e:  # keep going with listing data only
            warn(f"Details failed for '{it['title']}': {e}")
            info = {}
        entries.append(build_entry(it, info, keys))
        titles.append(norm_title(it["title"]))
        newly_seen.add(it["id"])
        if isinstance(src, DirectScholar) and i < len(new) - 1:
            time.sleep(random.uniform(3, 7))

    for e in entries:
        print("\n" + e)
    print(f"\n{len(entries)} new entries; {len(newly_seen)} ids newly marked as seen")

    if args.dry_run:
        return
    if entries:
        # Insert after the @string block so new papers sit at the top of the file.
        m = re.search(r"^@(?!string)\w+\{", bib_text, re.M | re.I)
        pos = m.start() if m else len(bib_text)
        block = "\n\n".join(entries) + "\n\n"
        BIB.write_text(bib_text[:pos] + block + bib_text[pos:])
    if newly_seen:
        SEEN.write_text(json.dumps(sorted(seen | newly_seen), indent=2) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        warn(f"Scholar sync crashed: {type(e).__name__}: {e}", "error")
        raise
