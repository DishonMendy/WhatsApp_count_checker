#!/usr/bin/env python3

from __future__ import annotations

import argparse

from chat_utils import parse_chat, write_chat


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert old WhatsApp export structure into the new export format style."
    )
    parser.add_argument("--input", default="old.txt", help="Path to the old export file")
    parser.add_argument(
        "--output",
        default="old_structured.txt",
        help="Path to write the normalized old export",
    )
    args = parser.parse_args()

    messages = parse_chat(args.input)
    write_chat(args.output, messages)

    print(f"Normalized {len(messages)} messages from {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
