#!/usr/bin/env python3
"""Turn out/<date>.script.json into out/<date>.mp3 with two voices.

Script format: {"segments": [{"host": "A", "text": "..."}, {"host": "B", "text": "..."}]}
Host A = Alex, host B = Sam. Voices can be changed with HOST_A_VOICE / HOST_B_VOICE.

Usage: python3 scripts/podcast.py YYYY-MM-DD
"""
import asyncio
import json
import os
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"

VOICES = {
    "A": [os.environ.get("HOST_A_VOICE", "en-US-AndrewNeural"), "en-US-GuyNeural"],
    "B": [os.environ.get("HOST_B_VOICE", "en-US-AvaNeural"), "en-US-AriaNeural"],
}
RATE = os.environ.get("PODCAST_RATE", "+4%")
TIMEOUT = float(os.environ.get("PODCAST_SEGMENT_TIMEOUT", "60"))  # seconds per segment attempt


async def synth(text, voice):
    audio = bytearray()
    async for chunk in edge_tts.Communicate(text, voice, rate=RATE, proxy=os.environ.get("HTTPS_PROXY")).stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return bytes(audio)


async def speak(text, voices):
    last = None
    for voice in voices:
        for attempt in range(3):
            try:
                # A stalled stream would otherwise hang the whole run, so give up and retry.
                audio = await asyncio.wait_for(synth(text, voice), TIMEOUT)
                if audio:
                    return audio
            except Exception as err:  # network hiccup, timeout or unknown voice
                last = err
                await asyncio.sleep(2 * (attempt + 1))
    raise RuntimeError(f"TTS failed for all voices {voices}: {last}")


async def main(date):
    src = OUT / f"{date}.script.json"
    segments = json.loads(src.read_text(encoding="utf-8"))["segments"]
    words = sum(len(s["text"].split()) for s in segments)
    print(f"{len(segments)} segments, {words} words, about {words / 150:.1f} min")

    parts = []
    for i, seg in enumerate(segments, 1):
        parts.append(await speak(seg["text"], VOICES[seg["host"].upper()]))
        print(f"  segment {i}/{len(segments)} done", flush=True)

    # edge-tts returns MP3 with identical settings per call, so frames can be joined directly.
    dest = OUT / f"{date}.mp3"
    dest.write_bytes(b"".join(parts))
    print(f"Wrote {dest} ({dest.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: podcast.py YYYY-MM-DD")
    asyncio.run(main(sys.argv[1]))
