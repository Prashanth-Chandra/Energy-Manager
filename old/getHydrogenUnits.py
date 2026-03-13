import requests
import re




def getHydrogenStorageIds():
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://energymanagergame.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": f"PHPSESSID=krchqict2kl5utamc06lric7j0"
    }

    url = "https://energymanagergame.com/production-storage.php"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch storage page")
        return []

    html = response.text

    ids = re.findall(r"production-charge-status-(\d+)", html)

    print("Storage IDs found:", ids)

    return ids