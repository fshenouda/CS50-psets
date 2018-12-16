// Run a validation on the credit card and determine if it's valid.
#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
    int productsumCC = 0, sumCC = 0, twodigits = 0, digitsCount = 0;
    long ccNumber = get_long_long("Number: ");

    while (ccNumber != 0)
    {
        digitsCount++;
        // Add a sum of the odd digits.
        if (digitsCount % 2 == 1)
        {
            sumCC += ccNumber % 10;
        }
        // Add a product sum of the even digits.
        if (digitsCount % 2 == 0)
        {
            int product = ccNumber % 10 * 2;
            // Check if the product is 2 digits then add them together.
            if (product > 9) product = (product / 10 % 10) + (product % 10);
            productsumCC += product;
        }
        if (ccNumber == 4) twodigits = ccNumber;
        if (ccNumber > 9 && ccNumber < 100) twodigits = ccNumber;
        ccNumber = ccNumber / 10;
    }

    int checksum = productsumCC + sumCC;

    // Run a validation test on the credit card number

    if (checksum % 10 == 0)
    {
        if (twodigits == 4  && (digitsCount == 13 || digitsCount == 16 ))
        {
            printf("VISA\n");
        }
        else if (digitsCount == 15 && (twodigits == 34 || twodigits == 37))
        {
            printf("AMEX\n");
        }
        else if (twodigits >= 51 && twodigits <= 55 && (digitsCount == 16))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else printf("INVALID\n");
}