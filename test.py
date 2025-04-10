#name = input("Enter name: ")

#match name:
#    case "jared" | "john":
 #       print("Hello")

def hello(to):
    print(f'Hello {to}')

name = input("Enter your name: ")
hello(name)

def greet(id):
    print(f'Thank you for clocking in {name}, your ID is {id}')

id_num =  input("Enter your WORK ID: ")
greet(id_num)