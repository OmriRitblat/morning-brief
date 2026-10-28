#!/usr/bin/env python3
"""Send today's issue link and podcast to Telegram.

Needs TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID and PAGES_URL (e.g. https://you.github.io/morning-brief).
Usage: python3 scripts/send_telegram.py YYYY-MM-DD
"""
import datetime
import html
import json
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
PAGES = os.environ["PAGES_URL"].rstrip("/")
API = f"https://api.telegram.org/bot{TOKEN}"


def call(method, **kwargs):
    r = requests.post(f"{API}/{method}", timeout=120, **kwargs)
    body = r.json()
    if not body.get("ok"):
        sys.exit(f"Telegram {method} failed: {body.get('description')}")
    return body


def main(date):
    data = json.loads((ROOT / "docs" / "issues" / date / "issue.json").read_text(encoding="utf-8"))["sections"]
    d = datetime.date.fromisoformat(date)
    esc = lambda s: html.escape(s, quote=False)

    lines = [
        f"<b>The Seven O'Clock</b> · {d:%A}, {d.day} {d:%B}",
        "",
        f"🇮🇱 {esc(data['israel']['lead']['headline'])}",
    ]
    lines += [f"🇺🇸 {esc(it['headline'])}" for it in data["us"]["items"]]
    lines += [f"🤖 {esc(s['headline'])}" for s in data["ai"]["stories"]]
    lines.append(f"🌿 {esc(data['nature']['headline'])}")
    spacex = data.get("spacex")
    if spacex and not spacex.get("quiet"):
        lines.append(f"🚀 {esc(spacex['lead']['headline'])}")
    lines += [f"📘 {esc(data['study']['title'])}", "", f'<a href="{PAGES}/issues/{date}/">Read today\'s issue</a>']

    call("sendMessage", data={"chat_id": CHAT, "text": "\n".join(lines), "parse_mode": "HTML"})

    mp3 = ROOT / "out" / f"{date}.mp3"
    if mp3.exists():
        with mp3.open("rb") as f:
            call("sendAudio", data={"chat_id": CHAT, "title": f"The Seven O'Clock, {d.day} {d:%B}",
                                    "performer": "Alex & Sam"}, files={"audio": f})
    else:
        call("sendMessage", data={"chat_id": CHAT, "text": "The podcast couldn't be generated today. The written issue is above."})
    print("Sent to Telegram")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: send_telegram.py YYYY-MM-DD")
    main(sys.argv[1])
