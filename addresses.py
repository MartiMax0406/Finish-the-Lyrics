import json

with open("addresses.json", "r") as file:
    data = json.load(file)



course_id = input(str("Kurs ID eingeben: "))
course_name = input(str("Kurs Name eingeben: "))


if (data["course_id"], data["course_name"]) == (course_id, course_name):
    for participant in data["participants"]:
        print(participant["first_name"])