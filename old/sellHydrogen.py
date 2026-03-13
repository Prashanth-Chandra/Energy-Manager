import requests

def sellHydrogen():
    url = "https://energymanagergame.com/hydrogen-exchange-sell.php"

    params = {
        "units": "15010685,15021967,15035416"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://energymanagergame.com/",
        "Origin": "https://energymanagergame.com",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "PHPSESSID=krchqict2kl5utamc06lric7j0"
    }

    response = requests.post(url, params=params, headers=headers)

    print("Status:", response.status_code)
    if response.status_code == 200:
        print("Hydrogen sold successfully!")
    else:
        print("Failed to sell hydrogen.")


if __name__ == "__main__":
    sellHydrogen()