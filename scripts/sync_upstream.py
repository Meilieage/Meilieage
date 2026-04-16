from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "upstream_sources.json"


def fetch_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MeilieageRuleBot/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def ensure_trailing_newline(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.endswith("\n"):
        text += "\n"
    return text


def main() -> None:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Missing config file: {CONFIG_FILE}")

    data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    sources = data.get("sources", [])

    if not isinstance(sources, list):
        raise ValueError("'sources' must be a list")

    for item in sources:
        if not item.get("enabled", True):
            continue

        url = item["url"]
        target = ROOT / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)

        print(f"[SYNC] {url} -> {target}")
        content = fetch_text(url)
        content = ensure_trailing_newline(content)
        target.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
