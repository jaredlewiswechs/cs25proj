students = ["Jared", "Johnny", "Mark"]

for student in students:
    print(student)

print("")

for i in range(len(students)):
    print(i + 1, students[i])

print("")

for i in range(3):
    print('meow')


# basically a chart (column/key: row/value)
wechs = {
    "Cemerius" : "1st Period",
    "Annabelle" : "2nd Period",
    "Keiry" : "4th Period",
    "Janae" : "5th Period"
}

print(wechs["Cemerius"])
print(wechs["Annabelle"])


for student in wechs:
    print(student, wechs[student], sep = ", ")

wechs_2 = [
    {'Name' : 'Cemerius', "Period" : "1", "Gender" : "M"},
    {'Name' : 'Jocelyn', 'Period' : '2', 'Gender' : "F"}
]

for student in wechs_2:
    print(student['Name'])
    print(student['Period'])

