from Hydrogen import (
    getHydrogenPrice,
    getHydrogenStorageIds,
    sellHydrogen,
    isDisharging,
)

from Utils import (
    refuelPlants,
    setProductionOnline,
)

from Fuel import (
    buyOil,
    getMaxOilLimit,
    getOilPrice,
    buyCoal,
    getMaxCoalLimit,
    getCoalPrice,
)

import random
import time
import logging

from config import OIL_BUY_MAX_PRICE, HYDROGEN_SELL_MIN_PRICE, COAL_BUY_MAX_PRICE


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] - %(message)s",
        datefmt="%d/%m/%y %H:%M:%S",
        handlers=[logging.FileHandler("main.logs"), logging.StreamHandler()],
    )
    random.seed(time.time())
    delay = lambda: time.sleep(random.uniform(1, 2))

    hydrogenPrices = getHydrogenPrice()
    if hydrogenPrices:
        logging.info("Latest hydrogen price: %s", hydrogenPrices[-1])
    else:
        logging.warning("No hydrogen prices returned")
    delay()
    if hydrogenPrices and hydrogenPrices[-1] >= HYDROGEN_SELL_MIN_PRICE:
        logging.info("Hydrogen price meets sell threshold %.2f", HYDROGEN_SELL_MIN_PRICE)
        ids = getHydrogenStorageIds()
        # logging.info("Hydrogen storage IDs found: %d", len(ids) if ids else 0)
        delay()
        if ids:
            logging.info("Selling hydrogen")
            unit_price = hydrogenPrices[-1]
            sale = sellHydrogen(ids, unit_price)
            if sale:
                print("Hydrogen sale details:", sale)
                logging.info(
                    "Hydrogen sale result - sold: %s, income: %s, price: %s",
                    sale["sold"],
                    sale["income"],
                    sale["price"],
                )
            else:
                logging.warning("Hydrogen sale response could not be parsed")
            delay()
            logging.info("Refueling oil tanks after sale")
            refuelPlants("oil")
            logging.info("Refueling coal bunkers after sale")
            refuelPlants("coal")
            logging.info("Waiting for discharging to finish before bringing plants online")
            check = 0
            while isDisharging():
                check += 1
                if check % 2 == 1:
                    logging.info("Plants still discharging (check %d); rechecking in 10s", (check+1)//2)
                time.sleep(5)
            logging.info("Discharge complete; setting production plants online")
            setProductionOnline()
    else:
        logging.info("Hydrogen price below threshold; skipping sell sequence")

    def purchaseFuel():
        logging.info("Fetching oil prices")
        oilPrices = getOilPrice()
        if oilPrices:
            logging.info("Latest oil price: %s", oilPrices[-1])
        else:
            logging.warning("No oil prices returned")
        delay()
        if oilPrices and oilPrices[-1] <= OIL_BUY_MAX_PRICE:
            logging.info("Oil price at or below buy max %.2f", OIL_BUY_MAX_PRICE)
            limit = getMaxOilLimit()
            logging.info("Oil purchase capacity: %s", limit)
            delay()
            if limit and limit > 0:
                logging.info("Buying %s kg of oil", limit)
                unit_price = oilPrices[-1]
                purchase = buyOil(limit, unit_price)
                if purchase:
                    logging.info(
                        "Oil buy result - bought: %s, cost: %s, price: %s",
                        purchase.get("bought"),
                        purchase.get("cost"),
                        purchase.get("price"),
                    )
                    logging.info("Total amount spent on oil: %s", purchase.get("cost"))
                else:
                    logging.warning("Oil buy response could not be parsed")
        else:
            logging.info("Oil price above threshold; skipping buy")
        delay()

        logging.info("Fetching coal prices")
        coalPrices = getCoalPrice()
        if coalPrices:
            logging.info("Latest coal price: %s", coalPrices[-1])
        else:
            logging.warning("No coal prices returned")
        delay()
        if coalPrices and coalPrices[-1] <= COAL_BUY_MAX_PRICE:
            logging.info("Coal price at or below buy max %.2f", COAL_BUY_MAX_PRICE)
            limit = getMaxCoalLimit()
            logging.info("Coal purchase capacity: %s", limit)
            delay()
            if limit and limit > 0:
                logging.info("Buying %s kg of coal", limit)
                unit_price = coalPrices[-1]
                purchase = buyCoal(limit, unit_price)
                if purchase:
                    logging.info(
                        "Coal buy result - bought: %s, cost: %s, price: %s",
                        purchase.get("bought"),
                        purchase.get("cost"),
                        purchase.get("price"),
                    )
                    logging.info("Total amount spent on coal: %s", purchase.get("cost"))
                else:
                    logging.warning("Coal buy response could not be parsed")
        else:
            logging.info("Coal price above threshold; skipping buy")
        delay()

    purchaseFuel()

if __name__ == "__main__":
    main()
