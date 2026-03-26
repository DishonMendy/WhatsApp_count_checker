#!/usr/bin/env python3

from __future__ import annotations

import argparse

from chat_utils import ChatMessage, parse_chat, signature, signature_wo_author, write_chat


def find_join_index(old_messages: list[ChatMessage], new_messages: list[ChatMessage]) -> int:
    if not old_messages:
        return -1

    old_last = old_messages[-1]
    target_sig = signature(old_last)
    target_sig_wo_author = signature_wo_author(old_last)

    exact_matches = [i for i, msg in enumerate(new_messages) if signature(msg) == target_sig]
    if exact_matches:
        return exact_matches[-1]

    loose_matches = [i for i, msg in enumerate(new_messages) if signature_wo_author(msg) == target_sig_wo_author]
    if loose_matches:
        return loose_matches[-1]

    # Fallback: if not found exactly, join at first message strictly after old-last timestamp.
    for i, msg in enumerate(new_messages):
        if msg.timestamp > old_last.timestamp:
            return i - 1

    return len(new_messages) - 1


def merge_chats(old_messages: list[ChatMessage], new_messages: list[ChatMessage]) -> tuple[list[ChatMessage], int]:
    join_idx = find_join_index(old_messages, new_messages)
    merged = list(old_messages)

    if join_idx + 1 < len(new_messages):
        merged.extend(new_messages[join_idx + 1 :])

    return merged, join_idx


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge old and new chat exports by appending only new messages after old's last message."
    )
    parser.add_argument("--old", default="old_contactless.txt", help="Path to old export")
    parser.add_argument("--new", default="new_contactless.txt", help="Path to new export")
    parser.add_argument("--output", default="merged.txt", help="Output merged file path")
    args = parser.parse_args()

    old_messages = parse_chat(args.old)
    new_messages = parse_chat(args.new)

    merged, join_idx = merge_chats(old_messages, new_messages)
    write_chat(args.output, merged)

    print(f"Old messages: {len(old_messages)}")
    print(f"New messages: {len(new_messages)}")
    print(f"Join index in new: {join_idx}")
    print(f"Merged messages: {len(merged)}")
    print(f"Wrote merged chat to {args.output}")


if __name__ == "__main__":
    main()
