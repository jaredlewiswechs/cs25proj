# Ask user for their name
# .strip() removes w h i t e s p a c e
# .title Capitalizes Correctly
name = input("What is your name and ID? ").strip().title()

# Split user's name into first and last name
first, last, user_id = name.split(" ")

print(f'Your first name is stored as {first}')

print(f'Your Last Name is Stored as {last}')

print(f'You entered {user_id} as your ID')


