# Port of caesar.c to Python
import cs50
from sys import argv

# Ensure the user entered at least one arg, otherwise exit
if (len(argv) != 2):
    print("Usage: python caesar.py <integer>")
    exit(1)

# init a key and wrap it around if it go past 26th letter
key = int(argv[1])
key = key % 26

# ask for a plaintext to cypher
print("plaintext: ", end="")
plaintext = cs50.get_string()

# output encrypted text using key
print("ciphertext: ", end="")
for c in plaintext:
    if c.isalpha():
        if c.isupper():
            c = chr((((ord(c) + key) - 65 ) % 26 ) + 65)
        if c.islower():
            c = chr((((ord(c) + key) - 97 ) % 26 ) + 97)
    print(c, end="")
print()