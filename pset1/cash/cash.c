// Get the cash from the user then give lowest possible changes back.
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    float change;
    int tmpChange;
    int quarterCount = 0, dimeCount = 0, nickelCount = 0, pennyCount = 0;
    do
    {
        change = get_float("Change owed: ");
    }
    while ( change <= 0 );

    tmpChange = (int)(change * 100 + 0.5);
    printf("%i\n", tmpChange);
    while ( tmpChange % 25 >= 0 && tmpChange >= 25)
    {
        tmpChange -= 25;
        quarterCount++;
    }
    while ( tmpChange % 10 >= 0 && tmpChange >= 10)
    {
        tmpChange -= 10;
        dimeCount++;
    }
    while ( tmpChange % 5 >= 0 && tmpChange >= 5)
    {
        tmpChange -= 5;
        nickelCount++;
    }
    while ( tmpChange % 1 >= 0 && tmpChange > 0)
    {
        tmpChange -= 1;
        pennyCount++;
    }
    printf("I have %i quarters, %i dimes, %i nickels and %i pennies.\n",
        quarterCount, dimeCount, nickelCount, pennyCount);

}