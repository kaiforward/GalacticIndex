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
    planet_collection = database.planets
    company_collection = database.companies
    return planet_collection, company_collection


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

    def mineral_data(mineral_group, mineral_id):
        return {
            "name": elements[mineral_group][mineral_id],
            "amount": planets[planet].chart_minerals[mineral_group][mineral_id],
            "need": planets[planet].chart_need[mineral_group][mineral_id],
            "SellPrice": planets[planet].price_sell[mineral_group][mineral_id],
            "BuyPrice":  planets[planet].price_buy[mineral_group][mineral_id],
            "HighSellPrice": planets[planet].max_price_sell[mineral_group][mineral_id],
            "LowSellPrice": planets[planet].low_price_sell[mineral_group][mineral_id],
            "HighBuyPrice": planets[planet].max_price_buy[mineral_group][mineral_id],
            "LowBuyPrice": planets[planet].low_price_buy[mineral_group][mineral_id],
            "ChartSellPrice": planets[planet].chart_price_sell[mineral_group][mineral_id],
            "ChartBuyPrice": planets[planet].chart_price_buy[mineral_group][mineral_id],
            "ChartMaxBuyPrice": planets[planet].chart_max_price_sell[mineral_group][mineral_id],
            "ChartMaxSellPrice": planets[planet].chart_max_price_buy[mineral_group][mineral_id],
        }

    def company_mineral_data(mineral_group, mineral_id):
        return {
            "name": elements[mineral_group][mineral_id],
            "AveragePricePaid": companies[company].average_prices_bought_for[mineral_group][mineral],
            "Amount": companies[company].company_minerals[mineral_group][mineral],
            "MineralsInTransitBought": companies[company].minerals_in_transit_bought[mineral_group][mineral],
            "MineralsInTransitSold": companies[company].minerals_in_transit_sell[mineral_group][mineral],
        }

    planet_collection, company_collection = open_collection()
    planet_collection.drop()  # remove the collection
    company_collection.drop()  # remove the collection
    # CREATE INITIAL INSERT OF ALL PLANETS

    for planet in xrange(0, number_of_planets):
        gasses = []
        liquids = []
        solids = []
        for mineral in xrange(0, 10):
            gasses.append(mineral_data(0, mineral))
            liquids.append(mineral_data(1, mineral))
            solids.append(mineral_data(2, mineral))
        insert_planet = [{"PlanetName": planets[planet].name,
                          "Habitability": planets[planet].habitable,
                          "Climate": planets[planet].climate,
                          "Location": planets[planet].location,
                          "EconomicStatus": planets[planet].economic,
                          "Population": planets[planet].population,
                          "LandSpecies": planets[planet].planet_features[0],
                          "PlantSpecies": planets[planet].planet_features[1],
                          "MarineSpecies": planets[planet].planet_features[2],
                          "MineralsGas": gasses,  # made a loop to insert these! yay!
                          "MineralsLiquid": liquids,
                          "MineralsSolid": solids,
                          }]
        # INSERT FIRST PLANET
        planet_collection.insert(insert_planet)

    for company in xrange(0, number_of_planets):
        comp_gasses = []
        comp_liquids = []
        comp_solids = []
        for mineral in xrange(0, 10):
            comp_gasses.append(company_mineral_data(0, mineral))
            comp_liquids.append(company_mineral_data(1, mineral))
            comp_solids.append(company_mineral_data(2, mineral))
        insert_company = [{"CompanyName": companies[company].name,
                           "Money": companies[company].company_money,
                           "profit": companies[company].profit,
                           "spent": companies[company].spent,
                           "expenses": companies[company].expenses,
                           "StockPrices": companies[company].stock_price,
                           "MineralsGas": comp_gasses,
                           "MineralsLiquid": comp_liquids,
                           "MineralsSolid": comp_solids,
                           "TradeList": companies[company].trade_list,
                           "SellList": companies[company].sell_list,
                           "NumberOfSpaceports": companies[company].number_of_spaceports,
                           "NumberOfSpaceships": companies[company].number_of_ships,
                           "CompanyAge": companies[company].company_age,
                           }]
        company_collection.insert(insert_company)

    return planet_collection, company_collection


