# Load a dictionary file and censor banned words.
from cs50 import get_string
from sys import argv


def main():
    words = []

    # Check if user enter an arg, otherwise exit with status 1
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # Load a dictionary from arg
    with open(argv[1], 'r') as file:
        for l in file:
            words.append(str(l.strip()))

    print("What message would you like to censor?")
    text = get_string().split()

    # Iterate through each word in text the user input and censor
    for i in range(len(text)):
        for word in words:
            if word == str(text[i].lower()):
                text[i] = len(word)*"*"

    print(' '.join(text))

if __name__ == "__main__":
    main()
