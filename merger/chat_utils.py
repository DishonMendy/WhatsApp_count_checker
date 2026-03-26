#!/usr/bin/env python3

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

# Unicode direction/format characters that often appear in WhatsApp exports.
_INVISIBLE_CHARS = [
    "\u200e",  # LRM
    "\u200f",  # RLM
    "\u202a",  # LRE
    "\u202b",  # RLE
    "\u202c",  # PDF
    "\u2066",  # LRI
    "\u2067",  # RLI
    "\u2068",  # FSI
    "\u2069",  # PDI
    "\ufeff",  # BOM
    "\xa0",    # NBSP
]

DATE_PREFIX_RE = re.compile(r"^\u200e?[0-9]{1,2}[./][0-9]{1,2}[./][0-9]{2,4}, [0-9]{1,2}:[0-9]{2} - ")
MESSAGE_LINE_RE = re.compile(
    r"^\u200e?(?P<date>[0-9]{1,2}[./][0-9]{1,2}[./][0-9]{2,4}, [0-9]{1,2}:[0-9]{2}) - (?P<body>.*)$"
)

DATE_FORMATS = (
    "%d/%m/%Y, %H:%M",
    "%d/%m/%y, %H:%M",
    "%d.%m.%Y, %H:%M",
    "%d.%m.%y, %H:%M",
)


@dataclass
class ChatMessage:
    timestamp: datetime
    author: str | None
    text: str


def strip_invisible(text: str) -> str:
    result = text
    for ch in _INVISIBLE_CHARS:
        result = result.replace(ch, "")
    return result


def normalize_author(author: str) -> str:
    return strip_invisible(author).strip()


def parse_timestamp(date_text: str) -> datetime:
    cleaned = strip_invisible(date_text).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_text}")


def is_phone_like(author: str) -> bool:
    cleaned = re.sub(r"[\s\-()\u200e\u200f]+", "", strip_invisible(author))
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    return cleaned.isdigit() and len(cleaned) >= 7


def normalize_phone_key(author: str) -> str:
    cleaned = re.sub(r"[\s\-()\u200e\u200f]+", "", strip_invisible(author))
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    return cleaned


def parse_chat(path: str | Path) -> list[ChatMessage]:
    lines = Path(path).read_text(encoding="utf8").splitlines()
    messages: list[ChatMessage] = []

    for line in lines:
        if not line.strip():
            continue

        if not DATE_PREFIX_RE.match(line):
            if messages:
                messages[-1].text += "\n" + line
            continue

        match = MESSAGE_LINE_RE.match(line)
        if not match:
            if messages:
                messages[-1].text += "\n" + line
            continue

        timestamp = parse_timestamp(match.group("date"))
        body = strip_invisible(match.group("body"))

        author: str | None = None
        text = body

        if ": " in body:
            possible_author, possible_text = body.split(": ", 1)
            possible_author = normalize_author(possible_author)
            if possible_author:
                author = possible_author
                text = possible_text

        messages.append(ChatMessage(timestamp=timestamp, author=author, text=text))

    return messages


def to_standard_line(message: ChatMessage) -> str:
    date_part = message.timestamp.strftime("%d/%m/%Y, %H:%M")
    if message.author is None:
        return f"{date_part} - {message.text}"
    return f"{date_part} - {message.author}: {message.text}"


def write_chat(path: str | Path, messages: Iterable[ChatMessage]) -> None:
    out_lines = [to_standard_line(msg) for msg in messages]
    Path(path).write_text("\n".join(out_lines) + "\n", encoding="utf8")


def signature(message: ChatMessage) -> tuple[str, str, str]:
    author_key = message.author or ""
    return (
        message.timestamp.isoformat(timespec="minutes"),
        author_key,
        message.text,
    )


def signature_wo_author(message: ChatMessage) -> tuple[str, str]:
    return (
        message.timestamp.isoformat(timespec="minutes"),
        message.text,
    )
