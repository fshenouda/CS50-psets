# Port of mario.c in Python
import cs50

# get user input and ensure that it's between 0 and 8
while True:
    print("Height: ", end="")
    height = cs50.get_int()
    if (height > 0 and height < 9):
        break

# set str variables for empty space and block
space = " "
block = "#"

# iterate over each line in pyramid
for i in range(height):
    print((height-i-1)*space + (1+i)*block + 2*space + (1+i)*block)