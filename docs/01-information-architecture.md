# Information Architecture & Trust-Signal Brief
**Firm:** Bijay Pokhrel & Associates, Chartered Accountants
**Prepared by:** UX Architecture review of the current single-page site (`index.html`)
**Goal:** Maximize "Trust Signals" for a regulated professional-services buyer and convert cold visitors into proposal requests.

---

## 1. Audit of the current structure

The current site is a single page with this section order:

> Hero → Credentials Ribbon → About → Services → Why Us → Industries → Experience Counters → Clients → Affiliations → Case Studies → Insights → Team → Testimonials → CTA Banner → Contact

**What works:** strong credential density (ICAN/NRB/SEBON), partner-led messaging, case studies with Challenge/Solution/Result structure.

**Structural problems:**

1. **Service overlap.** The mega-menu has four columns (Assurance, Tax Advisory, NFRS & Reporting, Advisory) but the services grid has six cards that cut across them (e.g., "NRB & Banking Compliance" is both assurance and advisory; NFRS appears in two places). A buyer can't tell which practice owns their problem.
2. **No dedicated lead-capture path.** Every CTA points at one generic `#contact` form. A statutory-audit RFP and a "quick tax question" land in the same funnel, which depresses proposal-quality leads.
3. **Trust signals are scattered, not sequenced.** Affiliations appear *after* clients and counters; testimonials appear *after* the team. There is no deliberate cold-visitor journey.
4. **Team cards bury credentials.** Certifications (ICAN, ACCA, CA India) live inside free-text paragraphs instead of scannable, verifiable badges.

---

## 2. Service categorization — the "Independence Rule"

Split services by **the nature of the engagement obligation**, not by topic. This eliminates overlap because every service has exactly one home:

| Pillar | Rule of inclusion | Services |
|---|---|---|
| **Audit & Assurance** | Anything requiring statutory **independence** and resulting in a signed opinion | Statutory/External Audit · Internal Audit · Tax Audit · Special Purpose Audit · Agreed-Upon Procedures |
| **Tax & Compliance** | Recurring **obligations with regulatory deadlines** | Corporate Income Tax · VAT & TDS Compliance · Transfer Pricing · Tax Litigation & IRD Representation · Tax Health-Checks |
| **Advisory & Consulting** | **Discretionary, project-based** engagements that improve the business | NFRS Implementation & Reporting · NRB/Banking Regulatory Advisory · Business Valuation · M&A Due Diligence · Risk & Internal Controls Advisory · Company Secretarial |

Resolution of the current ambiguities:

- **NFRS** → Advisory (it is a transformation project, not an opinion). The *audit of* NFRS statements stays in Assurance. Cross-link the two pages.
- **Internal Audit** → Assurance when outsourced as the internal audit function (independence applies); the *design* of risk frameworks → Advisory.
- **NRB & Banking Compliance** → Advisory, with a "Bank Statutory Audit" cross-link into Assurance.

This split also protects the firm ethically: it visually communicates that audit independence is firewalled from consulting — itself a trust signal for boards and regulators.

---

## 3. Sitemap (target multi-page structure)

```
/
├── /audit-assurance/
│   ├── /statutory-audit/
│   ├── /internal-audit/
│   ├── /tax-audit/
│   └── /special-purpose-audit/
├── /tax-compliance/
│   ├── /corporate-tax/
│   ├── /vat-tds-compliance/
│   ├── /transfer-pricing/
│   └── /tax-litigation/
├── /advisory/
│   ├── /nfrs-implementation/
│   ├── /nrb-banking-compliance/
│   ├── /valuation-due-diligence/
│   └── /risk-controls/
├── /industries/
│   ├── /banking-financial-institutions/
│   ├── /insurance/
│   ├── /manufacturing/
│   ├── /hydropower-energy/
│   ├── /ngo-ingo/
│   └── /... (one page per sector with: regulations we cover,
│              representative engagements, relevant partner, sector CTA)
├── /about/
│   ├── /our-firm/            (history, methodology, quality control)
│   ├── /team/                (partner index)
│   │   └── /team/{partner-slug}/   (full profile — template in §5)
│   └── /credentials/         (ICAN, NRB, SEBON, ACCA — with registration
│                              numbers and links to public registers)
├── /case-studies/
│   └── /case-studies/{slug}/
├── /insights/
│   └── /insights/{slug}/
├── /request-a-proposal/      ← dedicated lead-capture page (see proposal.html)
└── /contact/                 (general enquiries only — kept separate from RFPs)
```

**Navigation:** `Audit & Assurance · Tax · Advisory · Industries · Insights · About` + persistent gold **"Request a Proposal"** button in the header. Contact moves to the utility/footer level; the proposal CTA is the primary conversion action.

---

## 4. The Trust Funnel — cold visitor → proposal request

Professional-services buyers don't convert on features; they convert when perceived risk drops below perceived need. The journey is engineered to lower risk at each step:

