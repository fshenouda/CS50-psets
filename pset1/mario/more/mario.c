// Construct a pyramid using user height.
#include <stdio.h>
#include <cs50.h>

void space(int n);
void hashes(int n);

int main(void)
{

    int height;
    // Get the height from user.
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);

    for (int i = 0; i <= height; i++)
    {
        // Print empty space before left side of pyramid.
        space(height-i);
        // Print hashes for the left half.
        hashes(i);
        // Print 2 empty space between both halves.
        space(2);
        // Print hashes for the right half.
        hashes(i);
        printf("\n");
    }
}

// Print empty space using value n.
void space(int n)
{
    for (int i = 0; i < n; i++) printf(" ");
}

// Print # using value n.
void hashes(int n)
{
    for (int i = 0; i < n; i++) printf("#");
}