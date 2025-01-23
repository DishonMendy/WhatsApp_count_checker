import sys
from parser import get_messages

DEFAULT_FILE = "_chat.txt"
DEFAULT_START = 250102
DEFAULT_SKIP = 500

def main():
    if len(sys.argv) <= 1:
        print("\tuseage: python3 checker.py <file> <start_number> <skip_limit>")
        print("\texample: python3 checker.py _chat.txt 250000 500")
        print("\tfile is optional, defaults to: %s" % DEFAULT_FILE)
        print("\start number is optional, defaults to: %d" % DEFAULT_START)
        print("\tskip limit is optional, defaults to: %d" % DEFAULT_SKIP)
        print("\tstart number might fail if it was mentioned before it was supposed to arrive, do not choose a cool number.")
        sys.exit(0)
        

    messages = get_messages(sys.argv[1])
    
    next_number = DEFAULT_START
    if len(sys.argv) > 2:
        next_number = int(sys.argv[2])
        
    skip_limit = DEFAULT_SKIP
    if len(sys.argv) > 3:
        skip_limit = int(sys.argv[3])
        
    skipped_in_a_row = 0
    prev_author = '-1'
    last_message = ""
    started = False
    print("Start checking from message number: %d" % next_number)
    for message in messages["chats"]:
        if str(next_number) in message["message"]:
            started = True
        if (message["author"] != prev_author) and (str(next_number) in message["message"]):
            print('--> %d' % next_number)
            next_number += 1
            prev_author = message["author"]
            last_message = message["message"]
            skipped_in_a_row = 0
        elif started:
            skipped_in_a_row += 1
            print('skipped %d: %s' % (skipped_in_a_row, message))
            if skipped_in_a_row == skip_limit:
                print("Too many skipped messages in a row. Exiting.")
                break
        
    print("Last correct number: %d" % (next_number - 1))
    print("by: %s" % prev_author)
    print("message content:\n%s" % last_message)
    
    
if __name__ == "__main__":
    main()