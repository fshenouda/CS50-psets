// Encrypt a word using Vigenere's cipher.
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>

int main(int argc, string argv[])
{
    // Ensure the arg alphabetic word is inputted, otherwise return error.
    if (argc != 2)
    {
        printf("Error, please input only alphabetic word.\n");
        return 1;
    }

    // Ensure the arg alphabetic word, else return an error and exit.
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Error, please input only alphabetic word.\n");
            return 1;
        }
    }
    string key = argv[1];
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, j = 0; i < strlen(plaintext); i++)
    {
        int letterKey = tolower(key[j % strlen(key)]) - 'a';
        if (isalpha(plaintext[i]))
        {
            char plainchar = plaintext[i];
            if (isupper(plainchar))
                plainchar = (((plainchar + letterKey) - 65 ) % 26) + 65;
            if (islower(plainchar))
                plainchar = (((plainchar + letterKey) - 97 ) % 26) + 97;
            plaintext[i] = plainchar;
            j++;
        }
    printf("%c", plaintext[i]);
    }
    printf("\n");
    return 0;
}