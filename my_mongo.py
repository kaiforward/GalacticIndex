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
        insert_planet = [{"name": planets[planet].name,
                          "Habitable": planets[planet].habitable,
                          "Climate": planets[planet].climate,
                          "Location": planets[planet].location,
                          "Economic Status": planets[planet].economic,
                          "Population": planets[planet].population,
                          "Land Species": planets[planet].planet_features[0],
                          "Plant Species": planets[planet].planet_features[1],
                          "Marine Species": planets[planet].planet_features[2],
                          "Minerals Gas": planets[planet].minerals[0],
                          "Minerals Liquid": planets[planet].minerals[1],
                          "Minerals Solid": planets[planet].minerals[2],
                          "Sell Price Gas": planets[planet].price_sell[0],
                          "Sell Price Liquid": planets[planet].price_sell[1],
                          "Sell Price Solid": planets[planet].price_sell[2],
                          "Minerals Need Gas": planets[planet].need[0],
                          "Minerals Need Liquid": planets[planet].need[1],
                          "Minerals Need Solid": planets[planet].need[2],
                          "Buy Price Gas": planets[planet].price_buy[0],
                          "Buy Price Liquid": planets[planet].price_buy[1],
                          "Buy Price Solid": planets[planet].price_buy[2]
                          }]
        # INSERT FIRST PLANET
        collection.insert(insert_planet)

    for company in xrange(0, number_of_planets):
        insert_company = [{"name": companies[company].name,
                           "Money": companies[company].company_money,
                           "profit": companies[company].profit,
                           "spent": companies[company].spent,
                           "expenses": companies[company].expenses,
                           "Stock Prices": companies[company].stock_price,
                           "Average Price Paid": companies[company].average_prices_bought_for,
                           "Minerals Gas": companies[company].company_minerals[0],
                           "Minerals Liquid": companies[company].company_minerals[1],
                           "Minerals Solid": companies[company].company_minerals[2],
                           "Minerals Gas in Transit Bought": companies[company].minerals_in_transit_bought[0],
                           "Minerals Liquid in Transit Bought": companies[company].minerals_in_transit_bought[1],
                           "Minerals Solid in Transit Bought": companies[company].minerals_in_transit_bought[2],
                           "Minerals Gas in Transit Sold": companies[company].minerals_in_transit_sell[0],
                           "Minerals Liquid in Transit Sold": companies[company].minerals_in_transit_sell[1],
                           "Minerals Solid in Transit Sold": companies[company].minerals_in_transit_sell[2],
                           "Trade List": companies[company].trade_list,
                           "Sell List": companies[company].sell_list
                           }]
        collection.insert(insert_company)

    # NEED TO WORK OUT HOW TO ORDER THE SELL DATA PERHAPS USING SORT(), IT ONLY NEEDS ORDERING FOR VIEWERS LEGIBILITY
    insert_high_low_prices = [
        {"Name": "Collator",
         "Elements": elements,
         "Elements Rarity": elements_rarity,
         "Low Prices Gas": mineral_low_sell_price[0],
         "Low Prices Liquid": mineral_low_sell_price[1],
         "Low Prices Solid": mineral_low_sell_price[2],
         "Best low prices Gas": mineral_best_sell_price[0],
         "Best low prices Liquid": mineral_best_sell_price[1],
         "Best low prices Solid": mineral_best_sell_price[2],
         "High Prices Gas": mineral_high_buy_price[0],
         "High Prices Liquid": mineral_high_buy_price[1],
         "High Prices Solid": mineral_high_buy_price[2],
         "Best high prices Gas": mineral_best_buy_price[0],
         "Best high prices Liquid": mineral_best_buy_price[1],
         "Best high prices Solid": mineral_best_buy_price[2]}]
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
                                  "Economic Status": planets[planet].economic,
                                  "Minerals Gas": planets[planet].minerals[0],
                                  "Minerals Liquid": planets[planet].minerals[1],
                                  "Minerals Solid": planets[planet].minerals[2],
                                  "Sell Price Gas": planets[planet].price_sell[0],
                                  "Sell Price Liquid": planets[planet].price_sell[1],
                                  "Sell Price Solid": planets[planet].price_sell[2],
                                  "Minerals Need Gas": planets[planet].need[0],
                                  "Minerals Need Liquid": planets[planet].need[1],
                                  "Minerals Need Solid": planets[planet].need[2],
                                  "Buy Price Gas": planets[planet].price_buy[0],
                                  "Buy Price Liquid": planets[planet].price_buy[1],
                                  "Buy Price Solid": planets[planet].price_buy[2]}}
        # UPDATE VALUES
        collection.update(update_planet_selector, update_planet)

    for company in xrange(0, number_of_planets):
        update_company_selector = {"name": companies[company].name}
        update_company = {"$set": {
                           "Money": companies[company].company_money,
                           "profit": companies[company].profit,
                           "spent": companies[company].spent,
                           "expenses": companies[company].expenses,
                           "Stock Prices": companies[company].stock_price,
                           "Average Price Paid": companies[company].average_prices_bought_for,
                           "Minerals Gas": companies[company].company_minerals[0],
                           "Minerals Liquid": companies[company].company_minerals[1],
                           "Minerals Solid": companies[company].company_minerals[2],
                           "Minerals Gas in Transit Bought": companies[company].minerals_in_transit_bought[0],
                           "Minerals Liquid in Transit Bought": companies[company].minerals_in_transit_bought[1],
                           "Minerals Solid in Transit Bought": companies[company].minerals_in_transit_bought[2],
                           "Minerals Gas in Transit Sold": companies[company].minerals_in_transit_sell[0],
                           "Minerals Liquid in Transit Sold": companies[company].minerals_in_transit_sell[1],
                           "Minerals Solid in Transit Sold": companies[company].minerals_in_transit_sell[2],
                           "Trade List": companies[company].trade_list,
                           "Sell List": companies[company].sell_list
        }}
        collection.update(update_company_selector, update_company)

    update_best_prices_selector = {"Name": "Collator"}
    update_best_prices_info = {"$set": {"Elements": elements,
                                        "Elements Rarity": elements_rarity,
                                        "Low Prices Gas": mineral_low_sell_price[0],
                                        "Low Prices Liquid": mineral_low_sell_price[1],
                                        "Low Prices Solid": mineral_low_sell_price[2],
                                        "Best low prices Gas": mineral_best_sell_price[0],
                                        "Best low prices Liquid": mineral_best_sell_price[1],
                                        "Best low prices Solid": mineral_best_sell_price[2],
                                        "High Prices Gas": mineral_high_buy_price[0],
                                        "High Prices Liquid": mineral_high_buy_price[1],
                                        "High Prices Solid": mineral_high_buy_price[2],
                                        "Best high prices Gas": mineral_best_buy_price[0],
                                        "Best high prices Liquid": mineral_best_buy_price[1],
                                        "Best high prices Solid": mineral_best_buy_price[2]}}
    # UPDATE VALUES
    collection.update(update_best_prices_selector, update_best_prices_info)


