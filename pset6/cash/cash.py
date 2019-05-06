# Generate minimum amount of changes in Python
import cs50

while (True):
    print("Change owed: ", end="")
    change = cs50.get_float()
    if change > 0:
        break

change = round(change * 100)

quarters = change // 25
dimes = change % 25 // 10
nickels = change % 25 % 10 // 5
pennies = change % 25 % 10 % 5

print(quarters, dimes, nickels, pennies)