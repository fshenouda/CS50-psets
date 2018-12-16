// Encrypt a word using Caesar's cipher.
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>

int main(int argc, string argv[])
{
    // Ensure the arg integer is inputted, otherwise return an error and exit.
    if (argc != 2)
    {
        printf("Error, please input an non-negative integer.\n");
        return 1;
    }

    int key = atoi(argv[1]);
    // Ensure the arg integer is non-negative, else return an error and exit.
    if (key < 0)
    {
        printf("Error, please input an non-negative integer.\n");
        return 1;
    }
    // Wrap the key if it goes past 26.
    key = key % 26;
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]))
        {
            char plainchar = plaintext[i];
            if (isupper(plainchar))
                plainchar = (((plainchar + key) - 65 ) % 26) + 65;
            if (islower(plainchar))
                plainchar = (((plainchar + key) - 97 ) % 26) + 97;
            plaintext[i] = plainchar;
        }
        printf("%c", plaintext[i]);
    }
    printf("\n");
    return 0;
}