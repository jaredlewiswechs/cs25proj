# Making a calc (with integers)

x = int(input("What is X? "))
y = int(input("What is X? "))

ans = x + y

print(f'The total is {ans}')

# Making a calc (with decimals - floats)

a = float(input("What is X? "))
b = float(input("What is X? "))

ans_2 = a + b

rounded = round(ans_2)

print(f'The rounded answer is {rounded}, and the decimal answer is {ans_2}')


def adt():
    ans = num1 + num2
    print(ans)

def sub():
    ans =  num1 - num2
    print(ans)

def mult():
    ans = num1 * num2
    print(ans)

def divi():
    ans = num1 / num2
    print(ans)

selection = input("Would you like to: Multiply, Divide, Subtract, or Add?: ")
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))

if selection == "Multiply":
    mult()
elif selection == "Divide":
    divi()
elif selection == "Subtract":
    sub()
elif selection == "Addition":
    adt()
else:
    print("Invalid Selection")







































