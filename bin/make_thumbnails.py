#!/usr/bin/env python3
"""Make publication thumbnails automatically from each paper's Figure 1.

For every entry in _bibliography/papers.bib that has no `preview` yet:
  1. find a PDF: the entry's pdf field, its arXiv id, or an arXiv title search;
  2. find the "Figure 1" (or "Fig. 1") caption in the first pages and crop the
     figure above it; if there is no such caption, take the largest figure on
     the first pages;
  3. fit the crop to the same 2:1 shape as the other thumbnails, save it in
     assets/img/publication_preview/, and add `preview={...}` to the entry.

Papers it can't handle (no PDF, no figure) are listed and skipped. They are
remembered in _bibliography/.thumbnail_skipped.json so later runs don't retry
them; use --retry to try them again.

To replace a thumbnail you don't like, overwrite its image file (same name),
or delete the entry's preview line and run this again.

Usage:
    python3 bin/make_thumbnails.py              # all entries without a preview
    python3 bin/make_thumbnails.py --key Foo2026Bar
    python3 bin/make_thumbnails.py --pdf paper.pdf --key Foo2026Bar
    python3 bin/make_thumbnails.py --dry-run    # report only, change nothing
"""
import argparse
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

try:
    try:
        import pymupdf
    except ImportError:  # older PyMuPDF
        import fitz as pymupdf
    from PIL import Image
except ImportError:
    sys.exit("This script needs PyMuPDF and Pillow. Install them with:\n"
             "    python3 -m pip install --user pymupdf pillow\n"
             "(if pip says the environment is externally managed, add --break-system-packages)")

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_bibliography" / "papers.bib"
SKIPPED = ROOT / "_bibliography" / ".thumbnail_skipped.json"
OUT_DIR = ROOT / "assets" / "img" / "publication_preview"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"

CAPTION_1 = re.compile(r"^\s*(figure|fig\.?)\s*1\s*[.:|\-–—]?(\s|$)", re.I)
CAPTION_ANY = re.compile(r"^\s*(figure|fig\.?)\s*\d+\s*[.:|]", re.I)
SEARCH_PAGES = 10
RENDER_DPI = 220


# ------------------------------------------------------------------ bib

def entries(text):
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        if m.group(1).lower() in ("string", "comment", "preamble"):
            continue
        start = m.start()
        depth, i = 0, text.index("{", start)
        while i < len(text):
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            if depth == 0:
                break
            i += 1
        yield m.group(2), text[start:i + 1]


