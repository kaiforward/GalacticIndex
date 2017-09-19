import pymongo

# MONGO
def mongo_connect():
    try:
        conn = pymongo.MongoClient()
        print "Mongo is connected!"
        return conn
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e


def open_collection():
    # FIND SERVER
    connect_to_mongo = mongo_connect()
    database = connect_to_mongo['Galactic_stream']
    collection = database.my_galactic_test
    return collection


def my_mongo_insert(
        number_of_planets,
        planets,
        mineral_low_sell_price,
        mineral_best_sell_price,
        mineral_high_buy_price,
        mineral_best_buy_price,
        companies,
        elements,
        elements_rarity):

    collection = open_collection()
    collection.drop()  # remove the collection
    # CREATE INITIAL INSERT OF ALL PLANETS
    for planet in xrange(0, number_of_planets):
        insert_planet = [{"PlanetName": planets[planet].name,
                          "Habitable": planets[planet].habitable,
                          "Climate": planets[planet].climate,
                          "Location": planets[planet].location,
                          "EconomicStatus": planets[planet].economic,
                          "Population": planets[planet].population,
                          "LandSpecies": planets[planet].planet_features[0],
                          "PlantSpecies": planets[planet].planet_features[1],
                          "MarineSpecies": planets[planet].planet_features[2],
                          "MineralsGas": planets[planet].minerals[0],
                          "MineralsLiquid": planets[planet].minerals[1],
                          "MineralsSolid": planets[planet].minerals[2],
                          "SellPriceGas": planets[planet].price_sell[0],
                          "SellPriceLiquid": planets[planet].price_sell[1],
                          "SellPriceSolid": planets[planet].price_sell[2],
                          "MineralsNeedGas": planets[planet].need[0],
                          "MineralsNeedLiquid": planets[planet].need[1],
                          "MineralsNeedSolid": planets[planet].need[2],
                          "BuyPriceGas": planets[planet].price_buy[0],
                          "BuyPriceLiquid": planets[planet].price_buy[1],
                          "BuyPriceSolid": planets[planet].price_buy[2]
                          }]
        # INSERT FIRST PLANET
        collection.insert(insert_planet)

    for company in xrange(0, number_of_planets):
        insert_company = [{"CompanyName": companies[company].name,
                           "Money": companies[company].company_money,
                           "profit": companies[company].profit,
                           "spent": companies[company].spent,
                           "expenses": companies[company].expenses,
                           "StockPrices": companies[company].stock_price,
                           "AveragePricePaid": companies[company].average_prices_bought_for,
                           "MineralsGas": companies[company].company_minerals[0],
                           "MineralsLiquid": companies[company].company_minerals[1],
                           "MineralsSolid": companies[company].company_minerals[2],
                           "MineralsGasInTransitBought": companies[company].minerals_in_transit_bought[0],
                           "MineralsLiquidInTransitBought": companies[company].minerals_in_transit_bought[1],
                           "MineralsSolidInTransitBought": companies[company].minerals_in_transit_bought[2],
                           "MineralsGasInTransitSold": companies[company].minerals_in_transit_sell[0],
                           "MineralsLiquidInTransitSold": companies[company].minerals_in_transit_sell[1],
                           "MineralsSolidInTransitSold": companies[company].minerals_in_transit_sell[2],
                           "TradeList": companies[company].trade_list,
                           "SellList": companies[company].sell_list
                           }]
        collection.insert(insert_company)

    # NEED TO WORK OUT HOW TO ORDER THE SELL DATA PERHAPS USING SORT(), IT ONLY NEEDS ORDERING FOR VIEWERS LEGIBILITY
    insert_high_low_prices = [
        {"ObjectName": "Collator",
         "Elements": elements,
         "Elements Rarity": elements_rarity,
         "LowPricesGas": mineral_low_sell_price[0],
         "LowPricesLiquid": mineral_low_sell_price[1],
         "LowPricesSolid": mineral_low_sell_price[2],
         "BestLowPricesGas": mineral_best_sell_price[0],
         "BestLowPricesLiquid": mineral_best_sell_price[1],
         "BestLowPricesSolid": mineral_best_sell_price[2],
         "HighPricesGas": mineral_high_buy_price[0],
         "HighPricesLiquid": mineral_high_buy_price[1],
         "HighPricesSolid": mineral_high_buy_price[2],
         "BestHighPricesGas": mineral_best_buy_price[0],
         "BestHighPricesLiquid": mineral_best_buy_price[1],
         "BestHighPricesSolid": mineral_best_buy_price[2]}]
    collection.insert(insert_high_low_prices)
    # -------------------------------------------
    return collection


