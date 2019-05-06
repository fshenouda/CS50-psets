# Port of caesar.c to Python
import cs50
from sys import argv

def main():
    # Ensure the user entered at least one arg, otherwise exit
    if (len(argv) != 2):
        print("Usage: python caesar.py <integer>")
        exit(1)

    if argv[1].isalpha() == False:
        print("Error, input only alphabeticword.")
        exit(1)

    key = argv[1]
    cipher = []
    print("plaintext: ", end="")
    plaintext = cs50.get_string()
    print("ciphertext: ", end="")
    j = 0

    for c in plaintext:
        if c.isalpha():
            letterKey = ord(key[j % len(key)].lower()) - 97
            j = j + 1
            cipher.append(caesar(c, letterKey))
        else:
            cipher.append(c)

    for c in cipher:
        print(c, end="")
    print()
    exit(0)

def caesar(char, key):
    if char.isupper():
        return chr((((ord(char) + key) - 65 ) % 26) + 65)
    else:
        return chr((((ord(char) + key) - 97 ) % 26) + 97)

if __name__ == "__main__":
    main()