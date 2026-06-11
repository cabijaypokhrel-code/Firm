# Technical SEO & Schema Brief
**Target:** Professional authority + local search (Kathmandu / Nepal) · Lighthouse 90+

---

## 1. JSON-LD Schema — APPLIED ✅

The single `AccountingService` block in `index.html` has been replaced with an
`@graph` containing two linked entities:

- **`Organization`** (`#organization`) — `legalName`, `foundingDate`, **`founder`**
  (Person: CA Bijay Pokhrel, with `sameAs` → LinkedIn), `numberOfEmployees`,
  `memberOf` ICAN. This is the *authority* entity Google's Knowledge Graph builds on.
- **`["ProfessionalService", "AccountingService"]`** (`#service`) — the *local* entity:
  NAP data, `geo` coordinates, `openingHoursSpecification`, `priceRange`, plus:
  - **`knowsAbout`** — 14 expertise topics (Statutory Audit, NFRS, Transfer Pricing,
    NRB Directives, Risk Management, Financial Transparency, …) which maps the firm
    to topical entities for "professional authority" queries.
  - **`areaServed`** — Nepal + Kathmandu, Lalitpur, Bhaktapur for local pack relevance.
  - **`hasOfferCatalog`** — the six services, mirroring the visible services grid
    (schema must always mirror on-page content).

The existing `FAQPage` block was kept — it is valid and well-formed.

**Action still needed by the firm:** verify the `geo` coordinates against the actual
office location, and replace the Unsplash `image` with a real office/team photo at
1200×630 (the same asset should serve `og:image`).

## 2. Render-blocking resources — APPLIED ✅

| Fix | Status |
|---|---|
| Google Fonts CSS loaded with `media="print" onload="this.media='all'"` + `<noscript>` fallback — removes ~300–600 ms of render blocking; `display=swap` already present keeps text visible | ✅ applied |
| Font Awesome (icons are decorative) deferred the same way | ✅ applied |
| `preconnect` to both fonts origins | already present ✓ |

## 3. Heading hierarchy review (current page)

The `<h1>` is good — exactly one, and it carries "Chartered Accountancy & Advisory Firm" + the geo modifier "Nepal's". Issues and keyword opportunities:

| Location | Current | Recommendation |
|---|---|---|
| `h1` (hero) | "Nepal's Trusted Chartered Accountancy & Advisory Firm" | Keep. Optionally append the city for local intent: "…Advisory Firm in Kathmandu". |
| Services `h2` | "Comprehensive Financial & Advisory Services" | Weak — "comprehensive financial" has no search demand. Use **"Audit, Tax & Risk Management Services in Nepal"**. |
| Why-us `h2` | "Precision. Independence. Results." | Pure branding; carries zero keywords. Use **"Why Companies Trust Our Audit & Compliance Team"** (keeps the trust angle, adds *Compliance*). |
| Experience `h2` | "A Decade of Measurable Impact" | Add **"Financial Transparency"**: "A Decade of Measurable Impact in Financial Transparency". |
| Service `h3`s | Good ("Statutory & External Audit", "Tax Advisory & Compliance") | Add one `h3` keyword each where natural: "Internal Audit & **Risk Management** Advisory"; "NRB & Banking **Regulatory Compliance**". |
| Mega-menu & footer `h4`s | Headings inside `<nav>`/`<footer>` ("Assurance", "Services", "Company") | Replace with `<p class="menu-heading">` or `role="heading"` styling — navigation labels shouldn't occupy the document outline. |
| Industries / pillars | `h2 → h4` (skips `h3`) | Promote `.industry-card h4` and `.pillar-item h4` to `h3` (style with classes, not tag selectors). |

**Keyword set to weave into h2/h3 + body copy:** `compliance` → "NRB compliance", "regulatory compliance Nepal", "VAT compliance"; `risk management` → "risk management advisory", "enterprise risk management"; `financial transparency` → "financial transparency and governance", "transparent financial reporting NFRS".

## 4. Prioritized remaining fixes

| P | Fix | Why |
|---|---|---|
| **P0** | Self-host the two font families (woff2 + `font-display: swap`, `<link rel="preload" as="font">` for the 2 critical weights) and trim to ≤ 5 weights total (currently 13 variants are requested) | Largest remaining LCP/FCP lever; removes third-party dependency entirely |
| **P0** | Replace Font Awesome (~80 KB CSS + webfont) with an inline SVG sprite of the ~25 icons actually used | Kills a whole third-party chain; icons currently invisible until FA loads |
| **P1** | Add `width`/`height` (or `aspect-ratio`) to all `<img>` tags | Eliminates CLS from hero/about/insight images |
| **P1** | Serve Unsplash images with explicit `&w=` sized to the rendered box and `srcset`; keep `loading="lazy"` (already present) but add `fetchpriority="high"` + **no** lazy-load on the LCP image | LCP scoring |
| **P1** | Add `<link rel="canonical" href="https://www.bijaypokhrel-associates.com/">` and `og:url`; add `twitter:card` meta | Duplicate-URL hygiene; richer shares |
| **P2** | Move the ~760-line `<style>` block to an external cached stylesheet; inline only the critical above-the-fold subset (~6 KB: tokens, base, navbar, hero) | Repeat-visit caching; smaller HTML |
| **P2** | Fix the heading-outline issues from §3 (nav/footer `h4`s, skipped levels) | Semantic SEO + accessibility tree |
| **P2** | Remove `<meta name="keywords">` | Ignored by Google; signals nothing but dates the site |
| **P3** | Add `sitemap.xml` + `robots.txt` once the multi-page IA (docs/01) ships; one URL per service/industry page | Crawl coverage for the new architecture |
| **P3** | Person schema for each partner on future profile pages (`Person` + `hasCredential`) | Professional authority at the individual level |
