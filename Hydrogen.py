import re
import requests

SESSION_COOKIE = "PHPSESSID=krchqict2kl5utamc06lric7j0"
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://energymanagergame.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": SESSION_COOKIE,
}


def getHydrogenPrice():
    url = "https://energymanagergame.com/api/price.history.api.php"
    params = {"target": "hydrogen"}

    response = requests.get(url, params=params, headers=BASE_HEADERS)
    response.raise_for_status()

    prices = response.json()
    print("Latest price:", prices[-1])
    print("All prices:", prices)
    print("----------------------------------")
    return prices


def getHydrogenStorageIds():
    url = "https://energymanagergame.com/production-storage.php"

    response = requests.get(url, headers=BASE_HEADERS)
    response.raise_for_status()

    html = response.text

    pattern = r"setLiveData\((\d+),[^)]*?'p2x'"
    hydrogen_ids = re.findall(pattern, html)

    hydrogen_ids = list(dict.fromkeys(hydrogen_ids))

    print("Hydrogen storage IDs:", hydrogen_ids)
    print("----------------------------------")
    return hydrogen_ids


def isDisharging():
    url = "https://energymanagergame.com/production-storage.php"

    response = requests.get(url, headers=BASE_HEADERS)
    response.raise_for_status()

    html = response.text

    p2x_ids = re.findall(r"setChargingSim\((\d+),'p2x'", html)

    if not p2x_ids:
        print("No P2X units found")
        return False

    print("P2X IDs found:", p2x_ids)

    for unit_id in p2x_ids:
        discharge_pattern = rf"id='storage-pane-view-discharging-{unit_id}'.*?pane-discharging"

        if re.search(discharge_pattern, html, re.DOTALL):
            print(f"P2X unit {unit_id} is DISCHARGING")
            return True

    print("No P2X units are discharging")
    return False


def sellHydrogen(ids, price):
    url = "https://energymanagergame.com/hydrogen-exchange-sell.php"
    params = {"units": ",".join(ids)}

    headers = {**BASE_HEADERS, "Origin": "https://energymanagergame.com"}

    response = requests.post(url, params=params, headers=headers)
    if response.status_code != 200:
        print("Selling failed:", response.text[:300])
        print("----------------------------------")
        return None

    income_match = re.search(
        r"changeNumber\(['\"]headerAccount['\"],\s*\d+,\s*([\d.]+)",
        response.text
    )

    

    if income_match:
        income = float(income_match.group(1))
        income_rounded = round(income)
        sold = income_rounded / price if price else 0
        print(f"Sold hydrogen successfully: sold={sold}, income={income_rounded}, price={price}")
        print("----------------------------------")
        return {"sold": sold, "income": income_rounded, "price": price}

    print("Selling succeeded but could not parse income")
    print("\n\n\n\n\n\n")
    print(response.text)
    print("\n\n\n\n\n\n")
    print(response.text[:300])
    print("----------------------------------")
    return None


if __name__ == "__main__":
    getHydrogenPrice()
    getHydrogenStorageIds()
    sellHydrogen()
