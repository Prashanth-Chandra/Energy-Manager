import requests

def setProductionOnline():
    url = "https://energymanagergame.com/production-plants-state.php"

    params = {
        "mode": "online"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://energymanagergame.com/",
        "Origin": "https://energymanagergame.com",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "PHPSESSID=krchqict2kl5utamc06lric7j0"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        print("Production plants set to ONLINE")
        print(response.text[:300])  # preview HTML
    else:
        print("Request failed:", response.status_code)


if __name__ == "__main__":
    setProductionOnline()