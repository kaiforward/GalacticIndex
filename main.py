from create_system import Elements, Planet  # import my classes

number_of_planets = int(raw_input("Choose how many planets"))

# create all the universal Elements. 30 of them, these are the minerals traded between planets.
elements = Elements().create_elements()
elements_rarity = Elements().assign_minerals_rarity()

# creates a number of planets, however many you want.
planets = [Planet() for x in xrange(number_of_planets)]

price_check = 0

for tick in xrange(1, 1000):
    # simulation ticks
    price_check += 1
    for planet in xrange(0, number_of_planets):  # cycles through each planet
        planets[planet].add_minerals(elements_rarity)  # Add and removes different levels of minerals from a planet
        planets[planet].find_mineral_need()  # finds out what minerals a planet needs
        if price_check >= 500:  # resets max price every 500 ticks, so max price is for example that days changes.
            planets[planet].max_price_buy = [[0]*10, [0]*10, [0]*10]
            planets[planet].max_price_sell = [[0]*10, [0]*10, [0]*10]
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
    print "required -", current.total_increase
    print "Products -", current.total_decrease
    print "Pro Chan -", current.production_chance
    print "Req Chan -", current.requirement_chance
    print "Minerals -", current.minerals
    print "Sell Pri -", current.price_sell
    print "Max-sell -", current.max_price_sell
    print "Cur Need -", current.need
    print "BuyPrice -", current.price_buy
    print "Max--Buy -", current.max_price_buy


print elements_rarity
print elements

