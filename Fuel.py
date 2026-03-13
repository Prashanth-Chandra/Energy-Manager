import requests
import re

SESSION_ID = "krchqict2kl5utamc06lric7j0"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://energymanagergame.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": f"PHPSESSID={SESSION_ID}",
}


def getMaxOilLimit():
    url = "https://energymanagergame.com/commodities.php"
    params = {"type": "oil"}
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    holding_match = re.search(r"Holding.*?<div>([\d,]+)kg</div>", response.text, re.DOTALL)
    capacity_match = re.search(r"Capacity.*?<div>([\d,]+)kg</div>", response.text, re.DOTALL)
    if not holding_match or not capacity_match:
        print("Could not parse fuel data")
        return None
    holding = int(holding_match.group(1).replace(",", ""))
    capacity = int(capacity_match.group(1).replace(",", ""))
    max_purchase = capacity - holding
    print("Holding:", holding)
    print("Capacity:", capacity)
    print("Max purchasable:", max_purchase)
    print("----------------------------------")
    return max_purchase


def buyOil(amount, unit_price=None):
    url = "https://energymanagergame.com/api/commodities/buy.php"
    params = {"type": "oil", "amount": str(amount)}
    response = requests.get(url, params=params, headers=HEADERS)
    if response.status_code != 200:
        print("Buy failed:", response.status_code)
        print("----------------------------------")
        return None

    bought = float(amount)
    price = float(unit_price) if unit_price is not None else None
    cost = bought * price if price is not None else None
    if cost is not None:
        cost = round(cost)
        price = cost / bought if bought else None

    print("Buy request sent for", amount, "kg")
    print("----------------------------------")

    return {"bought": bought, "cost": cost, "price": price}


def getOilPrice():
    url = "https://energymanagergame.com/api/price.history.api.php"
    params = {"target": "oil", "multiplier": "1"}
    response = requests.get(url, params=params, headers=HEADERS)
    if response.status_code == 200:
        prices = response.json()
        print("Latest oil price:", prices[-1])
        print("All oil prices:", prices)
        return prices
    else:
        print("Request failed:", response.status_code)
        return None
    print("----------------------------------")


if __name__ == "__main__":
    getOilPrice()
    limit = getMaxOilLimit()
    if limit and limit > 0:
        buyOil(100)
