def get_number():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    return num1, num2

def adt():
    num1, num2 = get_number()
    ans = num1 + num2
    print(f'{num1} + {num2} is {ans}')


def sub():
    num1, num2 = get_number()
    ans = num1 - num2
    print(f'{num1} - {num2} is {ans}')


def mult():
    num1, num2 = get_number()
    ans = num1 * num2
    print(f'{num1} x {num2} is {ans}')


def divi():
    num1, num2 = get_number()
    ans = num1 / num2
    print(f'{num1} / {num2} is {ans}')

selection = input("Would you like to: Multiply, Divide, Subtract, or Add?: ")

if selection == "Multiply":
    mult()
elif selection == "Divide":
    divi()
elif selection == "Subtract":
    sub()
elif selection == "Add":
    adt()
else:
    print("Invalid Selection")


