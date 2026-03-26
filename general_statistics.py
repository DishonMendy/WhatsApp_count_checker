import argparse
from collections import Counter
from datetime import datetime

from parser import get_messages

DEFAULT_FILE = "_chat.txt"
DEFAULT_AMOUNT = 30


def format_message_line(message):
    text = message["message"].replace("\n", " ").strip()
    return "%s - %s: %s" % (message["timestamp"], message["author"], text)


def get_filtered_chats(chats, start_date):
    if start_date == "0":
        return chats
    cutoff = datetime.strptime(start_date, "%d%m%y")
    return [m for m in chats if m["timestamp"] >= cutoff]


def print_first_message_for_phone(chats, phone_number):
    for message in chats:
        if phone_number in message["author"]:
            print("\nFirst message for phone filter '%s':" % phone_number)
            print("Author:", message["author"])
            print("Message:\n%s" % message["message"])
            return
    print("\nNo message found for phone filter '%s'." % phone_number)


def print_counter_stats(chats, amount):
    counts_of_people = {}
    per_day_counts = {}
    first_message_date = {}

    for message in chats:
        author = message["author"]
        day_str = message["timestamp"].strftime("%Y-%m-%d")

        if author not in counts_of_people:
            counts_of_people[author] = 1
            per_day_counts[author] = {}
        else:
            counts_of_people[author] += 1

        if day_str not in per_day_counts[author]:
            per_day_counts[author][day_str] = 1
        else:
            per_day_counts[author][day_str] += 1

        if author not in first_message_date:
            first_message_date[author] = message["timestamp"].strftime("%Y-%m-%d")

    sorted_counts = sorted(counts_of_people.items(), key=lambda kv: kv[1], reverse=True)

    print("\nTop %d senders:" % amount)
    rank = 1
    for author, count in sorted_counts:
        if rank > amount:
            break
        day_counts = per_day_counts[author]
        first_date = first_message_date.get(author, "N/A")
        if day_counts:
            max_day, max_count = max(day_counts.items(), key=lambda kv: kv[1])
            print(
                "%d %s: %d (max %d on %s, first message on %s)"
                % (rank, author, count, max_count, max_day, first_date)
            )
        else:
            print("%d %s: %d (first message on %s)" % (rank, author, count, first_date))
        rank += 1


def print_best_day_stats(chats):
    day_to_messages = {}

    for message in chats:
        day_key = message["timestamp"].strftime("%Y-%m-%d")
        if day_key not in day_to_messages:
            day_to_messages[day_key] = []
        day_to_messages[day_key].append(message)

    if not day_to_messages:
        print("\nNo data for best-day statistics.")
        return

    # Match best_day.py behavior: if tie, later day wins.
    best_day_key = None
    best_day_messages = []
    best_count = -1

    for day_key in sorted(day_to_messages.keys()):
        day_messages = day_to_messages[day_key]
        day_count = len(day_messages)
        if day_count >= best_count:
            best_count = day_count
            best_day_key = day_key
            best_day_messages = day_messages

    first_msg = best_day_messages[0]
    last_msg = best_day_messages[-1]

    sender_counts = Counter(m["author"] for m in best_day_messages)
    top_sender, top_sender_count = sender_counts.most_common(1)[0]
    top_five_on_best_day = sender_counts.most_common(5)

    print("\nBest day statistics:")
    print("Most messages sent in a day: %d" % best_count)
    print("Best day date: %s" % best_day_key)
    print("First message of best day: \"%s\"" % first_msg["message"])
    print("First message author: %s" % first_msg["author"])
    print("Last message of best day: \"%s\"" % last_msg["message"])
    print("Last message author: %s" % last_msg["author"])
    print("Top sender on best day: %s with %d messages" % (top_sender, top_sender_count))
    print("Top 5 senders on best day:")
    rank = 1
    for author, count in top_five_on_best_day:
        print("%d %s: %d" % (rank, author, count))
        rank += 1


def main():
    parser = argparse.ArgumentParser(
        description="Combined statistics: counter + first_msg + best_day"
    )
    parser.add_argument("--file", default=DEFAULT_FILE, help="Chat export file path")
    parser.add_argument(
        "--amount",
        type=int,
        default=DEFAULT_AMOUNT,
        help="How many top senders to print",
    )
    parser.add_argument(
        "--start-date",
        default="0",
        help="Filter start date in ddmmyy format (example: 231024)",
    )
    parser.add_argument(
        "--phone",
        default=None,
        help="Optional phone substring to show first message for",
    )
    args = parser.parse_args()

    messages = get_messages(args.file)
    chats = messages["chats"]

    if not chats:
        print("No messages found in file: %s" % args.file)
        return

    filtered_chats = get_filtered_chats(chats, args.start_date)

    if not filtered_chats:
        print("No messages found after start date filter")
        return

    print("Start date: %s" % filtered_chats[0]["timestamp"])
    print("End date: %s" % filtered_chats[-1]["timestamp"])
    print("First message: %s" % format_message_line(filtered_chats[0]))
    print("Last message: %s" % format_message_line(filtered_chats[-1]))

    print_counter_stats(filtered_chats, args.amount)
    print_best_day_stats(filtered_chats)

    if args.phone:
        print_first_message_for_phone(filtered_chats, args.phone)


if __name__ == "__main__":
    main()
