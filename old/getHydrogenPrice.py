import requests

def getHydrogenPrice():
    url = "https://energymanagergame.com/api/price.history.api.php"

    params = {"target": "hydrogen"}

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://energymanagergame.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "PHPSESSID=krchqict2kl5utamc06lric7j0"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        prices = response.json()
        print("Latest price:", prices[-1])
        print("All prices:", prices)
    else:
        print("Request failed:", response.status_code)

if __name__ == "__main__":
    getHydrogenPrice()