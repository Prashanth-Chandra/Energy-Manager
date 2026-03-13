import requests
import re

SESSION_ID = "krchqict2kl5utamc06lric7j0"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://energymanagergame.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": f"PHPSESSID={SESSION_ID}"
}


def getMaxOilLimit():
    url = "https://energymanagergame.com/commodities.php"

    params = {
        "type": "oil"
    }

    response = requests.get(url, params=params, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch commodities page")
        return None

    html = response.text

    # Extract Holding
    holding_match = re.search(r"Holding.*?<div>([\d,]+)kg</div>", html, re.DOTALL)
    capacity_match = re.search(r"Capacity.*?<div>([\d,]+)kg</div>", html, re.DOTALL)

    if not holding_match or not capacity_match:
        print("Could not parse fuel data")
        return None

    holding = int(holding_match.group(1).replace(",", ""))
    capacity = int(capacity_match.group(1).replace(",", ""))

    max_purchase = capacity - holding

    print("Holding:", holding)
    print("Capacity:", capacity)
    print("Max purchasable:", max_purchase)

    return max_purchase

def buyOil(amount):
    url = "https://energymanagergame.com/api/commodities/buy.php"

    params = {
        "type": "oil",
        "amount": str(amount)
    }

    response = requests.get(url, params=params, headers=HEADERS)

    if response.status_code == 200:
        print("Buy request sent for", amount, "kg")
        print(response.text[:300])
    else:
        print("Buy failed:", response.status_code)


if __name__ == "__main__":
    max_amount = getMaxOilLimit()

    if max_amount and max_amount > 0:
        buyOil(100)