# The Seven O'Clock

A daily newsletter and two-host podcast, built by a Claude Code routine and delivered to Telegram at 07:00 Israel time.

## How it works

The routine runs at 06:30. Claude researches the news, writes `docs/issues/<date>/issue.json` and a podcast script, then runs `scripts/run.sh`, which:

1. renders the page from `template/issue.html` (`scripts/build.py`)
2. turns the script into an MP3 with two voices (`scripts/podcast.py`, edge-tts)
3. commits and pushes to `main`, so GitHub Pages publishes it
4. sends the headlines, the link and the MP3 to Telegram (`scripts/send_telegram.py`)

The routine's instructions live in `ROUTINE_PROMPT.md`, so you change the newsletter by editing that file. The MP3s are not committed, to keep the repo small. The podcast lives in Telegram.

## Setup

**Easiest:** open this folder in Claude Code and say: `Read SETUP_AGENT.md and do it.` It does everything below, asking you only for the Telegram parts.

To do it by hand instead:

### 1. GitHub repo and Pages
1. Create a **public** repo called `morning-brief` and push these files. GitHub Pages is free for public repos; a private one needs a paid plan.
2. Go to Settings → Pages → Build and deployment → Deploy from a branch, then pick `main` and `/docs`.
3. Your site will be at `https://<github-user>.github.io/morning-brief`.

### 2. Telegram bot
1. In Telegram, message **@BotFather** with `/newbot` and pick a name and username. Copy the token.
2. Send your new bot any message, such as "hi".
3. Open `https://api.telegram.org/bot<TOKEN>/getUpdates` in a browser and copy `message.chat.id`.

### 3. Cloud environment (claude.ai/code)
Create a new environment called `morning-brief` and set these variables:

```
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=123456789
TELEGRAM_BOT_USERNAME=your_bot_username
PAGES_URL=https://<github-user>.github.io/morning-brief
```

For **network access**, the default Trusted level blocks Telegram and the TTS service. Either allow all domains, or add these:
- `api.telegram.org`
- `speech.platform.bing.com`
- the news sites, if web fetches get blocked

Environment variable values are visible to anyone who uses the environment, so keep this one for yourself.

### 4. Routine (claude.ai/code/routines → New routine)
- **Repository:** `morning-brief`, with pushes to `main` allowed. By default routines only push to `claude/` branches, and Pages won't see those.
- **Environment:** `morning-brief`
- **Schedule:** daily, 06:30, Israel time
- **Prompt:** `Read ROUTINE_PROMPT.md at the repo root and follow it exactly.`

Use **Run now** once to test it.

### 5. Turn off the old email routine
The study section replaces the 09:00 "Daily Computing Study" email, so pause that routine to avoid duplicates.

## Options
- **Voices:** set `HOST_A_VOICE` and `HOST_B_VOICE` to any edge-tts voice (`edge-tts --list-voices`). `PODCAST_RATE` changes the speed, for example `+10%`.
- **Better audio later:** `podcast.py` is the only file to change if you move to a paid TTS such as ElevenLabs.
