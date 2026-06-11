#!/usr/bin/env python3
"""Build the Insights section from Markdown posts.

Reads posts/*.md (front matter + a small Markdown subset), then writes:
  - insight-<slug>.html       one article page per published post
  - insights.html             the listing page (all posts, newest first)
  - index.html                the three newest cards, replaced between the
                              INSIGHTS:CARDS:START/END markers

Run from anywhere:  python3 tools/build_insights.py

Front matter keys (--- delimited):
  title, slug, description, category, author (key into AUTHORS),
  date (YYYY-MM-DD), read_time, status (published | coming-soon), summary,
  cta_kicker / cta_heading / cta_sla (optional, override the article CTA band)

Markdown subset supported in the body:
  ## h2 / ### h3, paragraphs, - bullet lists, **bold**, *em*,
  [text](url) links, > note blocks (rendered as the .note callout),
  pipe tables with an optional preceding "[caption]: text" line.
No external dependencies — Python 3 stdlib only.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
SITE_URL = "https://www.bijaypokhrel-associates.com"

AUTHORS = {
    "bijay-pokhrel": {
        "name": "CA Bijay Pokhrel",
        "role": "Managing Partner",
        "monogram": "BP",
        "anchor": "bijay-pokhrel",
        "service": "Audit+%26+Assurance",
        "service_label": "an audit",
        "bio": "Statutory audit, NFRS implementation and banking-sector compliance "
               "under the NRB regulatory framework.",
    },
    "priya-sharma": {
        "name": "CA Priya Sharma",
        "role": "Tax Partner",
        "monogram": "PS",
        "anchor": "priya-sharma",
        "service": "Tax+%26+Compliance",
        "service_label": "a tax",
        "bio": "Corporate income tax, VAT and transfer pricing specialist; 12+ years "
               "advising multinationals and FDI transactions in Nepal.",
    },
    "rajan-thapa": {
        "name": "CA Rajan Thapa",
        "role": "Advisory Partner",
        "monogram": "RT",
        "anchor": "rajan-thapa",
        "service": "Advisory+%26+Consulting",
        "service_label": "an advisory",
        "bio": "Business valuation, M&A due diligence and corporate restructuring "
               "specialist; 10+ years supporting Nepal's leading conglomerates.",
    },
}


# ---------------------------------------------------------------------------
# Markdown subset → HTML
# ---------------------------------------------------------------------------

def inline(text):
    """Inline markdown on an already-HTML-escaped string."""
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # em: single * pairs only (a lone leading asterisk, e.g. a footnote, is left alone)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def render_table(lines, caption):
    head_cells = [c.strip() for c in lines[0].strip().strip("|").split("|")]
    out = ['<table class="rates-table">']
    if caption:
        out.append(f"<caption>{inline(caption)}</caption>")
    out.append("<thead><tr>" +
               "".join(f'<th scope="col">{inline(c)}</th>' for c in head_cells) +
               "</tr></thead>")
    out.append("<tbody>")
    for row in lines[2:]:  # lines[1] is the |---| separator
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        tds = [f"<td>{inline(cells[0])}</td>"]
        tds += [f'<td class="num">{inline(c)}</td>' for c in cells[1:]]
        out.append("<tr>" + "".join(tds) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def md_to_html(body):
    lines = [html.escape(l.rstrip(), quote=False) for l in body.splitlines()]
    out, i, caption = [], 0, None
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"\[caption\]:\s*(.+)", line)
        if m:
            caption = m.group(1)
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
            i += 1
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
            i += 1
        elif line.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].startswith("|"):
                tbl.append(lines[i])
                i += 1
            out.append(render_table(tbl, caption))
            caption = None
        elif line.startswith("&gt; ") or line.startswith("> "):
            note = []
            while i < len(lines) and (lines[i].startswith("&gt; ") or lines[i].startswith("> ")):
                note.append(re.sub(r"^(&gt;|>) ", "", lines[i]))
                i += 1
            out.append('<div class="note">' + inline(" ".join(note)) + "</div>")
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>\n" + "\n".join(items) + "\n</ul>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||- |> |&gt; |\[caption\]:)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Front matter
# ---------------------------------------------------------------------------

def parse_post(path):
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        sys.exit(f"{path}: missing front matter (--- block)")
    meta = {}
    for line in m.group(1).splitlines():
        if line.strip() and ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
    meta["body"] = m.group(2)
    for required in ("title", "slug", "author", "category", "date", "status", "summary"):
        if required not in meta:
            sys.exit(f"{path}: front matter missing '{required}'")
    if meta["author"] not in AUTHORS:
        sys.exit(f"{path}: unknown author '{meta['author']}' (known: {', '.join(AUTHORS)})")
    return meta


# ---------------------------------------------------------------------------
# Shared page chrome
# ---------------------------------------------------------------------------

def header(active_insights=True):
    cur = ' aria-current="page"' if active_insights else ""
    return f"""<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header" id="siteHeader">
    <div class="container site-header__inner">
        <a class="site-header__logo" href="index.html">Bijay Pokhrel &amp; Associates</a>
        <button class="site-header__toggle" id="navToggle" aria-expanded="false" aria-controls="primaryNav">Menu</button>
        <nav class="site-header__nav" id="primaryNav" aria-label="Primary">
            <a href="audit-assurance.html">Audit &amp; Assurance</a>
            <a href="tax-compliance.html">Tax &amp; Compliance</a>
            <a href="advisory.html">Advisory</a>
            <a href="industry-banking.html">Industries</a>
            <a href="insights.html"{cur}>Insights</a>
            <a href="team.html">Team</a>
        </nav>
        <a class="btn btn--primary site-header__cta" href="proposal.html">Request a Proposal</a>
    </div>
