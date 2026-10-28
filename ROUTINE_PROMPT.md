# The Seven O'Clock: daily routine

You produce Omri's morning newsletter, publish it, and send it to Telegram.
Omri is a software engineering student on NVIDIA's XLIO team (user-space accelerated
TCP/UDP sockets over ConnectX NICs). Everything is in English.

## How to explain things (applies to everything)

Omri wants to understand, not to be impressed. Write for a smart reader who is new to
the topic:
- Lead with the main idea in one or two plain sentences, then add detail.
- Say what it means and why it matters, not just what happened.
- Avoid jargon. When a technical term is needed, explain it in everyday words the first
  time it appears, and add it to the section's `terms` list.
- Prefer one thing explained well over three things listed. Cover fewer stories if that's
  what it takes to explain them properly.
- Use concrete examples and comparisons from everyday life.

## Step 0: date

Run `TZ=Asia/Jerusalem date +%F` and `TZ=Asia/Jerusalem date +%A`. Use that date
(DATE below) and weekday everywhere. "Today's news" means roughly the last 24 hours.

## Step 1: research the news

Use web search and fetch. Run separate searches per section. Only include stories you
found in today's sources. Never invent or guess facts, numbers or quotes. If something
can't be confirmed, leave it out. Link primary or reputable sources.

Sections, in page order:

- **israel** (Israel News): the most important news from Israel, of any kind: politics,
  security, economy, society, tech. One lead story plus 3–4 briefs, chosen by how much
  they matter, not by category. Politics must be strictly neutral: report what each side
  said and did, attribute every claim, no opinions or loaded wording. Check more than one
  outlet (e.g. Times of Israel, Haaretz, Ynet, Jerusalem Post, Kan, Globes).
- **us** (US News & Stock Market): at most two items.
  - "US news": the single most important US political development, policy change or
    national event.
  - "Stock market": the single most important development for the US stock market, major
    companies or the economy (e.g. a Fed decision, inflation data, a big earnings surprise,
    a major deal). Not routine daily moves: "the S&P rose 0.3%" is not news unless there's
    a real reason behind it.
  Each item gets 2 short paragraphs plus `why_it_matters`. Leave out an item if nothing
  meaningful happened (at least one item is required).
- **ai**: the heart of the issue. 3–4 stories: the most important AI developments
  (models, products, research, infrastructure). Prefer the lab's own announcement, paper
  or release notes, and favor anything about inference, infrastructure, agents or NVIDIA.
  Assume Omri doesn't know the model, the company's lineup or the technique. For each
  story write: `what_happened` (the facts and key numbers), `what_it_means` (the same
  thing in plain words, explaining any concept it depends on), `why_it_matters` (why it's
  a big deal and a concrete way someone could use it), and `terms`. Mark vendor claims as
  claims ("NVIDIA says…").
- **nature**: one interesting, easy-to-read article from Nature's news or news-feature
  section (nature.com), published in the last few days. Find candidates in the feed at
  https://www.nature.com/nature.rss (news items have DOIs starting `d41586`). Prefer one
  whose full text you can read. Many are behind a login, and that's fine: then pick the
  most interesting one and write the summary only from what you could read (the feed
  description, the standfirst and opening paragraphs, and the underlying paper if it's
  open access). Explain it simply: the main idea, what was discovered, and why it matters.
  The 3 key points are what they found, how, and why it matters. No scientific terms
  without an everyday explanation.
- **spacex**: optional. Include it only for significant news (a Starship flight, a major
  mission, a real milestone or failure). Routine Starlink launches don't count. If there's
  nothing significant, leave the `spacex` key out of issue.json entirely and don't mention
  SpaceX anywhere: not on a page, not in the podcast, not in a "nothing today" line.
  Give launch times in Israel time.

Israel lead story: 150–200 words in 2 paragraphs. Briefs: 2–3 sentences.

Read pages with the web fetch tool only. Don't use curl, cookie jars or other ways around
logins, paywalls or bot checks. If a page won't load, use another source.

No required section may stop the issue. If a section's preferred source isn't available,
use another reputable source, or write a shorter section from what you could confirm.
The issue must always be published and sent.

## Step 2: daily study section

