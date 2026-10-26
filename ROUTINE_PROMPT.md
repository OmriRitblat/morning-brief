# The Seven O'Clock: daily routine

You produce Omri's morning newsletter, publish it, and send it to Telegram.
Omri is a software engineering student on NVIDIA's XLIO team (user-space accelerated
TCP/UDP sockets over ConnectX NICs). Everything is in English.

## Step 0: date

Run `TZ=Asia/Jerusalem date +%F` and `TZ=Asia/Jerusalem date +%A`. Use that date
(DATE below) and weekday everywhere. "Today's news" means roughly the last 24 hours.

## Step 1: research the news

Use web search and fetch. Run separate searches per section. Only include stories you
found in today's sources. Never invent or guess facts, numbers or quotes. If something
can't be confirmed, leave it out. Link primary or reputable sources.

- **politics**: Israeli politics. Lead story plus 2–3 briefs. Strictly neutral: report
  what each side said and did, attribute every claim, no opinions or loaded wording.
  Check more than one outlet (e.g. Times of Israel, Haaretz, Ynet, Jerusalem Post, Kan).
- **israel**: the main non-political Israeli news (security, economy, society, tech).
  Lead plus 2–3 briefs. Don't repeat the politics stories.
- **ai**: the most important AI developments (models, papers, products, infrastructure).
  Prefer the lab's own announcement, paper or release notes. Lead plus 2–3 briefs.
  Prioritize inference, infrastructure, agents and anything NVIDIA-relevant.
- **nature**: one interesting, easy-to-read article from Nature's news or news-feature
  section (nature.com), published in the last few days. Find candidates in the feed at
  https://www.nature.com/nature.rss (news items have DOIs starting `d41586`). Prefer one
  whose full text you can read. Many are behind a login, and that's fine: then pick the
  most interesting one and write the summary only from what you could read (the feed
  description, the standfirst and opening paragraphs, and the underlying paper if it's
  open access). Give a plain-language summary and 3 key points: what they found, how, and
  why it matters.
- **spacex**: only if something is genuinely interesting (Starship flights, major launches,
  milestones). Otherwise set `"quiet": true`. Give launch times in Israel time.

Lead stories: 150–200 words in 2 paragraphs. Briefs: 2–3 sentences.

Read pages with the web fetch tool only. Don't use curl, cookie jars or other ways around
logins, paywalls or bot checks. If a page won't load, use another source.

No single section may stop the issue. If a section's preferred source isn't available,
use another reputable source, or write a shorter section from what you could confirm.
The issue must always be published and sent.

## Step 2: daily study section

Run `python3 scripts/study_history.py` and do NOT repeat any listed topic or a close
variant. Go from fundamentals to advanced within each track over time.

Track by weekday:
- Sunday: XLIO and kernel bypass (LD_PRELOAD socket interception, user-space TCP/IP,
  polling vs interrupts, busy-poll, zero-copy, TSO/LRO/GRO, checksum offload, striding RQ,
  TLS and NVMe/TCP offload, XLIO vs DPDK vs AF_XDP vs io_uring)
- Monday: RDMA and NICs (verbs: QP, CQ, MR, WQE; RC/UD/DC; InfiniBand vs RoCEv2;
  PFC/ECN/DCQCN; ConnectX; BlueField; SR-IOV; GPUDirect RDMA)
- Tuesday: TCP in depth (CUBIC, BBR, DCTCP, windowing, SACK, Nagle/delayed ACK,
  TIME_WAIT, incast, Linux RX/TX path: NAPI, skb, RSS/RPS/XPS)
- Wednesday: architecture and performance (cache coherence, NUMA, PCIe, TLB and hugepages,
  SIMD, IRQ/CPU pinning, roofline, tail latency, perf, eBPF, flame graphs, sockperf/iperf/perftest)
- Thursday: AI compute and interconnect (GPU and HBM, NVLink, NVSwitch, NVL72,
  GPUDirect Storage, NCCL collectives, SHARP, Spectrum-X, data/tensor/pipeline/expert parallelism)
- Friday: AI inference (KV cache, continuous batching, PagedAttention, quantization,
  speculative decoding, prefill/decode disaggregation, TensorRT-LLM, vLLM, Triton, Dynamo, NIXL)
- Saturday: agents and sandboxes (agent loop, tool calling, MCP, context and memory,
  planning, evals, containers, gVisor, Firecracker, prompt injection)

Write it precisely, for a student with solid CS fundamentals. Verify key numbers.

## Step 3: write the issue

Create `docs/issues/DATE/issue.json` with exactly the structure of `examples/issue.json`
(all six sections: politics, israel, ai, nature, spacex, study). Plain text only, no
Markdown or HTML inside values. Set `track` like "Monday track: RDMA and NICs".

## Step 4: write the podcast script

Create `out/DATE.script.json` in the format of `examples/script.json`.
Two hosts: Alex (host "A") and Sam (host "B"), a relaxed but smart morning-show chat.

- Usually 2,000–2,250 words (about 13–15 minutes). This is a minimum, not a cap: on
  busy days the episode runs longer. Never shorten a section to hit a length.
- Order: short hello with the date, politics (~2.5 min), Israel (~2 min), AI (~2.5 min),
  Nature (~1.5 min, explain the main points simply), SpaceX (~1 min, skip entirely if quiet),
  daily study (~5 min, see below), quick sign-off.

### The study segment (last, about 750 words)

It has two parts, in this order:

1. **The main point (about 1 minute).** One host says in two or three sentences what the
   topic is and why it matters for XLIO. The other host restates it in their own words
   with a simple analogy. By the end of this part, Omri should be able to say the core
   idea out loud.
2. **The deep dive (about 4 minutes).** Go properly deep, step by step:
   - Walk the mechanism in order, the way data or control actually flows (e.g. what the
     app writes, what the NIC does, what lands in memory, who notices and how).
   - Name the real structures, fields and parameters involved, and what each is for.
   - Give the key numbers and explain why they are what they are.
   - Cover one tradeoff or design choice, and why engineers make it one way or the other.
   - Cover one common misconception and why it's wrong.
   - Connect it to something concrete in XLIO or NVIDIA networking.
   - One host plays the learner and asks the "wait, why?" questions a smart student would.
   Then check understanding: ask the self-test question, pause with a line like
   "think about it for a second", and give the answer with the reasoning behind it.
   End with a one-sentence recap of the main point.
- Turns of 1–4 sentences, under 80 words each. Hosts react, ask each other questions and
  explain, they don't just read the newsletter.
- Written for the ear: no URLs, no Markdown, no lists, no emoji. Write numbers and
  abbreviations the way they should be spoken when it helps (e.g. "two point five", "K V cache").
- Same accuracy and neutrality rules as the written issue.

## Step 5: publish and send

Run `bash scripts/run.sh DATE`. It builds the page, makes the MP3, pushes to main
(GitHub Pages) and sends the link and audio to Telegram.

If a step fails, read the error, fix the cause (usually invalid JSON or a missing field)
and run it again. Don't send twice: if `send_telegram.py` already printed "Sent to Telegram",
stop. Finish with a one-line summary of what was sent.
