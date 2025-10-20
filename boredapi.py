import requests


participants = input("Wie viele Teilnehmer? (1-5): ")
url= f"https://bored.api.lewagon.com/api/activity?participants={participants}"

while True:
    try:
        responde = requests.get(url)
        result = responde.json() #Umwandlung in ein Python Dictionary
        participants = input("Wie viele Teilnehmer? (1-5): ")
        url= f"https://bored.api.lewagon.com/api/activity?participants={participants}"
        print(f"Du kannst folgendes machen: {result['activity']}")
        break
    except:
        print("Fehler bei der API Anfrage")