</header>"""


FOOTER = """<footer class="site-footer">
    <div class="container">
        <div class="grid">
            <div class="col-4 footer-brand">
                <h2>Bijay Pokhrel &amp; Associates</h2>
                <p>Chartered Accountants &amp; Business Advisors. ICAN member firm —
                   registration details available on request and verifiable with the
                   Institute of Chartered Accountants of Nepal.</p>
            </div>
            <div class="col-3">
                <p class="footer-heading">Services</p>
                <ul>
                    <li><a href="audit-assurance.html">Audit &amp; Assurance</a></li>
                    <li><a href="tax-compliance.html">Tax &amp; Compliance</a></li>
                    <li><a href="advisory.html">Advisory &amp; Consulting</a></li>
                    <li><a href="proposal.html">Request a Proposal</a></li>
                </ul>
            </div>
            <div class="col-2">
                <p class="footer-heading">Firm</p>
                <ul>
                    <li><a href="team.html">Our Team</a></li>
                    <li><a href="industry-banking.html">Industries</a></li>
                    <li><a href="insights.html">Insights</a></li>
                    <li><a href="index.html#methodology">Methodology</a></li>
                </ul>
            </div>
            <div class="col-3">
                <p class="footer-heading">Contact</p>
                <ul>
                    <li><a href="tel:+9779862145832">+977-9862145832</a></li>
                    <li><a href="mailto:info@bijaypokhrel-associates.com">info@bijaypokhrel-associates.com</a></li>
                    <li>Level 4, Corporate Tower,<br>New Baneshwor, Kathmandu 44600</li>
                    <li>Sun–Fri · 9:00–18:00</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Bijay Pokhrel &amp; Associates, Chartered Accountants. All rights reserved.</p>
            <p><a href="https://www.linkedin.com/in/bijay-pokhrel-8b09981b9" rel="noopener" target="_blank">LinkedIn</a></p>
        </div>
    </div>
</footer>

