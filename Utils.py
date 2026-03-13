import requests

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://energymanagergame.com/",
    "Origin": "https://energymanagergame.com",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "PHPSESSID=krchqict2kl5utamc06lric7j0",
}


def refuelPlants():
    url = "https://energymanagergame.com/fuel-management.php"
    params = {"mode": "do", "pct": "100", "type": "oil"}
    response = requests.get(url, params=params, headers=BASE_HEADERS)
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Refuel successful")
    else:
        print("Refuel failed:", response.status_code)
    print("----------------------------------")


def setProductionOnline():
    url = "https://energymanagergame.com/production-plants-state.php"
    params = {"mode": "online"}
    response = requests.get(url, params=params, headers=BASE_HEADERS)
    if response.status_code == 200:
        print("Production plants set to ONLINE")
    else:
        print("Request failed:", response.status_code)
    print("----------------------------------")


if __name__ == "__main__":
    refuelPlants()
    setProductionOnline()
