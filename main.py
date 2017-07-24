from create_system import Elements, Planet  # import my classes

number_of_planets = int(raw_input("Choose how many planets"))

# create all the universal Elements. 30 of them, these are the minerals traded between planets.
elements = Elements().create_elements()
elements_rarity = Elements().assign_minerals_rarity()

# creates a number of planets, however many you want.
planets = [Planet() for x in xrange(number_of_planets)]

price_check = 0

for tick in xrange(1, 10000):
    # simulation ticks
    price_check += 1
    for planet in xrange(0, number_of_planets):  # cycles through each planet
        planets[planet].add_minerals(elements_rarity)  # Add and removes different levels of minerals from a planet
        planets[planet].find_mineral_need()  # finds out what minerals a planet needs
        if price_check >= 1800:  # resets max price every 500 ticks, so max price is for example that days changes.
            planets[planet].max_price_buy = [[0]*10, [0]*10, [0]*10]
            planets[planet].max_price_sell = [[0]*10, [0]*10, [0]*10]
            planets[planet].low_price_buy = [[100000]*10, [100000]*10, [100000]*10]
            planets[planet].low_price_sell = [[100000]*10, [100000]*10, [100000]*10]
            price_check = 0
        planets[planet].find_max_prices()
        planets[planet].find_price(elements_rarity)  # Calculates the buy and sell price of each mineral on a planet
        # time.sleep(1)


for planet2 in xrange(len(planets)):
    current = planets[planet2]
    # current = planets[int(raw_input("Choose planet number to view"))]
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
    print ""

print elements_rarity
print elements

