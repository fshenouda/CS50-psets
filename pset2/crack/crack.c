// Decrypt a hashed password that use C's DES encryption.
#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <cs50.h>

string hash;
char salt[3];
int hashMatches(string word);

int main(int argc, string argv[])
{
    // Ensure user input exist, otherwise return an error and exit.
    if (argc != 2)
    {
        printf("Usage: ./crack <password>\n");
        return 1;
    }

char word[5];
hash = argv[1];
salt[0] = hash[0];
salt[1] = hash[1];

// Store all ASCII characters in an array
string letters = "\0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

// Use a reverse loop to brute force all possible hashes.

for (int m = 0; m < 57; m++)
    for (int l = 0; l < 57; l++)
        for (int k = 0; k < 57; k++)
            for (int j = 0; j < 57; j++)
                for (int i = 0; i < 57; i++)
                {
                    word[0] = letters[i];
                    word[1] = letters[j];
                    word[2] = letters[k];
                    word[3] = letters[l];
                    word[4] = letters[m];
                    if (hashMatches(word)) return 0;
                }
    return 1;
}

// Compare the generated hash against user's input of hash.
int hashMatches(string word)
{
    if (strcmp(crypt(word, salt), hash) == 0)
    {
        printf("%s\n", word);
        return 1;
    }
    return 0;
}