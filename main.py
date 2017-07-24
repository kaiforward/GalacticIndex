from create_system import Elements, Planet  # import my classes

number_of_planets = int(raw_input("Choose how many planets"))

elements = Elements().create_elements()
elements_rarity = Elements().assign_minerals_rarity()

planets = [Planet() for x in xrange(number_of_planets)]

for tick in xrange(1, 1000):
    for planet in xrange(0, number_of_planets):
        planets[planet].add_minerals(elements_rarity)
        planets[planet].find_mineral_need()
        planets[planet].find_price(elements_rarity)
    # time.sleep(1)

for planet2 in xrange(len(planets)):
    current = planets[planet2]
    # current = planets[int(raw_input("Choose planet number to view"))]
    print "Planet Name -", current.name
    print "Habitable -", current.habitable
    print "Climate -", current.climate
    print "Economic Status -", current.economic
    print "required -", current.requirement
    print "Products -", current.production
    print "Pro Chan -", current.production_chance
    print "Req Chan -", current.requirement_chance
    print "Minerals -", current.minerals
    print "Cur Need -", current.need
    print "sell Pri -", current.price_sell
    print "Buy Pric -", current.price_buy
    print ""

print elements_rarity
print elements