<script src="assets/site.js"></script>"""


def esc(s):
    return html.escape(s, quote=False)


def card(post):
    """Listing/homepage card. Coming-soon posts render as non-linked divs."""
    author = AUTHORS[post["author"]]
    body = f"""    <span class="insight-card__cat">{esc(post["category"])}</span>
    <h3>{esc(post["title"])}</h3>
    <p>{esc(post["summary"])}</p>"""
    if post["status"] == "published":
        meta = f'<span>{esc(author["name"])}</span><span>{esc(post.get("read_time", ""))}</span>'
        return (f'<a class="insight-card col-4" href="insight-{post["slug"]}.html">\n'
                f'{body}\n    <span class="insight-card__meta">{meta}</span>\n</a>')
    meta = f'<span>{esc(author["name"])}</span><span>Coming soon</span>'
    return (f'<div class="insight-card col-4" aria-label="Coming soon">\n'
            f'{body}\n    <span class="insight-card__meta">{meta}</span>\n</div>')


# ---------------------------------------------------------------------------
# Article page
# ---------------------------------------------------------------------------

def article_page(post):
    author = AUTHORS[post["author"]]
    title = esc(post["title"])
    url = f"{SITE_URL}/insight-{post['slug']}.html"
    cta_kicker = esc(post.get("cta_kicker", "Apply It"))
    cta_heading = esc(post.get("cta_heading", "Need this applied to your numbers, not just explained?"))
    cta_sla = esc(post.get("cta_sla", "A senior partner responds within 1 business day"))
    about = json_str_list(post.get("about", ""))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Bijay Pokhrel &amp; Associates</title>
<meta name="description" content="{html.escape(post.get('description', post['summary']))}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": {json_str(post["title"])},
  "author": {{
    "@type": "Person",
    "name": {json_str(author["name"].replace("CA ", ""))},
    "honorificPrefix": "CA",
    "jobTitle": {json_str(author["role"])},
    "worksFor": {{ "@id": "{SITE_URL}/#organization" }}
  }},
  "publisher": {{ "@id": "{SITE_URL}/#organization" }},
  "datePublished": "{post["date"]}",
  "dateModified": "{post.get("modified", post["date"])}",
  "url": "{url}",
  "isPartOf": {{ "@type": "Blog", "url": "{SITE_URL}/insights.html" }},
  "about": [{about}]
}}
</script>
<link rel="stylesheet" href="assets/design-system.css">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>

{header()}

<main id="main">

<section class="page-hero">
    <div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <ol>
                <li><a href="index.html">Home</a></li>
                <li><a href="insights.html">Insights</a></li>
                <li><span aria-current="page">{esc(post.get("crumb", post["title"]))}</span></li>
            </ol>
        </nav>
        <span class="kicker">{esc(post["category"])}</span>
        <h1>{title}</h1>
    </div>
</section>

<section class="section section--compact">
    <div class="container">
        <article class="article">
            <div class="article__meta">
                <span>By {esc(author["name"])} · {esc(author["role"])}</span>
                <span>Published {post["date"]}</span>
                <span>{esc(post.get("read_time", ""))}</span>
            </div>

{md_to_html(post["body"])}

            <div class="author-box">
                <div class="monogram" aria-hidden="true">{author["monogram"]}</div>
                <div>
                    <h2>{esc(author["name"])} — {esc(author["role"])}</h2>
                    <p>{esc(author["bio"])}
                       <a href="team.html#{author["anchor"]}">Full profile</a> ·
                       <a href="proposal.html?service={author["service"]}">Request {author["service_label"]} proposal</a></p>
                </div>
            </div>
        </article>
    </div>
</section>

<section class="section section--inverted cta-band">
    <div class="container">
        <div class="grid">
            <div class="col-8">
                <span class="kicker">{cta_kicker}</span>
                <h2>{cta_heading}</h2>
                <p class="cta-band__sla">{cta_sla}</p>
            </div>
            <div class="col-4 cta-band__actions">
                <a class="btn btn--primary" href="proposal.html?service={author["service"]}">Request a Proposal</a>
            </div>
        </div>
    </div>
</section>

</main>

{FOOTER}
</body>
</html>
"""


def json_str(s):
    import json as _json
    return _json.dumps(s)


