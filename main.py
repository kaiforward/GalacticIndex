from create_system import CreateGalaxySize, Elements, Planet, Company, DataAggregator, FuelPrices  # import my classes
from create_system import create_locations  # import my classes
from my_mongo import mongo_connect

import time
import locale
import random
locale.setlocale(locale.LC_ALL, "")


mongo_connect()  # MONGO CONNECTION FUNCTION

# galaxy_size = CreateGalaxySize()
# number_of_planets = galaxy_size.number_of_planets
# CHOOSE PLANET NUMBER ^^

number_of_planets = random.randint(5, 10)

# create all the universal Elements. Always 30 of them, these are the minerals traded between planets.
elements = Elements().create_elements()
elements_rarity = Elements().assign_minerals_rarity()

# CREATES THE PLANETS creates a number of planets, however many you want. try 1000 ;) (NO DON'T!)
planets = [Planet() for x in xrange(number_of_planets)]

# CREATES A LIST OF LOCATIONS, IS USED HERE SO REPEATS WILL BE RECOGNISED
location_list = []
for planet in xrange(0, number_of_planets):
    planets[planet].create_pop()
    current_location = create_locations()
    if current_location in location_list:  # if planet random location already used
        current_location = create_locations()
    location_list.append(current_location)
    planets[planet].location = location_list[planet]

# MY MONGO INSERT BITS ----------------------
connect_to_mongo = mongo_connect()
database = connect_to_mongo['Galactic_stream']
collection = database.my_galactic_test

collection.drop()  # remove the collection
# CREATE INITIAL INSERT OF ALL PLANETS
for planet in xrange(0, number_of_planets):
    insert_planet = [{"name": planets[planet].name, "Habitable": planets[planet].habitable, "Climate": planets[planet].climate,
                      "Location": planets[planet].location, "Economic Status": planets[planet].economic,
                      "Minerals": planets[planet].minerals, "Sell Price": planets[planet].price_sell,
                      "Minerals Need": planets[planet].need, "Buy Price": planets[planet].price_buy}]
    # INSERT FIRST PLANET
    collection.insert(insert_planet)

mineral_low_sell_price, mineral_best_sell_price = DataAggregator(planets, number_of_planets).mineral_lowest_sell_prices
# aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
mineral_high_buy_price, mineral_best_buy_price = DataAggregator(planets, number_of_planets).mineral_highest_buy_prices
# aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
fuel_change = 0  # declared here because company needs it as arg
tick = 0
# THIS IS THE COMPANY LOGIC
company = Company(elements, location_list, number_of_planets, mineral_best_sell_price, mineral_best_buy_price, planets, fuel_change, tick)

# NEED TO WORK OUT HOW TO ORDER THE SELL DATA PERHAPS USING SORT(), IT ONLY NEEDS ORDERING FOR VIEWERS LEGIBILITY
insert_high_low_prices = [{"Name": "Collator", "Low Prices": mineral_low_sell_price, "Best low prices": mineral_best_sell_price,
                           "High Prices": mineral_high_buy_price, "Best high prices": mineral_best_buy_price}]
collection.insert(insert_high_low_prices)
# -------------------------------------------

fuel_price = FuelPrices()

tags = ["gas", "liquid", "solid"]
price_check = 0  # check with yoni how to use tick if i need to reset it?


