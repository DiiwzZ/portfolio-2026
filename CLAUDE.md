# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal job-application portfolio for **Vuttipat Prapai (Dew)**, targeting two roles:
**AI Specialist** (primary emphasis) and **Graphic Designer** (secondary).

Live at `https://diiwzz.github.io/portfolio/` — GitHub Pages, repo `DiiwzZ/portfolio`, branch `master`.

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

**Before the first push:** this repo was `git init`-ed locally on 2026-08-24 and has fresh history
unrelated to whatever is on `DiiwzZ/portfolio`. Pushing will require reconciling with the remote —
check `git remote -v` and the remote's history first. Do not force-push without asking.

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

- `--accent` (teal) marks **anything AI-related** — tags, badges, card borders
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

## Known issues

Audited 2026-08-24. All still open — see `CLAUDE-HANDOFF.md` for the original TODO list.

**Blocking the site's credibility:**

- The **Work Samples** block ([index.html:936](index.html:936)) inside the first Experience card
  still renders placeholder copy — literally `ชื่อบทความ / Article Title`, `— reads`, `รูปบทความ`
  — on the live page. Three slots need real images, titles, URLs, and engagement numbers.
- **29.7 MB of images load eagerly.** No `loading="lazy"`, no `width`/`height` on any of the 27
  `<img>` tags. `images/work/C1/design.jpg` alone is 11.7 MB. This is the single biggest problem
  for a recruiter on mobile.

**Bugs:**

- [index.html:1438](index.html:1438) — `document.querySelector(a.getAttribute('href'))` throws
  `SyntaxError` on the four `href="#"` placeholder links, so `preventDefault()` never runs and the
  page jumps to top.
- [index.html:72](index.html:72) — `background: var(--bg)/0;` is invalid CSS, silently dropped.

**Accessibility:** 19 of 27 images have no `alt`. No `prefers-reduced-motion` despite ~8 animations.
`<html lang="en">` while placeholder copy is Thai.

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

## Job-description coverage

What the portfolio proves today, and the one real gap:

- **AI Specialist** — AI implementation, workflow optimization, prompt engineering, AI ethics/QC,
  and Python all have concrete evidence. **Data Analysis has none.**
- **Graphic Designer** — Illustrator, Photoshop, and print/signage work are covered.
  **SketchUp 3D is absent** and there is nothing to show for it.