def field(entry, name):
    m = re.search(r"\b" + name + r"\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", entry, re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def add_preview(text, key, filename):
    m = re.search(r"@\w+\s*\{\s*" + re.escape(key) + r"\s*,[^\n]*\n", text)
    return text[:m.end()] + f"  preview={{{filename}}},\n" + text[m.end():]


# ------------------------------------------------------------------ PDFs

def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def arxiv_by_title(title):
    q = urllib.parse.quote(f'ti:"{re.sub(r"[^A-Za-z0-9 ]", " ", title)}"')
    xml = fetch(f"https://export.arxiv.org/api/query?search_query={q}&max_results=5").decode()
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        t = re.search(r"<title>(.*?)</title>", entry, re.S)
        i = re.search(r"<id>https?://arxiv.org/abs/([^<v]+)", entry)
        if t and i and norm_title(t.group(1)) == norm_title(title):
            return i.group(1)
    return ""


def pdf_urls(entry):
    pdf = field(entry, "pdf")
    arxiv = field(entry, "arxiv")
    if not arxiv:
        m = re.search(r"arXiv:\s*(\d{4}\.\d{4,5})", field(entry, "journal"), re.I)
        arxiv = m.group(1) if m else ""
    if pdf:
        yield pdf.replace("openreview.net/forum?", "openreview.net/pdf?").replace(
            "arxiv.org/abs/", "arxiv.org/pdf/")
    if arxiv:
        yield f"https://arxiv.org/pdf/{arxiv}"
    elif field(entry, "title"):
        try:
            found = arxiv_by_title(field(entry, "title"))
        except Exception:
            found = ""
        if found:
            yield f"https://arxiv.org/pdf/{found}"


def get_pdf(entry):
    for url in pdf_urls(entry):
        try:
            data = fetch(url)
        except Exception:
            continue
        if data[:4] == b"%PDF":
            return data, url
    return None, None


# ------------------------------------------------------------------ figures

def graphics(page):
    """Rectangles of images and of clustered vector drawings on a page."""
    pr = page.rect
    rects = []
    for info in page.get_image_info():
        r = pymupdf.Rect(info["bbox"]) & pr
        if r.width > 20 and r.height > 20:
            rects.append(r)
    try:
        clusters = page.cluster_drawings()
    except Exception:
        clusters = [d["rect"] for d in page.get_drawings()]
    for r in clusters:
        r = pymupdf.Rect(r) & pr
        thin = r.height < 3 or r.width < 3
        if thin or r.width * r.height < 400:
            continue  # rules, underlines, link boxes
        if r.width > 0.9 * pr.width and r.height > 0.9 * pr.height:
            continue  # page frame
        rects.append(r)
    return rects


def text_blocks(page):
    return [(pymupdf.Rect(b[:4]), b[4]) for b in page.get_text("blocks") if b[6] == 0]


def _region(page, cap, left, right, allg, blocks):
    """Graphics above the caption, between left and right, below any text above."""
    ceiling = page.rect.y0
    for rect, text in blocks:
        if rect.y1 <= cap.y0 - 2 and rect.x1 > left + 5 and rect.x0 < right - 5:
            if CAPTION_ANY.match(text) or len(text.split()) > 30:
                ceiling = max(ceiling, rect.y1)
    cands = [r for r in allg if r.y1 <= cap.y0 + 4 and r.y0 >= ceiling - 2
             and r.x0 >= left - 5 and r.x1 <= right + 5]
    if not cands:
        return None
    cands.sort(key=lambda r: cap.y0 - r.y1)
    region = pymupdf.Rect(cands[0])
    if cap.y0 - region.y1 > 80:
        return None
    grew = True
    while grew:
        grew = False
        for r in cands:
            if r not in region and r.y1 >= region.y0 - 30:
                region |= r
                grew = True
    # include labels sitting on the figure's edges
    for rect, text in blocks:
        if (rect.intersects(region + (-8, -8, 8, 8)) and rect.y0 >= ceiling - 1
                and rect.y1 <= cap.y0 + 1 and len(text.split()) <= 30
                and not CAPTION_ANY.match(text) and rect.x0 >= left - 5 and rect.x1 <= right + 5):
            region |= rect
    region.y1 = min(region.y1, cap.y0 - 1)  # never include the caption itself
    return region if region.width > 60 and region.height > 40 else None


def figure_above_caption(page, cap):
    """The figure directly above a caption: full page width or the caption's column."""
    pr = page.rect
    allg = graphics(page)
    blocks = text_blocks(page)
    near = [r for r in allg if -4 <= cap.y0 - r.y1 < 80]
    span = (max(r.x1 for r in near) - min(r.x0 for r in near)) if near else 0
    column = (cap.x0 - 15, cap.x1 + 15)
    if cap.width > 0.55 * pr.width or span > 0.6 * pr.width:
        region = _region(page, cap, pr.x0, pr.x1, allg, blocks)
        if region:
            # a full-width crop must not swallow another caption or a paragraph
            clash = any(rect.intersects(region) and rect != cap and
                        (CAPTION_ANY.match(text) or len(text.split()) > 30)
                        for rect, text in blocks)
            if not clash:
                return region
    if cap.width > 0.55 * pr.width:
        return None
    return _region(page, cap, column[0], column[1], allg, blocks)


def find_figure_1(doc):
    for pno in range(min(SEARCH_PAGES, len(doc))):
        page = doc[pno]
        for rect, text in text_blocks(page):
            if CAPTION_1.match(text):
                region = figure_above_caption(page, rect)
                if region:
                    return pno, region
    return None


def largest_figure(doc):
    best = None
    for pno in range(min(3, len(doc))):
        page = doc[pno]
        for r in graphics(page):
            area = r.width * r.height
            if area > 0.08 * page.rect.width * page.rect.height and (not best or area > best[0]):
                best = (area, pno, r)
    return (best[1], best[2]) if best else None


def crop(doc, pno, region, pad_bottom=6):
    page = doc[pno]
    clip = (region + (-6, -6, 6, pad_bottom)) & page.rect
    pix = page.get_pixmap(clip=clip, dpi=RENDER_DPI, alpha=False)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")


def fit_2_to_1(img, width=800):
    w, h = img.size
    W, H = (w, round(w / 2)) if w / h > 2 else (round(h * 2), h)
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(img, ((W - w) // 2, (H - h) // 2))
    return canvas.resize((width, width // 2), Image.LANCZOS)


def thumbnail_from_pdf(data):
    doc = pymupdf.open(stream=data, filetype="pdf")
    hit = find_figure_1(doc)
    pad_bottom = 0  # the caption sits right below
    if not hit:
        hit, pad_bottom = largest_figure(doc), 6
    if not hit:
        return None, ""
    pno, region = hit
    img = crop(doc, pno, region, pad_bottom)
    return fit_2_to_1(img), f"page {pno + 1}"


# ------------------------------------------------------------------ main

def slug(key):
    return re.sub(r"(?<!^)(?=[A-Z])", "-", key).lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", help="only this bib key")
    ap.add_argument("--pdf", help="use this local PDF (with --key)")
    ap.add_argument("--retry", action="store_true", help="retry papers skipped before")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = BIB.read_text(encoding="utf-8")
    skipped = set(json.loads(SKIPPED.read_text())) if SKIPPED.exists() else set()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    made, failed = [], []

    for key, entry in entries(text):
        if args.key and key != args.key:
            continue
        if re.search(r"\bpreview\s*=", entry) and not args.key:
            continue
        if key in skipped and not (args.retry or args.key):
            continue
        if args.pdf:
            data, src = Path(args.pdf).read_bytes(), args.pdf
        else:
            data, src = get_pdf(entry)
        if not data:
            failed.append((key, "no PDF found"))
            continue
        try:
            img, where = thumbnail_from_pdf(data)
        except Exception as e:
            img, where = None, f"error: {e}"
        if img is None:
            failed.append((key, where or "no figure found"))
            continue
        name = slug(key) + ".jpg"
        if not args.dry_run:
            img.save(OUT_DIR / name, quality=90)
            if not re.search(r"\bpreview\s*=", entry):
                text = add_preview(text, key, name)
        made.append((key, name, where, src))

    if not args.dry_run:
        BIB.write_text(text, encoding="utf-8")
        skipped |= {k for k, _ in failed}
        skipped -= {k for k, *_ in made}
        SKIPPED.write_text(json.dumps(sorted(skipped), indent=2) + "\n")

    for key, name, where, src in made:
        print(f"thumbnail  {key}: {name} ({where} of {src})")
    for key, why in failed:
        print(f"skipped    {key}: {why}")
    if not made and not failed:
        print("Every paper already has a thumbnail.")


if __name__ == "__main__":
    sys.exit(main())
