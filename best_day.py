from datetime import datetime, timedelta
import sys
from parser import get_messages

DEFAULT_FILE = "_chat.txt"

def main():
    print("running %s", sys.argv[0])
    print("\tbest_day usage: python3 best_day.py <file> <start_date>")
    print("\texample: python3 counter.py _chat.txt 231024")
    print("\tdate format is ddmmyy, the example above will start counting from 23rd October 2024")
    print("\tfile is optional, defaults to: %s" % DEFAULT_FILE)
    print("\tdate is optional, will start counting from the first message if not provided")
    print("\tcan only give up arguments from the end\n")
  
    file = DEFAULT_FILE
    start_date = "0"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    
    if len(sys.argv) > 2:
        start_date = sys.argv[2]
    
    messages = get_messages(file)
    
    first_msg = messages["chats"][0]
    current_date = first_msg["timestamp"]
    msg_count = 0
    prev_message = first_msg
    
    max_first_msg = messages["chats"][0]
    max_last_msg = first_msg
    max_date = first_msg["timestamp"]
    max_msg_count = 0
    
    who_sent_the_most = (first_msg["author"], 1)
    
    if start_date == "0":
        print("Start checking from date: %s" % messages["chats"][0]["timestamp"])
    countsOfPeople = {}
    for message in messages["chats"]:
        author = message["author"]
        date = message["timestamp"]
        if start_date != "0":
            if (date.year - 2000) < int(start_date[-2:]) or (date.month) < int(start_date[2:4]) or (date.day) < int(start_date[:2]):
                continue
            else:
                print("Start checking from date: %s" % date)
                start_date = "0"
        
        # if the date has changed
        if current_date.year < date.year or current_date.month < date.month or current_date.day < date.day:
            # if the day that just passed was the day with the most messages
            if max_msg_count <= msg_count:
                max_first_msg = first_msg
                max_last_msg = prev_message
                max_date = current_date
                max_msg_count = msg_count
                
                countsOfPeople = sorted(countsOfPeople.items(), key=lambda kv: kv[1])
                countsOfPeople.reverse()
                who_sent_the_most = countsOfPeople[0]
                
            msg_count = 0
            current_date = date
            first_msg = message
            countsOfPeople = {}
            
        if author not in countsOfPeople:
            countsOfPeople[author] = 1
        else:
            countsOfPeople[author] += 1
            
        msg_count += 1
        prev_message = message
    
    print(f"\nMost messages sent: {max_msg_count}")
    print(f"First message of the day's date: {max_date}")
    print("First message of the day: \"%s\"" % max_first_msg["message"])
    print(max_first_msg["author"])
    print("Last message of the day: \"%s\"" % max_last_msg["message"])
    print(max_last_msg["author"])
    print(f"Who sent the most messages that day? {who_sent_the_most[0]} with {who_sent_the_most[1]} messages")
    print("\nEnd checking at date: %s" % prev_message["timestamp"])
    
if __name__ == "__main__":
    main()