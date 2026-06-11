# Publishing an insight

1. Copy an existing `.md` file in this folder (use `2026-06-11-tax-rates.md`
   as the reference — it exercises every feature).
2. Fill in the front matter. `status: coming-soon` shows a non-linked teaser
   card; `status: published` generates the article page.
3. Write the body in Markdown: `##`/`###` headings, paragraphs, `-` lists,
   `**bold**`, `*italics*`, `[links](url)`, `> ` blocks for the highlighted
   note callout, and pipe tables (put `[caption]: My caption` on the line
   above a table).
4. Run `python3 tools/build_insights.py` from the repo root. It regenerates
   the article pages, `insights.html`, and the three homepage cards.
5. Review, commit, push.

Authors are defined in `tools/build_insights.py` (`AUTHORS`) — add new
people there once, and every page picks them up.
