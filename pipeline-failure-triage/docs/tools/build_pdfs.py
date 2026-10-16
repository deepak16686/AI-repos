#!/usr/bin/env python3
"""Build the Pipeline Failure Triage PDFs from the Markdown sources.

Pipeline: Markdown --pandoc--> HTML (+ print.css) --headless Chromium--> PDF.
Requirements: pandoc and a Chromium/Chrome binary (set CHROME to override discovery).

Usage:
    python3 build_pdfs.py            # builds every document into ../pdf/
    python3 build_pdfs.py 01-solution-design
"""
import glob
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
DOCS_DIR = HERE.parent
OUT_DIR = DOCS_DIR / "pdf"

DOCUMENTS = {
    "01-solution-design": ("Pipeline Failure Triage · Complete Solution Design v1.0",
                           "Pipeline Failure Triage: Complete Solution Design"),
    "02-detailed-use-case-specification": ("Pipeline Failure Triage · Detailed Use Case Specification v1.0",
                                           "Pipeline Failure Triage: Detailed Use Case Specification"),
}

TOC_TEMPLATE = "$table-of-contents$\n"


def find_chrome() -> str:
    env = os.environ.get("CHROME")
    if env:
        return env
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        found = shutil.which(name)
        if found:
            return found
    for pattern in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                    "/usr/bin/chromium*", "C:/Program Files/Google/Chrome/Application/chrome.exe"):
        matches = sorted(glob.glob(pattern))
        if matches:
            return matches[-1]
    sys.exit("No Chromium/Chrome found; set the CHROME environment variable.")


def pandoc(args, source: pathlib.Path) -> str:
    cmd = ["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none", "--no-highlight",
           "--number-sections", "--metadata", "title=Pipeline Failure Triage",
           f"--resource-path={DOCS_DIR}"] + args + [str(source)]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def keep_ids_on_one_line(html: str) -> str:
    """Stop short, space-free table cells (IDs such as UC-17.1, AC-1.1, T2.4) from wrapping."""
    def fix(match):
        attrs, inner = match.group(1), match.group(2)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        if 0 < len(text) <= 14 and " " not in text:
            if 'style="' in attrs:
                attrs = attrs.replace('style="', 'style="white-space: nowrap; ', 1)
            else:
                attrs += ' style="white-space: nowrap"'
            return f"<td{attrs}>{inner}</td>"
        return match.group(0)
    return re.sub(r"<td((?:\s[^>]*)?)>((?:(?!</td>).){1,200}?)</td>", fix, html, flags=re.S)


def build(name: str, chrome: str) -> pathlib.Path:
    footer, title = DOCUMENTS[name]
    source = DOCS_DIR / f"{name}.md"
    if not source.exists():
        sys.exit(f"Missing source: {source}")

    body = pandoc([], source)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=HERE) as tpl:
        tpl.write(TOC_TEMPLATE)
        tpl_path = tpl.name
    try:
        toc = pandoc(["--standalone", "--toc", "--toc-depth=2", f"--template={tpl_path}"], source)
    finally:
        os.unlink(tpl_path)

    # Insert the table of contents after the cover, before the first section.
    marker = '<h1 class="unnumbered" id="document-control">'
    nav = f'<nav id="TOC">\n{toc}\n</nav>\n'
    idx = body.find(marker)
    body = body[:idx] + nav + body[idx:] if idx >= 0 else nav + body

    body = keep_ids_on_one_line(body)

    css = (HERE / "print.css").read_text(encoding="utf-8").replace("{{FOOTER_TITLE}}", footer)
    html = (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
            f"<title>{title}</title>\n<style>\n{css}\n</style></head>\n<body>\n{body}\n</body></html>\n")

    html_path = DOCS_DIR / f"{name}.print.html"
    html_path.write_text(html, encoding="utf-8")
    OUT_DIR.mkdir(exist_ok=True)
    pdf_path = OUT_DIR / f"{name}.pdf"
    try:
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                       check=True, capture_output=True, text=True)
    finally:
        html_path.unlink(missing_ok=True)
    return pdf_path


def main() -> None:
    chrome = find_chrome()
    names = sys.argv[1:] or list(DOCUMENTS)
    for name in names:
        if name not in DOCUMENTS:
            sys.exit(f"Unknown document {name!r}; choose from {', '.join(DOCUMENTS)}")
        out = build(name, chrome)
        print(f"built {out.relative_to(DOCS_DIR.parent)}")


if __name__ == "__main__":
    main()
