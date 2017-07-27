from create_system import CreateGalaxySize, Elements, Planet, Company  # import my classes
from my_mongo import mongo_connect

import time

mongo_connect()  # MONGO CONNECTION FUNCTION

galaxy_size = CreateGalaxySize()
number_of_planets = galaxy_size.number_of_planets

# create all the universal Elements. 30 of them, these are the minerals traded between planets.
elements = Elements().create_elements()
elements_rarity = Elements().assign_minerals_rarity()

# creates a number of planets, however many you want. try 1000
planets = [Planet() for x in xrange(number_of_planets)]

# THIS IS THE COMPANY LOGIC
company = Company()
company.find_distance_of_planets(number_of_planets)

price_check = 0

# MY MONGO INSERT BITS ----------------------
conn = mongo_connect()
db = conn['Galactic_stream']
coll = db.my_galactic_test
docs = []

coll.drop()  # remove the collection
# CREATE INITIAL INSERT OF ALL PLANETS
for planet in xrange(0, number_of_planets):
    doc = [{"name": planets[planet].name, "Habitable": planets[planet].habitable, "Climate": planets[planet].climate,
            "Economic Status": planets[planet].economic, "Minerals": planets[planet].minerals,
            "Sell Price": planets[planet].price_sell, "Minerals Need": planets[planet].need,
            "Buy Price": planets[planet].price_buy}]
    # INSERT FIRST PLANET
    coll.insert(doc)
# -------------------------------------------

for tick in xrange(1, 8000):
    # simulation ticks
    price_check += 1
    # THIS IS THE PLANET ECONOMY CHANGE LOGIC
    for planet in xrange(0, number_of_planets):  # cycles through each planet
        planets[planet].add_minerals(elements_rarity)  # Add and removes different levels of minerals from a planet
        planets[planet].find_mineral_need()  # finds out what minerals a planet needs
        if price_check >= 100:  # resets max price every 500 ticks, so max price is for example that days changes.
            planets[planet].max_price_buy = [[0]*10, [0]*10, [0]*10]
            planets[planet].max_price_sell = [[0]*10, [0]*10, [0]*10]
            planets[planet].low_price_buy = [[100000]*10, [100000]*10, [100000]*10]
            planets[planet].low_price_sell = [[100000]*10, [100000]*10, [100000]*10]
            price_check = 0
        planets[planet].find_max_prices()  # finds the highs and lows of thew buy and sell prices.
        planets[planet].find_price(elements_rarity)  # Calculates the buy and sell price of each mineral on a planet

    if tick >= 7000:
        time.sleep(1)
        for planet2 in xrange(len(planets)):
            current = planets[planet2]
            # current = planets[int(raw_input("Choose planet number to view"))]
            print "---------------------------------------------------------------------"
            print "Planet Name -", current.name
            print "Habitable -", current.habitable
            print "Climate -", current.climate
            print "Economic Status -", current.economic
            print ""
            print "required minerals -", current.total_increase[1]
            print "Produced minerals -", current.total_decrease[1]
            print "Production Change -", current.production_chance[1]
            print "Required Change   -", current.requirement_chance[1]
            print ""
            print "Minerals Levels   -", current.minerals[1]
            print "Sell Price        -", current.price_sell[1]
            print "Hours High Sell P -", current.max_price_sell[1]
            print "Hours low Sell P  -", current.low_price_sell[1]
            print "Turns prod inc/dec-", current.how_many_times_production_changed[1]
            print ""
            print "Minerals Needed   -", current.need[1]
            print "Minerals BuyPrice -", current.price_buy[1]
            print "Hours High Buy P  -", current.max_price_buy[1]
            print "Hours low Buy P   -", current.low_price_buy[1]
            print "Turns requ inc/dec-", current.how_many_times_requirement_changed[1]
            print "---------------------------------------------------------------------"
            # company statistics
            print "Company name", company.name
            print "Company Distance from planets", company.distance_from_planets

    # MY MONGO UPDATE CALLED EVERY TICK TO UPDATE NEW PLANET VALUES.
    # CREATE UPDATE
    for planet in xrange(0, number_of_planets):
        update_doc_selector = {"name": planets[planet].name}
        update_doc = {"$set": {"Minerals": planets[planet].minerals, "Sell Price": planets[0].price_sell,
                               "Minerals Need": planets[planet].need,
                               "Buy Price": planets[planet].price_buy}}
        # UPDATE VALUES
        coll.update(update_doc_selector, update_doc)

print elements_rarity
print elements



