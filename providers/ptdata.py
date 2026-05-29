import requests

URL = "https://api.ptdata.org/v1/civil-protection/occurrences/active"

def get_occurrences():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    data = r.json()

    return data["data"]["occurrences"]
