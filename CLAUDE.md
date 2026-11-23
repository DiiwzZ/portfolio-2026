# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal job-application portfolio for **Vuttipat Prapai (Dew)**, targeting two roles:
**Content Creator** (primary emphasis) and **Graphic Designer** (secondary).

**Repositioned 2026-11-23, away from "AI Specialist".** An audit showed the portfolio claimed AI
Specialist loudest while holding the least proof of it — both AI cards had no images, only a GitHub
link — so the claim was dropped rather than propped up. The internship was, in substance, content
production: articles, social graphics, short-form video. The AI tools he used are still listed, as
tools, lower down. Do not re-promote AI to a claimed role without new evidence behind it.

Target deploy is `https://diiwzz.github.io/portfolio-2026/` — GitHub Pages, repo
`DiiwzZ/portfolio-2026`, branch `master`.

**This is a deliberate fork of the old site.** `DiiwzZ/portfolio` still exists, still serves
`https://diiwzz.github.io/portfolio/`, and holds an older version of this page. It is not to be
touched — no pushing, no force-pushing, no adding it as a remote. All work happens in the new repo
so the live site keeps working while this one is rebuilt.

Audience is recruiters, not developers. Every change should be judged by "does this make a hiring
manager trust him more?" — not by code elegance.

## No build system

There is no npm, no bundler, no tests, no linter. `index.html` is the entire application:
HTML + `<style>` + `<script>` inline in one 1,499-line file. Editing it is the whole workflow.

Preview locally:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`. Opening `index.html` via `file://` also works, but relative
image paths behave differently — prefer the server.

Deploy (GitHub Pages rebuilds in 1–2 min):

```bash
git push origin master
```

This repo was `git init`-ed locally on 2026-08-25 with fresh history. Because `portfolio-2026` is a
brand-new empty repo, the first push is an ordinary fast-forward — there is nothing to reconcile and
no reason to force-push.

The three places that hardcode the deploy URL are `og:image` ([index.html:10](index.html:10)) and
the Contact link's `href` and label ([index.html:1335](index.html:1335),
[:1339](index.html:1339)). `pujo-cat_hotel` at [index.html:1224](index.html:1224) is a different
project — leave it alone.

## Architecture

Single file, five sections in this fixed order:

1. **Hero** — name + typing animation cycling job titles
2. **About** — copy + three skill groups (AI & LLMs / Creative Tools / Development)
3. **Experience** — real work; the most important section
4. **Projects** — coursework
5. **Contact**

**Experience is deliberately above Projects.** Internship work is more compelling than
coursework, so recruiters hit it first. Do not reorder.

**Nano Banana lives in Experience, not Projects** — it was built *during* the internship to fix a
real bottleneck (generating graphics one at a time was slow). That framing is the evidence for
"Workflow Optimization" on the job description. Moving it to Projects would demote it to a hobby
project and lose the point.

The JS at the bottom is five independent IIFE-less blocks: typing animation, nav scroll/toggle,
`IntersectionObserver` scroll-reveal, lightbox, and smooth-scroll. Elements opt into reveal
animation with `class="reveal"` plus optional `reveal-delay-1..3`. Images opt into the lightbox
with `class="lightbox-trigger"` and `data-caption`.

## Design system

All colors are CSS variables in `:root`. **Never hardcode a color.** If a new one is genuinely
needed, use `oklch()` tuned to the existing palette.

Two rules govern accent usage:

- `--accent` (teal) marks **the lead role's evidence** — content work. Exactly one Experience card
  carries the accent border and glow: *Content Production — Internship*. Nano Banana used to carry
  it back when AI was the claimed role; it was deliberately demoted to a plain border so the
  highlight follows the positioning rather than contradicting it.
- `--gold` is **only** the featured-project badge

Typography is the system font stack. **Do not switch to a Google Font** — it costs a render-blocking
request for no benefit on a page this small.

Layout is flex/grid with `gap`, never margins for spacing. Write HTML compact; heavy indentation is
not the house style here.

## Content rules

These exist because they were violated before and had to be undone:

- **Never invent experience.** A "Staff Training" entry was previously added and removed because he
  had not actually done it.
- **Never oversell.** Describe what was actually done, at the scale it was actually done.
- **No new emoji** beyond the ones already in `exp-icon`.
- **Scope changes narrowly.** Fix what was asked; do not redesign adjacent sections.

## Image pipeline