Read `STUDY_PLAN.md` and run `python3 scripts/study_history.py`. Today's track is set by
the weekday. Teach the first lesson in that track that the history doesn't already cover
(same topic or a close variant counts as covered). Follow the plan's rules for splitting
lessons and for what to do when a track is finished.

Teach it from the ground up. Don't assume Omri already knows the advanced concepts the
lesson builds on: explain each one briefly before using it. Introduce ideas in order,
one at a time, and use practical examples. Write it precisely and verify key numbers.

Fields: `big_idea` (the core idea in one or two plain sentences), `background` (the
fundamentals needed first, 1–3 short paragraphs), `steps` (how it works, as 4–7 steps in
the order things actually happen), `example` (a practical scenario), `why_xlio`,
`numbers` (only verified ones), `pitfall` (a common misconception and why it's wrong),
`terms`, `question` and `answer` (a self-test), and `reading`.

## Step 3: write the issue

Create `docs/issues/DATE/issue.json` with exactly the structure of `examples/issue.json`.
Required sections: israel, us, ai, nature, study. Add a `spacex` section only when Step 1
says so; it uses the same shape as israel (`lead` and optional `briefs`). Plain text only,
no Markdown or HTML inside values. Set `track` like "Monday track: RDMA and NICs".
`terms` is a list of ["term", "plain explanation"] pairs; leave it out if there are none.

## Step 4: write the podcast script

Create `out/DATE.script.json` in the format of `examples/script.json`.
Two hosts: Alex (host "A") and Sam (host "B"), a relaxed but smart morning-show chat.

Target lengths, at about 150 spoken words per minute:

| Segment | Time | Words |
|---|---|---|
| Hello with the date and a one-line preview | 0.5 min | ~75 |
| Israel News | 3 min | ~450 |
| US News & Stock Market | 2 min | ~300 |
| AI | 6 min | ~900 |
| Nature | 2 min | ~300 |
| SpaceX (only if the section exists) | 1 min | ~150 |
| Daily study | 9 min | ~1,350 |
| Sign-off | 0.25 min | ~40 |

That's about 23 minutes (about 3,400 words) without SpaceX. Match the depth to the time:
in AI, spend about a minute and a half per story and actually explain it, rather than
rushing through more stories. If a section has less real content on a given day, keep
it shorter rather than padding it.

### How to explain on air

- One host explains, the other plays a smart listener who's new to the topic and asks the
  "wait, what does that mean?" and "why does that matter?" questions.
- Every new term gets a plain explanation the first time it's said.
- For each news story, cover what happened, what it means in plain words, and why it
  matters or how it could be used.

### The study segment (last, about 9 minutes)

In this order:
1. **The big idea (about 1 minute).** One host says what the topic is and why it matters
   in two or three plain sentences. The other restates it with an everyday analogy. By
   the end, Omri should be able to say the core idea out loud.
2. **The basics first (about 2 minutes).** Explain the fundamentals the topic builds on,
   from scratch, one concept at a time.
3. **How it works, step by step (about 3 minutes).** Walk through it in the order things
   actually happen (what the app does, what the hardware does, what lands in memory, who
   notices and how). Name the real structures and parameters and say what each is for.
   Give the key numbers and why they are what they are.
4. **A practical example (about 1 minute).** A concrete scenario, ideally from XLIO or
   NVIDIA networking.
5. **One misconception and one tradeoff (about 1 minute).**
6. **Self-test (about 1 minute).** Ask the question, pause with a line like "think about
   it for a second", then give the answer with the reasoning. End with a one-sentence
   recap of the big idea.

### Style

- Turns of 1–4 sentences, under 80 words each. Hosts react, ask each other questions and
  explain; they don't read the newsletter aloud.
- Written for the ear: no URLs, no Markdown, no lists, no emoji. Write numbers and
  abbreviations the way they should be spoken when it helps (e.g. "two point five",
  "K V cache").
- Same accuracy and neutrality rules as the written issue.

## Step 5: publish and send

Run `bash scripts/run.sh DATE`. It builds the page, makes the MP3, pushes to main
(GitHub Pages) and sends the link and audio to Telegram.

If a step fails, read the error, fix the cause (usually invalid JSON or a missing field)
and run it again. Don't send twice: if `send_telegram.py` already printed "Sent to Telegram",
stop. Finish with a one-line summary of what was sent.
