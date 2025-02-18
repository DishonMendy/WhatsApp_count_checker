import sys
from parser import get_messages

DEFAULT_FILE = "_chat.txt"
DEFAULT_AMOUNT = 20

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
    
    countsOfPeople = {}
    if start_date == "0":
        print("Start checking from date: %s" % messages["chats"][0]["timestamp"])
    for message in messages["chats"]:
        author = message["author"]
        date = message["timestamp"]
        if start_date != "0":
            if (date.year - 2000) < int(start_date[-2:]) or (date.month) < int(start_date[2:4]) or (date.day) < int(start_date[:2]):
                continue
            else:
                print("Start checking from date: %s" % date)
                start_date = "0"

        if author not in countsOfPeople:
            countsOfPeople[author] = 1
        else:
            countsOfPeople[author] += 1
            
    countsOfPeople = sorted(countsOfPeople.items(), key=lambda kv: kv[1])
    countsOfPeople.reverse()
    rank = 1
    for (author, count) in countsOfPeople:
        if amount > 0:
            print("%d %s: %d" % (rank, author, count))
            rank += 1
            amount -= 1
        else:
            break
    
if __name__ == "__main__":
    main()