Images were compressed on 2026-08-25: 33 MB on disk down to 3.2 MB, and the page went from
29.7 MB to 2.9 MB fully loaded / **123 KB on first paint** (only the hero art loads eagerly;
everything else is `loading="lazy"`).

Rules the working script applied, worth keeping if new images are added:

- **No CMYK.** Three source files were CMYK JPEGs, which browsers render with wrong colours —
  fatal on a design portfolio. Always convert to sRGB.
- **Opaque source → JPEG q85.** Most "PNG" screenshots had an alpha channel carrying no
  information at all.
- **Transparent source → lossy WebP.** Photographic content with alpha is the worst case for PNG
  and there is no `pngquant` on this machine. Only `images/main.webp` (hero) is actually
  referenced; the other WebP files are unused assets.
- **Never blindly quantize.** A 255-colour palette visibly bands gradients and photos. The script
  measured the error and refused it — flat logos passed, the hero and the 3D icons did not.
- Longest side capped at 1600px (the lightbox shows at most ~90vw), animated avatar at 300px.
- Every `<img>` carries `width`/`height` so the browser reserves the box before the file lands.

## Known issues

Audited 2026-08-24; performance and placeholder items fixed 2026-08-25. See `CLAUDE-HANDOFF.md`
for the original TODO list.

**Work Samples: filled 2026-11-23.** The block had been deleted for shipping placeholder copy;
it is now rebuilt from the real internship assets and the numbers in the co-op report.

Source of truth for every figure in that card is the report at
`D:\BUWORK\Year4\present\index.html` (outside this repo). Do not invent or round these numbers.
The raw asset folders the user dropped in — `images/post/` and `images/รวมภาพ/`, 136 MB with
Thai names — are gitignored on purpose; the curated, compressed, ASCII-named set lives in
`images/internship/`. The still-missing piece is public URLs for individual articles, posts and
videos, so nothing in that card links out yet.

**Still open:**

- [index.html:72](index.html:72) — `background: var(--bg)/0;` is invalid CSS, silently dropped.
- **Accessibility:** 19 of 26 images have no `alt`. No `prefers-reduced-motion` despite ~8
  animations.
- `og:description` still says "Graphic Designer & UX/UI Designer" with no mention of AI, so link
  previews sent to recruiters undersell the primary role.

**Dead code:** `.exp-item` was once an accordion; the arrow markup was removed but `.exp-arrow`,
six empty `<div>`s in each `exp-header`, and a misleading `.exp-header:hover` background remain.
`.project-card` sets `cursor:pointer` but is not clickable. `.exp-video` and `.reveal-delay-4` are
unused. The builder **tweaks panel** ([index.html:1445](index.html:1445)–end, ~55 lines) posts to
`window.parent` and should not ship to production.

**Unused assets:** `images/work/C0/` (5 Photoshop cut-outs for the Lay's banner — that card
currently shows no images at all), `images/figma_main.png`, `images/illustrator/AI_logo.png`.

## Waiting on the user

Cannot be completed without information only he has: the three Work Samples entries, a resume PDF
(there is no download button anywhere), and a YouTube link for the After Effects banner — the file
was too large for GitHub, so the card currently says "Available upon request".

## Evidence behind each claim

Audited 2026-11-23. Graded by what a recruiter can actually click or look at.

- **Content Creator** (lead role) — **now the best-evidenced claim on the page.** Filled
  2026-11-23 from the co-op internship report. 704,992+ video views (343K Reels / 362K TikTok),
  24 articles written with 8 published, 11 videos, 101+ graphics, 7 Facebook infographics. The
  three top videos are shown as real platform screenshots with the view counts visible in the
  image, which is stronger than any number typed into the page.
- **Graphic Designer** — strongest evidence. Maginta is real client work installed on a physical
  vending machine (3 photos); plus the animated avatar, Illustrator practice, personal logo.
  The Lay's After Effects card still shows nothing at all.
- **UX/UI Designer** (typing animation only, not a claimed role) — one academic project,
  BedBuddies, but with a working Figma prototype link.
- **Not claimed, though well evidenced:** frontend and full-stack web development — Pujo Cat Hotel
  has a live demo, Classroom Booking is Angular + Node + MySQL + JWT, Nano Banana is Python/Flask
  with a public repo. He was asked whether to add Developer as a third role and chose not to.

All three external proof links were verified working on 2026-11-23: the Pujo Cat Hotel demo, the
batch-image-generator repo, and the Figma prototype.
