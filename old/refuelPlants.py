import requests

def refuelPlants():
    # The action URL
    url = "https://energymanagergame.com/fuel-management.php"

    # Query parameters
    params = {
        "mode": "do",
        "pct": "100",
        "type": "oil"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Referer": "https://energymanagergame.com/",
        "Origin": "https://energymanagergame.com",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "PHPSESSID=krchqict2kl5utamc06lric7j0"
    }

    response = requests.get(url, params=params, headers=headers)

    print("Status Code:", response.status_code)
    print(response.text[:500])  

if __name__ == "__main__":
    refuelPlants()