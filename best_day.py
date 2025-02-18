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
    
    # temp_sec = messages["chats"][3000]
    
    # out = first_msg["timestamp"] < temp_sec["timestamp"]
    # print(out)
    
    if start_date == "0":
        print("Start checking from date: %s" % messages["chats"][0]["timestamp"])
    for message in messages["chats"]:
        date = message["timestamp"]
        if current_date.year < date.year or current_date.month < date.month or current_date.day < date.day:
            if max_msg_count <= msg_count:
                max_first_msg = first_msg
                max_last_msg = prev_message
                max_date = current_date
                max_msg_count = msg_count
                
            msg_count = 0
            current_date = date
            first_msg = message
            
        msg_count += 1
        prev_message = message
    
    print(f"\nMost messages sent: {max_msg_count}")
    print(f"First message of the day's date: {max_date}")
    print("First message of the day: \"%s\"" % max_first_msg["message"])
    print(max_first_msg["author"])
    print("Last message of the day: \"%s\"" % max_last_msg["message"])
    print(max_last_msg["author"])
    
    print("\n--last message tested date: %s" % prev_message["timestamp"])
    
if __name__ == "__main__":
    main()