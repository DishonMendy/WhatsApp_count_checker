import sys
from datetime import datetime
from parser import get_messages

DEFAULT_FILE = "_chat.txt"
DEFAULT_AMOUNT = 20


def format_message_line(message):
    # Keep multiline messages readable in a single console line.
    text = message["message"].replace("\n", " ").strip()
    return "%s - %s: %s" % (message["timestamp"], message["author"], text)

def main():
    print("running %s", sys.argv[0])
    print("\tcounter usage: python3 counter.py <file> <amount> <start_date>")
    print("\texample: python3 counter.py _chat.txt 100 231024")
    print("\tamount is how many people to show (ordered by count, desc)")
    print("\tdate format is ddmmyy, the example above will start counting from 23rd October 2024")
    print("\tfile is optional, defaults to: %s" % DEFAULT_FILE)
    print("\tamount is optional, defaults to: %s" % DEFAULT_AMOUNT)
    print("\tdate is optional, will start counting from the first message if not provided")
    print("\tcan only give up arguments from the end\n")
  
    file = DEFAULT_FILE
    start_date = "0"
    amount = DEFAULT_AMOUNT
    if len(sys.argv) > 1:
        file = sys.argv[1]
    
    if len(sys.argv) > 2:
        amount = int(sys.argv[2])
        
    if len(sys.argv) > 3:
        start_date = sys.argv[3]
    
    messages = get_messages(file)
    chats = messages["chats"]

    if not chats:
        print("No messages found in file: %s" % file)
        return

    filtered_chats = chats
    if start_date != "0":
        cutoff = datetime.strptime(start_date, "%d%m%y")
        filtered_chats = [m for m in chats if m["timestamp"] >= cutoff]

    if not filtered_chats:
        print("No messages found after start date filter")
        return

    print("Start date: %s" % filtered_chats[0]["timestamp"])
    print("End date: %s" % filtered_chats[-1]["timestamp"])
    print("First message: %s" % format_message_line(filtered_chats[0]))
    print("Last message: %s" % format_message_line(filtered_chats[-1]))
    
    countsOfPeople = {}
    perDayCounts = {}
    for message in filtered_chats:
        author = message["author"]
        date = message["timestamp"]
        day_str = date.strftime("%Y-%m-%d")

        if author not in countsOfPeople:
            countsOfPeople[author] = 1
            perDayCounts[author] = {}
        else:
            countsOfPeople[author] += 1
        if day_str not in perDayCounts[author]:
            perDayCounts[author][day_str] = 1
        else:
            perDayCounts[author][day_str] += 1

    countsOfPeople = sorted(countsOfPeople.items(), key=lambda kv: kv[1])
    countsOfPeople.reverse()
    rank = 1
    for (author, count) in countsOfPeople:
        if amount > 0:
            # Find the day with the most messages for this author
            day_counts = perDayCounts[author]
            if day_counts:
                max_day, max_count = max(day_counts.items(), key=lambda kv: kv[1])
                print("%d %s: %d (max %d on %s)" % (rank, author, count, max_count, max_day))
            else:
                print("%d %s: %d" % (rank, author, count))
            rank += 1
            amount -= 1
        else:
            break
    
if __name__ == "__main__":
    main()