```
Stage 1: RELEVANCE      "They know my industry"
   Industry Expertise page (e.g., /industries/banking/)
   — names the exact regulations (NRB Unified Directives, NFRS 9 ECL)
   — entry point from search, insights articles, or homepage industry grid
        │
        ▼
Stage 2: PROOF          "They've solved my exact problem"
   Inline case study on the industry page (Challenge → Solution → Result)
   with quantified outcome ("zero audit findings", "3 weeks early")
        │
        ▼
Stage 3: ACCOUNTABILITY "I know who would sign my engagement"
   "Your engagement partner" block: photo, name, credential badges,
   link to full partner profile. A named human is the strongest
   de-risking signal in audit selection.
        │
        ▼
Stage 4: VERIFIABILITY  "I can check their license"
   Credential strip: ICAN membership no., NRB/SEBON approval —
   linked to the public registers where possible.
        │
        ▼
Stage 5: LOW-FRICTION ASK
   Sector-specific CTA: "Request a proposal for your bank's
   statutory audit" → /request-a-proposal/ with the industry and
   service pre-selected (query param), multi-step form (3 short steps,
   contact details LAST), and an explicit response-time promise
   ("a partner responds within 1 business day").
```

**Rules:** every industry page contains stages 2–5 *on the page* (no dead ends); the proposal form never asks for information the firm doesn't need to scope a fee; the thank-you state restates the response-time SLA — reliability is the product.

---

## 5. Partner Profile — structural template

```html
<article class="partner-profile" itemscope itemtype="https://schema.org/Person">
  <!-- 1. IDENTITY BAND -->
  <header>
    <img>                                   <!-- professional photo, not stock -->
    <h1 itemprop="name">CA Bijay Pokhrel</h1>
    <p class="partner-role" itemprop="jobTitle">Managing Partner</p>
    <ul class="credential-badges">          <!-- scannable, verifiable -->
      <li>ICAN · CA, Membership No. XXXX <a>verify ↗</a></li>
      <li>NRB-Approved Auditor (Class A BFIs)</li>
      <li>DipIFR / ACCA (if applicable)</li>
    </ul>
  </header>

  <!-- 2. INDUSTRY EXPERIENCE MATRIX -->
  <section class="partner-sectors">        <!-- sector + depth, not adjectives -->
    Banking & Financial Institutions — 12 statutory audits, NFRS 9 ECL
    Hydropower — 6 project financings supported
    <!-- each row links to the matching /industries/ page -->
  </section>

  <!-- 3. SIGNATURE ENGAGEMENTS (anonymized) -->
  <section class="partner-engagements">    <!-- 2–3 Challenge→Result bullets -->

  <!-- 4. PROFESSIONAL ACTIVITY -->
  <section>                                  <!-- speaking, ICAN committees,
                                                published insights (auto-list
                                                their /insights/ articles) -->

  <!-- 5. DIRECT CONTACT -->
  <footer>
    LinkedIn (itemprop="sameAs") · firm email ·
    CTA: "Request a proposal — engagements led by CA Pokhrel"
  </footer>
</article>
```

**Why this order:** credentials before narrative (buyers verify first, read second); industry matrix uses *counts* not adjectives (auditable claims); the profile ends with the same proposal CTA so the team page is a funnel stage, not a dead end. Fix on the current site: CA Bijay Pokhrel's card says "5+ years" while the hero claims a 10-year-old firm — credential claims must be consistent everywhere or every other trust signal is discounted.

---

## 6. Homepage technical brief — section order and the "Why"

| # | Section | Why it sits here |
|---|---|---|
| 1 | **Hero** — positioning + stats bar | The 4-stat bar (years, clients, retention, professionals) belongs in the first viewport: numbers anchor credibility before any marketing copy is read. Primary CTA = "Request a Proposal", secondary = "Our Services". |
| 2 | **Credentials ribbon** (ICAN/NRB/SEBON) | Regulatory approval is the *license to be considered at all* — it must appear before services so everything after is read as "approved firm says…", not "vendor says…". |
| 3 | **Services — three pillars** | Now that the visitor trusts the license, route them by need. Three pillar cards (not six overlapping ones), each linking to its hub page. |
| 4 | **Industry expertise grid** | The funnel entry point (§4 Stage 1). Each tile links to its industry page. Placed directly after services because sector relevance, not service breadth, is what shortlists a firm. |
| 5 | **Featured case study** (one, not three) | Proof immediately after relevance. One strong quantified story outperforms a wall of three; the rest live at /case-studies/. |
| 6 | **Methodology / Why Us** | Process transparency (the 5-step engagement model) answers "what is it like to work with you" — the question right before contact. |
| 7 | **Partners strip** | Faces + credential badges, linking to full profiles. Accountability comes late in the page because it's the *closer*, not the opener. |
| 8 | **Testimonial band** (with client name, role, sector) | Third-party voice placed adjacent to the final CTA — the last objection-handler. |
| 9 | **Proposal CTA banner** | Single conversion action with the response-time SLA stated ("a partner responds within 1 business day"). |
| 10 | **Footer** | Full sitemap, registration numbers, privacy/terms — the "fine print" trust layer regulators and procurement teams check. |

**Removed/demoted from the current homepage:** Clients wall with placeholder names (fabricated-looking logos *damage* trust — only use real, permissioned client names, else replace with sector counts), Insights grid (moves to /insights/, surfaced contextually on service pages), duplicate counter section (merge into hero stats).