def my_mongo_update(
        number_of_planets,
        planets,
        mineral_low_sell_price,
        mineral_best_sell_price,
        mineral_high_buy_price,
        mineral_best_buy_price,
        collection,
        companies,
        elements,
        elements_rarity):
    # MY MONGO UPDATE CALLED EVERY TICK TO UPDATE NEW PLANET VALUES.
    # CREATE UPDATE
    for planet in xrange(0, number_of_planets):
        update_planet_selector = {"name": planets[planet].name}
        update_planet = {"$set": {"Population": planets[planet].population,
                                  "EconomicStatus": planets[planet].economic,
                                  "MineralsGas": planets[planet].minerals[0],
                                  "MineralsLiquid": planets[planet].minerals[1],
                                  "MineralsSolid": planets[planet].minerals[2],
                                  "SellPriceGas": planets[planet].price_sell[0],
                                  "SellPriceLiquid": planets[planet].price_sell[1],
                                  "SellPriceSolid": planets[planet].price_sell[2],
                                  "MineralsNeedGas": planets[planet].need[0],
                                  "MineralsNeedLiquid": planets[planet].need[1],
                                  "MineralsNeedSolid": planets[planet].need[2],
                                  "BuyPriceGas": planets[planet].price_buy[0],
                                  "BuyPriceLiquid": planets[planet].price_buy[1],
                                  "BuyPriceSolid": planets[planet].price_buy[2]}}
        # UPDATE VALUES
        collection.update(update_planet_selector, update_planet)

    for company in xrange(0, number_of_planets):
        update_company_selector = {"name": companies[company].name}
        update_company = {"$set": {
                           "Money": companies[company].company_money,
                           "profit": companies[company].profit,
                           "spent": companies[company].spent,
                           "expenses": companies[company].expenses,
                           "StockPrices": companies[company].stock_price,
                           "AveragePricePaid": companies[company].average_prices_bought_for,
                           "MineralsGas": companies[company].company_minerals[0],
                           "MineralsLiquid": companies[company].company_minerals[1],
                           "MineralsSolid": companies[company].company_minerals[2],
                           "MineralsGasInTransitBought": companies[company].minerals_in_transit_bought[0],
                           "MineralsLiquidInTransitBought": companies[company].minerals_in_transit_bought[1],
                           "MineralsSolidInTransitBought": companies[company].minerals_in_transit_bought[2],
                           "MineralsGasInTransitSold": companies[company].minerals_in_transit_sell[0],
                           "MineralsLiquidInTransitSold": companies[company].minerals_in_transit_sell[1],
                           "MineralsSolidInTransitSold": companies[company].minerals_in_transit_sell[2],
                           "TradeList": companies[company].trade_list,
                           "SellList": companies[company].sell_list
        }}
        collection.update(update_company_selector, update_company)

    update_best_prices_selector = {"Name": "Collator"}
    update_best_prices_info = {"$set": {"Elements": elements,
                                        "Elements Rarity": elements_rarity,
                                        "LowPricesGas": mineral_low_sell_price[0],
                                        "LowPricesLiquid": mineral_low_sell_price[1],
                                        "LowPricesSolid": mineral_low_sell_price[2],
                                        "BestLowPricesGas": mineral_best_sell_price[0],
                                        "BestLowPricesLiquid": mineral_best_sell_price[1],
                                        "BestLowPricesSolid": mineral_best_sell_price[2],
                                        "HighPricesGas": mineral_high_buy_price[0],
                                        "HighPricesLiquid": mineral_high_buy_price[1],
                                        "HighPricesSolid": mineral_high_buy_price[2],
                                        "BestHighPricesGas": mineral_best_buy_price[0],
                                        "BestHighPricesLiquid": mineral_best_buy_price[1],
                                        "BestHighPricesSolid": mineral_best_buy_price[2]}}
    # UPDATE VALUES
    collection.update(update_best_prices_selector, update_best_prices_info)


