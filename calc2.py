def adt():
    ans = num1 + num2
    print(f'{num1} + {num2} is {ans}')

def sub():
    ans =  num1 - num2
    print(f'{num1} - {num2} is {ans}')

def mult():
    ans = num1 * num2
    print(f'{num1} x {num2} is {ans}')

def divi():
    ans = num1 / num2
    print(f'{num1} / {num2} is {ans}')

selection = input("Would you like to: Multiply, Divide, Subtract, or Add?: ")

if selection == "Multiply":
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    mult()
elif selection == "Divide":
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    divi()
elif selection == "Subtract":
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    sub()
elif selection == "Add":
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    adt()
else:
    print("Invalid Selection")

def get_number():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))