def json_str_list(csv):
    return ", ".join(json_str(x.strip()) for x in csv.split(",") if x.strip())


# ---------------------------------------------------------------------------
# Listing page
# ---------------------------------------------------------------------------

def listing_page(posts):
    cards = "\n\n".join(card(p) for p in posts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Insights &amp; Updates | Tax Rates, NFRS, NRB Directives | Bijay Pokhrel &amp; Associates</title>
<meta name="description" content="Practical updates from our partners: Nepal tax rate changes, Finance Act analysis, NFRS implementation guidance, and NRB directive briefings.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE_URL}/insights.html">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Blog",
  "name": "Insights & Updates — Bijay Pokhrel & Associates",
  "url": "{SITE_URL}/insights.html",
  "publisher": {{ "@id": "{SITE_URL}/#organization" }}
}}
</script>
<link rel="stylesheet" href="assets/design-system.css">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>

{header()}

<main id="main">

<section class="page-hero">
    <div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <ol>
                <li><a href="index.html">Home</a></li>
                <li><span aria-current="page">Insights &amp; Updates</span></li>
            </ol>
        </nav>
        <span class="kicker">Knowledge Center</span>
        <h1>Insights &amp; updates from our partners</h1>
        <p class="hero__lead">Tax rate changes, Finance Act analysis, NFRS guidance and NRB directive
           briefings — written by the partners who apply them in practice, not a content team.</p>
    </div>
</section>

<section class="section section--alt">
    <div class="container">
        <div class="grid">

{cards}

        </div>

        <div class="note mt-4">
            <strong>Get updates as they publish.</strong> We brief clients on Finance Act changes and
            NRB directives as they land — <a href="proposal.html">become a client</a> or email
            <a href="mailto:info@bijaypokhrel-associates.com">info@bijaypokhrel-associates.com</a>
            to join the circulation list.
        </div>
    </div>
</section>

<section class="section section--inverted cta-band">
    <div class="container">
        <div class="grid">
            <div class="col-8">
                <span class="kicker">Beyond Reading</span>
                <h2>Need this applied to your numbers, not just explained?</h2>
                <p class="cta-band__sla">A senior partner responds within 1 business day</p>
            </div>
            <div class="col-4 cta-band__actions">
                <a class="btn btn--primary" href="proposal.html">Request a Proposal</a>
            </div>
        </div>
    </div>
</section>

</main>

{FOOTER}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    posts = [parse_post(p) for p in sorted(POSTS_DIR.glob("*.md"))
             if p.name.lower() != "readme.md"]
    if not posts:
        sys.exit("no posts found in posts/")
    # Published first (newest first), then coming-soon
    posts.sort(key=lambda p: (p["status"] != "published", p["date"]), reverse=False)
    published = [p for p in posts if p["status"] == "published"]
    published.sort(key=lambda p: p["date"], reverse=True)
    coming = [p for p in posts if p["status"] != "published"]
    ordered = published + coming

    for post in published:
        out = ROOT / f"insight-{post['slug']}.html"
        out.write_text(article_page(post))
        print(f"wrote {out.name}")

    (ROOT / "insights.html").write_text(listing_page(ordered))
    print("wrote insights.html")

    # Homepage cards: three newest, replaced between markers
    index = ROOT / "index.html"
    src = index.read_text()
    block = ("<!-- INSIGHTS:CARDS:START — generated by tools/build_insights.py, do not edit by hand -->\n"
             + "\n\n".join(card(p) for p in ordered[:3])
             + "\n<!-- INSIGHTS:CARDS:END -->")
    new = re.sub(r"<!-- INSIGHTS:CARDS:START.*?<!-- INSIGHTS:CARDS:END -->", block, src, flags=re.S)
    if new == src and "INSIGHTS:CARDS:START" not in src:
        sys.exit("index.html: INSIGHTS:CARDS markers not found")
    index.write_text(new)
    print("updated index.html cards")


if __name__ == "__main__":
    main()
