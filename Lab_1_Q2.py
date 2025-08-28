## First simple approach
import math

# Taking user input
a=int(input("Enter First numbers: "))
b=int(input("Enter Second numbers: "))
c=int(input("Enter Third numbers: "))

# Function to calculate LCM of two numbers using gcd
def lcm(x, y):
    return x * y // math.gcd(x, y)

# LCM of three numbers
result = lcm(lcm(a, b), c)
print("LCM of the three numbers is:", result)

## With out using the library function
def gcd(x, y):
    i=0
    while y != 0:
        
        print(f"Question 2 of KG sir lab 1.py {i}:",x,y,x%y) ## For investigating the Process
        x, y = y, x % y
        i+=1
        print(x) ## To check the final updated x value
    return x

# Function to find LCM of two numbers
def lcm(x, y):
    return (x * y) // gcd(x, y)

# Taking user input
nums = []
for i in range(3):
    num = int(input(f"Enter number {i+1}: "))
    nums.append(num)
a, b, c = nums
# Finding LCM of three numbers
result = lcm(lcm(a, b), c)

print("LCM of", a, b, c, "is:", result)


### Generalized form for any number of input to handle and also give LCM
# Step 1: Ask how many numbers
n = int(input("How many numbers do you want to enter? "))

# Step 2: Take inputs one by one
nums = []
for i in range(n):
    num = int(input(f"Enter number {i+1}: "))
    nums.append(num)

# Step 3: Find LCM of all numbers
result = nums[0]
for i in range(1, n):
    result = lcm(result, nums[i])

# Step 4: Print result
print("LCM of the given numbers is:", result)
