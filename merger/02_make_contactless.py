#!/usr/bin/env python3

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from chat_utils import (
    ChatMessage,
    is_phone_like,
    normalize_author,
    parse_chat,
    signature_wo_author,
    write_chat,
)


def choose_preferred_phone(phones: set[str]) -> str:
    # Prefer a representation that already starts with '+' for readability.
    plus_first = sorted(phones, key=lambda x: (not x.strip().startswith("+"), len(x), x))
    return plus_first[0]


def infer_name_to_phone_map(messages_a: list[ChatMessage], messages_b: list[ChatMessage]) -> dict[str, str]:
    by_signature: dict[tuple[str, str], set[str]] = defaultdict(set)

    for msg in messages_a + messages_b:
        if msg.author:
            by_signature[signature_wo_author(msg)].add(normalize_author(msg.author))

    votes: dict[str, Counter[str]] = defaultdict(Counter)

    for authors in by_signature.values():
        if len(authors) < 2:
            continue

        phone_authors = {a for a in authors if is_phone_like(a)}
        name_authors = {a for a in authors if not is_phone_like(a)}

        if not phone_authors or not name_authors:
            continue

        target_phone = choose_preferred_phone(phone_authors)
        for name in name_authors:
            votes[name][target_phone] += 1

    resolved: dict[str, str] = {}
    for name, counter in votes.items():
        if not counter:
            continue
        phone, _count = counter.most_common(1)[0]
        resolved[name] = phone

    return resolved


def apply_mapping(messages: list[ChatMessage], mapping: dict[str, str]) -> list[ChatMessage]:
    updated: list[ChatMessage] = []

    # Also allow matching by fully normalized phone-key for names with odd spacing symbols.
    reverse_normalized_map = {normalize_author(k): v for k, v in mapping.items()}

    for msg in messages:
        new_msg = ChatMessage(timestamp=msg.timestamp, author=msg.author, text=msg.text)

        if new_msg.author and not is_phone_like(new_msg.author):
            normalized = normalize_author(new_msg.author)
            if normalized in reverse_normalized_map:
                new_msg.author = reverse_normalized_map[normalized]

        updated.append(new_msg)

    return updated


def print_mapping(mapping: dict[str, str]) -> None:
    if not mapping:
        print("No cross-file name->number mappings could be inferred.")
        return

    print("Resolved mappings:")
    for name in sorted(mapping):
        phone = mapping[name]
        print(f"  {name} -> {phone}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Make both WhatsApp exports contactless by replacing names with phone numbers where overlap allows it."
    )
    parser.add_argument("--old", default="old.txt", help="Path to old export")
    parser.add_argument("--new", default="new.txt", help="Path to new export")
    parser.add_argument(
        "--old-out",
        default="old_contactless.txt",
        help="Output path for rewritten old export",
    )
    parser.add_argument(
        "--new-out",
        default="new_contactless.txt",
        help="Output path for rewritten new export",
    )
    args = parser.parse_args()

    old_messages = parse_chat(args.old)
    new_messages = parse_chat(args.new)

    mapping = infer_name_to_phone_map(old_messages, new_messages)
    print_mapping(mapping)

    old_contactless = apply_mapping(old_messages, mapping)
    new_contactless = apply_mapping(new_messages, mapping)

    write_chat(args.old_out, old_contactless)
    write_chat(args.new_out, new_contactless)

    print(f"Wrote {len(old_contactless)} messages to {args.old_out}")
    print(f"Wrote {len(new_contactless)} messages to {args.new_out}")


if __name__ == "__main__":
    main()
