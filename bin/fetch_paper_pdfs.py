#!/usr/bin/env python3
"""Download the PDFs of papers that don't have a thumbnail yet.

Run on your own computer (it needs normal internet access):

    python3 bin/fetch_paper_pdfs.py

It reads _bibliography/papers.bib, picks every entry without a preview,
downloads its PDF (the pdf field, or arXiv when there is an arXiv id),
and puts them all in ~/Downloads/ai4ai-paper-pdfs.zip, named by bib key.
Upload that zip to Claude to have thumbnails made from the figures.
"""
import os
import re
import sys
import tempfile
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB = os.path.join(ROOT, "_bibliography", "papers.bib")
OUT = os.path.expanduser("~/Downloads/ai4ai-paper-pdfs.zip")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"


def field(entry, name):
    m = re.search(r"\n\s*" + name + r"\s*=\s*\{(.*?)\},?\s*\n", entry, re.S)
    return m.group(1).strip() if m else ""


def candidate_urls(entry):
    urls = []
    pdf = field(entry, "pdf")
    arxiv = field(entry, "arxiv")
    if not arxiv:
        m = re.search(r"arXiv:(\d{4}\.\d{4,5})", field(entry, "journal"))
        arxiv = m.group(1) if m else ""
    if pdf:
        pdf = pdf.replace("openreview.net/forum?", "openreview.net/pdf?")
        pdf = re.sub(r"arxiv\.org/abs/", "arxiv.org/pdf/", pdf)
        urls.append(pdf)
    if arxiv:
        urls.append("https://arxiv.org/pdf/" + arxiv)
    return urls


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if data[:4] == b"%PDF" else None


def main():
    text = open(BIB, encoding="utf-8").read()
    got, missed = [], []
    tmp = tempfile.mkdtemp()
    for entry in re.split(r"\n(?=@)", text):
        m = re.match(r"\s*@(\w+)\{([^,\s]+),", entry)
        if not m or m.group(1).lower() == "string" or "preview=" in entry:
            continue
        key = m.group(2)
        data = None
        for url in candidate_urls(entry):
            try:
                data = fetch(url)
            except Exception:
                data = None
            if data:
                break
        if data:
            with open(os.path.join(tmp, key + ".pdf"), "wb") as f:
                f.write(data)
            got.append(key)
            print("downloaded", key)
        else:
            missed.append(key)
            print("no PDF     ", key)
    if not got:
        sys.exit("Nothing downloaded.")
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for key in got:
            z.write(os.path.join(tmp, key + ".pdf"), key + ".pdf")
    print(f"\n{len(got)} PDFs saved to {OUT}")
    if missed:
        print(f"{len(missed)} without a downloadable PDF: " + ", ".join(missed))


if __name__ == "__main__":
    main()
