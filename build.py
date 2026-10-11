"""Builds the Quiet Income Lab how-to site from articles/*.md into docs/ (served by GitHub Pages).

Article format: first line "# Title", second line "> one-sentence description", then simple markdown
(## headings, paragraphs, - lists, 1. lists, **bold**, [text](url)). No dependencies.
  python build.py            build only
  python build.py --publish  build, commit and push (goes live in about a minute)
"""
import html
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART, OUT = ROOT / "articles", ROOT / "docs"
SITE = "Quiet Income Lab"
TAGLINE = "Practical how-tos for small cleaning businesses and do-it-yourself AI."
STORE = "https://jbman03gmail.gumroad.com"

CSS = """
:root{--ink:#1d1d1f;--mute:#5f6368;--line:#e3e3e3;--bg:#fff;--card:#f6f8f7;--accent:#2f6f4f}
@media (prefers-color-scheme:dark){:root{--ink:#e8e8e8;--mute:#a0a0a0;--line:#333;--bg:#121212;--card:#1c1f1d;--accent:#7cc79f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 -apple-system,"Segoe UI",Roboto,Arial,sans-serif}
main,header,footer{max-width:720px;margin:0 auto;padding:0 16px}header{padding-top:28px}
header a{color:var(--ink);text-decoration:none;font-weight:700}header p{color:var(--mute);margin:2px 0 0}
h1{font-size:2rem;line-height:1.2;margin:28px 0 8px}h2{font-size:1.3rem;margin:28px 0 6px}
a{color:var(--accent)}.desc{color:var(--mute);font-size:1.05rem}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:14px 0}
.card h2{margin:0 0 4px;font-size:1.15rem}.card a{text-decoration:none}.cta{background:var(--card);border-left:4px solid var(--accent);padding:12px 16px;border-radius:6px;margin:28px 0}
blockquote{margin:12px 0;padding:8px 14px;border-left:3px solid var(--line);color:var(--mute)}code{background:var(--card);padding:1px 4px;border-radius:4px}
footer{color:var(--mute);font-size:.9rem;padding:32px 16px 40px;border-top:1px solid var(--line);margin-top:40px}
"""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)


def md(text):
    out, lst = [], None
    for raw in text.splitlines():
        line = raw.rstrip()
        m_ul, m_ol = re.match(r"^- (.*)", line), re.match(r"^\d+\. (.*)", line)
        kind = "ul" if m_ul else "ol" if m_ol else None
        if lst and kind != lst:
            out.append(f"</{lst}>")
            lst = None
        if kind:
            if not lst:
                out.append(f"<{kind}>")
                lst = kind
            out.append(f"<li>{inline((m_ul or m_ol).group(1))}</li>")
        elif line.startswith("<div"):          # call-to-action boxes are written as raw HTML
            out.append(line)
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        elif line:
            out.append(f"<p>{inline(line)}</p>")
    if lst:
        out.append(f"</{lst}>")
    return "\n".join(out)


def page(title, body, desc=""):
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' "
            f"content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title>"
            f"<meta name='description' content='{html.escape(desc)}'><style>{CSS}</style></head><body>"
            f"<header><a href='./'>{SITE}</a><p>{TAGLINE}</p></header><main>{body}</main>"
            f"<footer>Products and setup help: <a href='{STORE}'>{STORE.replace('https://', '')}</a></footer>"
            "</body></html>")


def parse(p):
    lines = p.read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ").strip()
    desc = lines[1][2:].strip() if len(lines) > 1 and lines[1].startswith("> ") else ""
    rest = "\n".join(lines[2:] if desc else lines[1:])
    return title, desc, rest


TOOLS = ROOT / "tools"
BASE_URL = "https://jbman03.github.io/quiet-income-lab/"


def build_tools():
    """tools/<slug>.html = an HTML fragment whose first two lines are '<!-- title: ... -->' and '<!-- desc: ... -->'."""
    cards = []
    for p in sorted(TOOLS.glob("*.html")) if TOOLS.exists() else []:
        src = p.read_text(encoding="utf-8")
        title = re.search(r"<!-- title: (.*?) -->", src).group(1)
        desc = re.search(r"<!-- desc: (.*?) -->", src).group(1)
        (OUT / p.name).write_text(page(title, f"<h1>{html.escape(title)}</h1><p class='desc'>{html.escape(desc)}</p>{src}", desc),
                                  encoding="utf-8")
        cards.append(f"<div class='card'><h2><a href='{p.name}'>{html.escape(title)}</a></h2><div>{html.escape(desc)}</div></div>")
    return cards


def sitemap():
    urls = [BASE_URL] + [BASE_URL + p.name for p in sorted(OUT.glob("*.html")) if p.name != "index.html"]
    (OUT / "sitemap.xml").write_text(
        "<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n"
        + "".join(f"  <url><loc>{u}</loc><lastmod>{date.today()}</lastmod></url>\n" for u in urls) + "</urlset>\n",
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8")


def build():
    OUT.mkdir(exist_ok=True)
    tool_cards = build_tools()
    cards = []
    for p in sorted(ART.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
        title, desc, rest = parse(p)
        slug = p.stem
        (OUT / f"{slug}.html").write_text(page(title, f"<h1>{inline(title)}</h1><p class='desc'>{inline(desc)}</p>{md(rest)}", desc),
                                          encoding="utf-8")
        cards.append(f"<div class='card'><h2><a href='{slug}.html'>{inline(title)}</a></h2><div>{inline(desc)}</div></div>")
    keep = {f"{p.stem}.html" for p in ART.glob("*.md")} | {p.name for p in TOOLS.glob("*.html")} | {"index.html"}
    for stale in OUT.glob("*.html"):                # removed articles disappear from the site too
        if stale.name not in keep:
            stale.unlink()
    tools_html = ("<h1>Free tools</h1>" + "".join(tool_cards)) if tool_cards else ""
    (OUT / "index.html").write_text(page(SITE, tools_html + "<h1>How-to guides</h1>" + "".join(cards), TAGLINE),
                                    encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    sitemap()
    return len(cards) + len(tool_cards)


def publish(msg=None):
    n = build()
    run = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    run("add", "-A")
    c = run("commit", "-m", msg or f"Update site ({date.today()})")
    p = run("push", "-u", "origin", "main")
    ok = p.returncode == 0
    return f"Site rebuilt ({n} articles) and {'pushed - live in about a minute' if ok else 'push FAILED: ' + (p.stderr or c.stderr)[-200:]}"


if __name__ == "__main__":
    print(publish() if "--publish" in sys.argv else f"Built {build()} articles into docs/")
