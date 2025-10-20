import json

with open("addresses.json", "r") as file:
    data = json.load(file)

first_name = input("Gib den Vornamen ein: ")
last_name = input("Gib den Nachnamen ein: ")

for teilnehmer in data["participants"]:
    if teilnehmer["first_name"] == first_name and teilnehmer["last_name"] == last_name:
        print(f"{teilnehmer['first_name']} {teilnehmer['last_name']} wohnt in {teilnehmer['address']['location']} in der {teilnehmer['address']['street']} mit der Postleitzahl {teilnehmer['address']['PLZ']}")
        break

else:
    print("Teilnehmer gibt es nicht")