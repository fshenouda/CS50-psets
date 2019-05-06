# Port of credit.c to Python, check for valid credit card.
import cs50

print("Credit card number: ", end="")
ccNumber = cs50.get_int()

sumCC = 0
product = 0
productsumCC = 0
digitsCount = 0

while (ccNumber != 0):
    digitsCount = digitsCount + 1
    # Add a sum of the odd digits.
    if (digitsCount % 2 == 1):
        sumCC = sumCC + ccNumber % 10
    # Add a product sum of the even digits.
    if (digitsCount % 2 == 0):
        product = ccNumber % 10 * 2
        # Check if the product is 2 digits then add them together.
        if (product > 9):
            product = (product // 10 % 10) + (product % 10)
        productsumCC = productsumCC + product
    if (ccNumber == 4):
        twodigits = ccNumber
    if (ccNumber > 9 and ccNumber < 100):
        twodigits = ccNumber
    ccNumber = ccNumber // 10

checksum = productsumCC + sumCC;

# Run a validation test on the credit card number

if (checksum % 10 == 0):
    if (twodigits == 4 and (digitsCount == 13 or digitsCount == 16 )):
        print("VISA");
    elif (digitsCount == 15 and (twodigits == 34 or twodigits == 37)):
        print("AMEX")
    elif (twodigits >= 51 and twodigits <= 55 and (digitsCount == 16)):
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")