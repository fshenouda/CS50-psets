# Port of crack.c to Python
import crypt
import string
from sys import argv

# Ensure the user entered at least one arg, otherwise exit
if (len(argv) != 2):
    print("Usage: python crack.py hash")
    exit(1)

# init a hash as as a string
hashed = str(argv[1])
salt = str(hashed[:2])
password = ""

# Store all ASCII charactersin an tuple
letters = string.ascii_letters
letlen = len(letters)

# iterate through a hash to brute force all possible hashes
for i in range(letlen):
    for j in range(letlen):
        for k in range(letlen):
            for m in range(letlen):
                for n in range(letlen):
                    # check if the hash matches the word and exits if passed
                    if crypt.crypt(password, salt) == hashed:
                        print(password)
                        exit(0)
                    password = letters[n] + password[1:]
                password = password[:1] + letters[m] + password[2:]
            password = password[:2] + letters[k] + password[3:]
        password = password[:3] + letters[j] + password[4:]
    password = password[:4] + letters[i] + password[5:]