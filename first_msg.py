import sys
from parser import get_messages

DEFAULT_FILE = "_chat.txt"

def main():
    print("running", sys.argv[0])

        
    if len(sys.argv) < 2:
        print("Usage: python3 first_msg.py <phone_number> [file]")
        print("Example: python3 first_msg.py 52-123-3457 _chat.txt")
        print("File is optional, defaults to:", DEFAULT_FILE)
        return
    
    phone_number = sys.argv[1]
    file = DEFAULT_FILE
    if len(sys.argv) > 2:
        file = sys.argv[2]
    messages = get_messages(file)
    found = False
    for message in messages["chats"]:
        if phone_number in message["author"]:
            print("First message from:", message["author"])
            print("Message content:\n", message["message"])
            found = True
            break
    if not found:
        print("No message found from this phone number.")
    
    
if __name__ == "__main__":
    main()