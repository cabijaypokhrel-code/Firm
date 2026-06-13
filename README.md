# Bijay Pokhrel & Associates — Website

Static website for **Bijay Pokhrel & Associates, Chartered Accountants**, Kathmandu, Nepal.  
Plain HTML + CSS + vanilla JavaScript. No build step, no npm, no framework.

---

## What this site is

A professional lead-generation website for a Chartered Accountancy firm offering audit & assurance, tax & compliance, and advisory services. Pages:

| File | URL |
|---|---|
| `index.html` | Homepage |
| `audit-assurance.html` | Audit & Assurance service page |
| `tax-compliance.html` | Tax & Compliance service page |
| `advisory.html` | Advisory & Consulting service page |
| `industry-banking.html` | Banking & Finance industry page |
| `team.html` | Partner profiles |
| `proposal.html` | Multi-step proposal request form |

CSS lives in `assets/design-system.css` (tokens) and `assets/site.css` (compositions).  
Shared JavaScript is in `assets/site.js` (mobile nav + sticky header).

---

## How to edit

Open any `.html` file in a text editor. The site uses no templating — header, footer and nav appear in each file. If you update the phone number or address, update it in every file.

**Key things to customise before launch:**

1. **Domain** — search and replace `bijaypokhrel-associates.com` with your real domain across all files.
2. **Phone number** — currently `+977-9862145832`. Update in `index.html`, all service pages, `proposal.html`, and `assets/site.js` if referenced.
3. **Email** — `info@bijaypokhrel-associates.com`. Update wherever it appears.
4. **Address** — "Level 4, Corporate Tower, New Baneshwor, Kathmandu 44600". Update in all footers and `index.html` schema.
5. **LinkedIn URL** — update `sameAs` in schema and footer links.
6. **ICAN membership numbers** — marked as `ICAN Membership No. XXXXX` in team.html. Add real numbers.
7. **Proposal form endpoint** — see section below.

---

## How to connect the proposal form

The proposal form (`proposal.html`) submits to **Formspree**, which emails you every submission.

### Steps

1. Go to [https://formspree.io](https://formspree.io) and create a free account.
2. Create a new form — set the notification email to your firm's address.
3. Copy your form ID (it looks like `xabcdefg`) from the endpoint URL.
4. Open `proposal.html` and find this line near the top of the `<script>` block:

```js
var FORMSPREE_ENDPOINT = 'https://formspree.io/f/YOUR_FORM_ID';
```

5. Replace `YOUR_FORM_ID` with your real form ID, e.g.:

```js
var FORMSPREE_ENDPOINT = 'https://formspree.io/f/xabcdefg';
```

That is all. No server required.

**Alternative: Netlify Forms**  
If you deploy on Netlify, you can use Netlify's built-in form handling instead:

1. Add `netlify` attribute to the `<form>` tag: `<form id="proposalForm" name="proposal" netlify novalidate>`
2. Add a hidden `<input type="hidden" name="form-name" value="proposal">` inside the form.
3. In the JS submit handler, change the fetch call to POST to `'/'` with `Content-Type: application/x-www-form-urlencoded` and the form data encoded accordingly, or simply remove the fetch and allow native form submission after validation (you will lose the in-page success state — the form will redirect to Netlify's thank-you page unless you set `action="/thank-you"` and create a thank-you page).

The Formspree approach (already wired) is simpler and works on any host.

---

## How to deploy

### GitHub Pages (free)

1. Push the repo to GitHub.
2. Go to **Settings → Pages** → set Source to `main` branch, root folder.
3. Your site will be live at `https://yourusername.github.io/repo-name/`.
4. To use a custom domain, add a `CNAME` file containing your domain (e.g. `www.bijaypokhrel-associates.com`) and configure your DNS provider to point the domain to GitHub Pages.

### Netlify (recommended — free tier)

1. Push the repo to GitHub (or GitLab / Bitbucket).
2. Go to [https://app.netlify.com](https://app.netlify.com) → **Add new site → Import an existing project**.
3. Select your repo. Build command: *(leave blank)*. Publish directory: `.` (root).
4. Deploy. Netlify picks up the `_redirects` file automatically.
5. Under **Domain management**, add your custom domain and follow the DNS instructions.
6. Free SSL is provisioned automatically.

### Vercel (free tier)

1. Push the repo to GitHub.
2. Go to [https://vercel.com](https://vercel.com) → **New Project → Import Git Repository**.
3. Framework preset: **Other**. Root directory: `.`. No build command.
4. Deploy. Add your domain under **Settings → Domains**.

---

## WhatsApp direct-chat link

The footer and proposal page contain a WhatsApp link: `https://wa.me/9779862145832`  
Replace `9779862145832` with the firm's WhatsApp-enabled number (country code + number, no `+`).

---

## Updating the sitemap

`sitemap.xml` lists all pages with a `<lastmod>` date. Update the dates whenever you make significant content changes, then re-deploy.

---

## Local preview

Open any `.html` file directly in a browser. Everything works from `file://` — no local server needed.  
If you want a local server: `python3 -m http.server 8000` in the repo root, then visit `http://localhost:8000`.