# BELOW IS WHERE ALL THE REPEATED FUNCTIONS ARE CARRIED OUT
for tick in xrange(1, 10000):
    # simulation ticks
    price_check += 1
    fuel_change += 1
    # THIS IS THE PLANET ECONOMY CHANGE LOGIC
    for planet in xrange(0, number_of_planets):  # cycles through each planet
        planets[planet].decide_economic_status()
        planets[planet].add_minerals(elements_rarity)  # Add and removes different levels of minerals from a planet
        planets[planet].find_mineral_need()  # finds out what minerals a planet needs
        planets[planet].find_price(elements_rarity)  # Calculates the buy and sell price of each mineral on a planet
        planets[planet].find_max_prices()  # finds the highs and lows of the buy and sell prices.
        if price_check >= 100:  # resets max price every 500 ticks, so max price is for example that days changes.
            for planet2 in xrange(0, number_of_planets):  # RESET FOR EVERY PLANET
                planets[planet2].reset_max_prices()
                price_check = 0
    if fuel_change >= 20:
        fuel_price.fuel_prices()
        fuel_change = 0

    mineral_low_sell_price, mineral_best_sell_price = DataAggregator(planets, number_of_planets).mineral_lowest_sell_prices
    # aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
    mineral_high_buy_price, mineral_best_buy_price = DataAggregator(planets, number_of_planets).mineral_highest_buy_prices
    # aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
    # NEED TO WORK OUT HOW TO ORDER THE SELL DATA PERHAPS USING SORT(), IT ONLY NEEDS ORDERING FOR VIEWERS LEGIBILITY

    company.mineral_best_buy_prices = mineral_best_buy_price  # give company price data to work with
    company.mineral_best_sell_prices = mineral_best_sell_price
    company.fuel_price = fuel_price.fuel_price  # find fuel price for company
    fuel_cost = company.calculate_fuel_cost()  # find out the cost of fuel to each planet
    company_profit_potential = company.evaluate_planet_prices()
    # company evalutates the prices seeing which mineral has the most potential for profit
    profit_minus_fuel_cost = company.take_cost_of_fuel_per_unit()  # take that cost away from the profit potential

    company.tick = tick

    if tick >= 1000:
        time.sleep(1)

        company.purchase = company.decide_to_buy()
        company.sale = company.sell_minerals()
        purchase = company.purchase
        sale = company.sale

        planets[planet].remove_minerals(purchase)
        planets[planet].buy_minerals(sale)

        for planet in planets:
            # planet = planets[int(raw_input("Choose planet number to view"))]
            print "---------------------------------------------------------------------"
            print "Planet Name -", planet.name
            print "Habitable -", planet.habitable
            print "Climate -", planet.climate
            print "Economic Status -", planet.economic
            print "Population      -", locale.format('%d', planet.population, grouping=True)
            print "Max Production  -", planet.max_production
            print "Max Requirement -", planet.max_requirement
            print "Max/min possible chance prod", planet.max_low_chance_prod
            print "Max/min possible chance req", planet.max_low_chance_req
            print ""
            print "Produced minerals -", planet.total_increase
            print "Required Minerals-", planet.total_decrease
            print "Production Change -", planet.production_chance
            print "Required Change   -", planet.requirement_chance
            print ""
            print "Minerals Levels   -", planet.minerals
            print "Sell Price        -", planet.price_sell
            print "MAX PRICE SELL    -", planet.max_price_sell
            print "LOW PRICE SELL    -", planet.low_price_sell
            print "Turns prod inc/dec-", planet.how_many_times_production_changed
            print ""
            print "Minerals Needed   -", planet.need
            print "Minerals BuyPrice -", planet.price_buy
            print "HIGH PRICE BUY    -", planet.max_price_buy
            print "LOW PRICE BUY     -", planet.low_price_buy
            print "Turns requ inc/dec-", planet.how_many_times_requirement_changed
            print "---------------------------------------------------------------------"
            # company statistics
            print "Company name", company.name
        print "PLANET DISTANCES", company.planet_distances
        print "Company Location", company.company_locations
        # for min_g in xrange(0, 3):
        #     for mineral in xrange(0, 10):
        #         print "MINERAL LOW SELL PRICE  -", elements[min_g][mineral], mineral_low_sell_price[min_g][mineral]
        #         print "MINERAL HIGH BUY PRICE  -", elements[min_g][mineral], mineral_high_buy_price[min_g][mineral]
        for mineral_group in xrange(0, 3):
            print "BEST LOW SELL PRICE-", tags[mineral_group], mineral_best_sell_price[mineral_group]
        for mineral_group in xrange(0, 3):
            print "BEST HIGH BUY PRICE-", tags[mineral_group], mineral_best_buy_price[mineral_group]
        print "Company Profit Potential list-", company_profit_potential
        print "Company fuel cost            -", fuel_cost
        print "Profit Potential After Fuel  -", profit_minus_fuel_cost
        print "Company Money", company.company_money
        print "Company Minerals", company.company_minerals
        print "Average Price Paid", company.average_prices_bought_for
        print "PURCHASE", company.purchase
        print "PURCHASE LIST", company.trade_list
        print 'SALE', company.sale
        print 'SALE LIST', company.sell_list
        print elements_rarity
        print elements
        print fuel_price.fuel_price
        print company.tick
        print tick

    # MY MONGO UPDATE CALLED EVERY TICK TO UPDATE NEW PLANET VALUES.
    # CREATE UPDATE
    for planet in xrange(0, number_of_planets):
        update_doc_selector = {"name": planets[planet].name}
        update_doc = {"$set": {"Minerals": planets[planet].minerals, "Sell Price": planets[planet].price_sell,
                               "Minerals Need": planets[planet].need,
                               "Buy Price": planets[planet].price_buy}}
        # UPDATE VALUES
        collection.update(update_doc_selector, update_doc)

    update_best_prices_selector = {"Name": "Collator"}
    update_best_prices_info = {"$set": {"Low Prices": mineral_low_sell_price, "Best low prices": mineral_best_sell_price,
                                        "High Prices": mineral_high_buy_price, "Best high prices": mineral_best_buy_price}}
    # UPDATE VALUES
    collection.update(update_best_prices_selector, update_best_prices_info)





