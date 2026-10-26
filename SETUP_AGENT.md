# Setup instructions for Claude Code

You are setting up "The Seven O'Clock", a daily newsletter. Do every step you can yourself.
Stop and ask Omri only where a step says **ASK**. Never write secrets (bot token, chat ID)
into any file in the repo or commit them.

Work through the steps in order and print a short status line after each one.

## Step 1: check tools

Run:
```
git --version && python3 --version && gh --version && gh auth status
```
- If `gh` is missing, install it (`brew install gh`, `winget install GitHub.cli`, or apt).
- If `gh` isn't logged in, **ASK** Omri to run `gh auth login` himself, since it opens a
  browser. Then continue.

## Step 2: create the GitHub repo and enable Pages

From the `morning-brief` folder:
```
OWNER=$(gh api user -q .login)
git init -b main
git add . && git commit -m "Initial setup"
gh repo create "$OWNER/morning-brief" --public --source=. --push
gh api -X POST "repos/$OWNER/morning-brief/pages" -f "source[branch]=main" -f "source[path]=/docs"
```
If the repo already exists, push to it instead of creating it. If Pages is already enabled,
the last command errors, which is fine. Confirm with
`gh api repos/$OWNER/morning-brief/pages -q .html_url` and save that URL as PAGES_URL
(no trailing slash).

## Step 3: Telegram bot

1. **ASK** Omri to open Telegram, message @BotFather with `/newbot`, pick a name and a
   username, and paste the token here.
2. Verify the token and get the bot username:
   `curl -s https://api.telegram.org/bot<TOKEN>/getMe`
3. **ASK** Omri to send any message to the new bot.
4. Get the chat ID:
   `curl -s https://api.telegram.org/bot<TOKEN>/getUpdates`
   and read `result[-1].message.chat.id`. If `result` is empty, ask him to send another
   message and try again.

Keep TOKEN, CHAT_ID and the bot USERNAME in shell variables only.

## Step 4: end-to-end test from this machine

This checks TTS and Telegram before the cloud routine runs. Use the fake date 2000-01-01
and clean up afterwards.
```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdir -p docs/issues/2000-01-01 out
cp examples/issue.json docs/issues/2000-01-01/
cp examples/script.json out/2000-01-01.script.json
export TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... TELEGRAM_BOT_USERNAME=... PAGES_URL=...
python3 scripts/build.py 2000-01-01
python3 scripts/podcast.py 2000-01-01
python3 scripts/send_telegram.py 2000-01-01
```
Ask Omri to confirm that a message and a short audio arrived in Telegram. Then clean up:
```
rm -rf docs/issues/2000-01-01 docs/latest out .venv
git checkout -- docs 2>/dev/null; git status
```
The working tree must be clean, with nothing from the test committed. If a step fails, fix
the cause in the scripts, commit the fix with a clear message, push, and rerun the test.

## Step 5: cloud environment and routine

If you have a tool that can create Claude Code cloud environments or routines, use it with
the settings below. Otherwise, print them in one block for Omri to set up at
claude.ai/code. He needs:

**Environment** (name: `morning-brief`)
- Environment variables (fill in the real values in your printout):
  ```
  TELEGRAM_BOT_TOKEN=<token>
  TELEGRAM_CHAT_ID=<chat id>
  TELEGRAM_BOT_USERNAME=<username without @>
  PAGES_URL=<pages url>
  ```
- Network access: allow all domains, or add `api.telegram.org` and
  `speech.platform.bing.com` to the allowed list. Mention that if news pages fail to load
  in the first run, the news sites need allowing too.

**Routine** (claude.ai/code/routines → New routine)
- Repository: `<OWNER>/morning-brief`, with pushes to `main` allowed
- Environment: `morning-brief`
- Schedule: daily at 06:30, Israel time
- Prompt: `Read ROUTINE_PROMPT.md at the repo root and follow it exactly.`

Then tell him to click **Run now** once and check Telegram at the end of the run.

## Step 6: final checklist

Print what's done and what's left, for example:
- [x] Repo created and Pages enabled at <url>
- [x] Telegram bot works (test message received)
- [ ] Environment created with variables and network access
- [ ] Routine created at 06:30 and Run now tested
- [ ] Old "Daily Computing Study" 09:00 routine paused at claude.ai/code/routines
