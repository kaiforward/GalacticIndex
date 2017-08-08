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
        mineral_best_buy_price):

    collection = open_collection()
    collection.drop()  # remove the collection
    # CREATE INITIAL INSERT OF ALL PLANETS
    for planet in xrange(0, number_of_planets):
        insert_planet = [{"name": planets[planet].name, "Habitable": planets[planet].habitable, "Climate": planets[planet].climate,
                          "Location": planets[planet].location, "Economic Status": planets[planet].economic,
                          "Minerals Gas": planets[planet].minerals[0], "Minerals Liquid": planets[planet].minerals[1],
                          "Minerals Solid": planets[planet].minerals[2], "Sell Price": planets[planet].price_sell,
                          "Minerals Need": planets[planet].need, "Buy Price": planets[planet].price_buy}]
        # INSERT FIRST PLANET
        collection.insert(insert_planet)

    # NEED TO WORK OUT HOW TO ORDER THE SELL DATA PERHAPS USING SORT(), IT ONLY NEEDS ORDERING FOR VIEWERS LEGIBILITY
    insert_high_low_prices = [
        {"Name": "Collator", "Low Prices": mineral_low_sell_price, "Best low prices": mineral_best_sell_price,
         "High Prices": mineral_high_buy_price, "Best high prices": mineral_best_buy_price}]
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
        collection):
    # MY MONGO UPDATE CALLED EVERY TICK TO UPDATE NEW PLANET VALUES.
    # CREATE UPDATE
    for planet in xrange(0, number_of_planets):
        update_doc_selector = {"name": planets[planet].name}
        update_doc = {"$set": {"Minerals Gas": planets[planet].minerals[0], "Minerals Liquid": planets[planet].minerals[1],
                               "Minerals Solid": planets[planet].minerals[2], "Sell Price": planets[planet].price_sell,
                               "Minerals Need": planets[planet].need,
                               "Buy Price": planets[planet].price_buy}}
        # UPDATE VALUES
        collection.update(update_doc_selector, update_doc)

    update_best_prices_selector = {"Name": "Collator"}
    update_best_prices_info = {"$set": {"Low Prices": mineral_low_sell_price, "Best low prices": mineral_best_sell_price,
                                        "High Prices": mineral_high_buy_price, "Best high prices": mineral_best_buy_price}}
    # UPDATE VALUES
    collection.update(update_best_prices_selector, update_best_prices_info)