def my_mongo_update(
        number_of_planets,
        planets,
        mineral_low_sell_price,
        mineral_best_sell_price,
        mineral_high_buy_price,
        mineral_best_buy_price,
        planet_collection,
        companies,
        elements,
        elements_rarity,
        company_collection):
    # MY MONGO UPDATE CALLED EVERY TICK TO UPDATE NEW PLANET VALUES.
    # CREATE UPDATE

    def mineral_data(mineral_group, mineral_id):
        return {
            "name": elements[mineral_group][mineral_id],
            "amount": planets[planet].chart_minerals[mineral_group][mineral_id],
            "need": planets[planet].chart_need[mineral_group][mineral_id],
            "SellPrice": planets[planet].price_sell[mineral_group][mineral_id],
            "BuyPrice":  planets[planet].price_buy[mineral_group][mineral_id],
            "HighSellPrice": planets[planet].max_price_sell[mineral_group][mineral_id],
            "LowSellPrice": planets[planet].low_price_sell[mineral_group][mineral_id],
            "HighBuyPrice": planets[planet].max_price_buy[mineral_group][mineral_id],
            "LowBuyPrice": planets[planet].low_price_buy[mineral_group][mineral_id],
            "ChartSellPrice": planets[planet].chart_price_sell[mineral_group][mineral_id],
            "ChartBuyPrice": planets[planet].chart_price_buy[mineral_group][mineral_id],
            "ChartMaxBuyPrice": planets[planet].chart_max_price_sell[mineral_group][mineral_id],
            "ChartMaxSellPrice": planets[planet].chart_max_price_buy[mineral_group][mineral_id]
        }

    def company_mineral_data(mineral_group, mineral_id):
        return {
            "name": elements[mineral_group][mineral_id],
            "AveragePricePaid": companies[company].average_prices_bought_for[mineral_group][mineral],
            "Amount": companies[company].company_minerals[mineral_group][mineral],
            "MineralsInTransitBought": companies[company].minerals_in_transit_bought[mineral_group][mineral],
            "MineralsInTransitSold": companies[company].minerals_in_transit_sell[mineral_group][mineral],
        }

    for planet in xrange(0, number_of_planets):
        gasses = []
        liquids = []
        solids = []
        for mineral in xrange(0, 10):
            gasses.append(mineral_data(0, mineral)),
            liquids.append(mineral_data(1, mineral)),
            solids.append(mineral_data(2, mineral))

        update_planet_selector = {"PlanetName": planets[planet].name}
        update_planet = {"$set": {"Population": planets[planet].population,
                                  "EconomicStatus": planets[planet].economic,
                                  "MineralsGas": gasses,  # made a loop to insert these! yay!
                                  "MineralsLiquid": liquids,
                                  "MineralsSolid": solids,
                                  }}
        # UPDATE VALUES
        planet_collection.update(update_planet_selector, update_planet)

    for company in xrange(0, number_of_planets):
        comp_gasses = []
        comp_liquids = []
        comp_solids = []
        for mineral in xrange(0, 10):
            comp_gasses.append(company_mineral_data(0, mineral))
            comp_liquids.append(company_mineral_data(1, mineral))
            comp_solids.append(company_mineral_data(2, mineral))
        update_company_selector = {"CompanyName": companies[company].name}
        update_company = {"$set": {
                           "Money": companies[company].company_money,
                           "profit": companies[company].profit,
                           "spent": companies[company].spent,
                           "expenses": companies[company].expenses,
                           "StockPrices": companies[company].stock_price,
                           "MineralsGas": comp_gasses,
                           "MineralsLiquid": comp_liquids,
                           "MineralsSolid": comp_solids,
                           "TradeList": companies[company].trade_list,
                           "SellList": companies[company].sell_list,
                           "NumberOfSpaceports": companies[company].number_of_spaceports,
                           "NumberOfSpaceships": companies[company].number_of_ships,
                           "CompanyAge": companies[company].company_age,
        }}
        company_collection.update(update_company_selector, update_company)
