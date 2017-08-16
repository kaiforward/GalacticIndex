from create_system import CreateGalaxySize, Elements, Planet, Company, DataAggregator, FuelPrices  # import my classes
from create_system import create_all_planet_locations, create_all_company_locations  # import my classes
from my_mongo import my_mongo_insert, my_mongo_update

import time
import locale
import random
locale.setlocale(locale.LC_ALL, "")  # used to format some of the numbers in when printed

# galaxy_size = CreateGalaxySize()
# number_of_planets = galaxy_size.number_of_planets
# CHOOSE PLANET NUMBER ^^

number_of_planets = random.randint(20, 30)  # creates a number of planets, however many you want. try 1000 ;) (NO DON'T!)

# create all the universal Elements. Always 30 of them, these are the minerals traded between planets.
elements = Elements().create_elements()
elements_rarity = Elements().assign_minerals_rarity()

# CREATES THE PLANETS
planets = [Planet() for x in xrange(number_of_planets)]
location_list = create_all_planet_locations(number_of_planets, planets)

mineral_low_sell_price, mineral_best_sell_price = DataAggregator(planets, number_of_planets).mineral_lowest_sell_prices
# aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
mineral_high_buy_price, mineral_best_buy_price = DataAggregator(planets, number_of_planets).mineral_highest_buy_prices
# aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
fuel_change = 0  # declared here because company needs it as arg
tick = 0
# THIS IS THE COMPANY LOGIC
company_locations = create_all_company_locations(number_of_planets, location_list)
# assign company locations to existing planets locations ^^
companies = [Company(elements, location_list, number_of_planets, mineral_best_sell_price, mineral_best_buy_price, planets, fuel_change, tick, company_locations[company]) for company in xrange(number_of_planets)]

fuel_price = FuelPrices()
tags = ["GAS", "LIQUID", "SOLID"]
price_check = 0  # check with yoni how to use tick if i need to reset it?

collection = my_mongo_insert(
    number_of_planets,
    planets,
    mineral_low_sell_price,
    mineral_best_sell_price,
    mineral_high_buy_price,
    mineral_best_buy_price,
    companies,
    elements,
    elements_rarity
)

# BELOW IS WHERE ALL THE REPEATED FUNCTIONS ARE CARRIED OUT
for tick in xrange(1, 50000):
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
    for company in companies:
        company.stock_prices()
        company.remove_expenses()
        company.choose_to_improve()  # decide to improve size of spaceport or number of ships
        company.mineral_best_buy_prices = mineral_best_buy_price  # give company price data to work with
        company.mineral_best_sell_prices = mineral_best_sell_price
        company.fuel_price = fuel_price.fuel_price  # find fuel price for company
        company.total_fuel_cost = company.calculate_fuel_cost()  # find out the cost of fuel to each planet
        company.profit_potential = company.evaluate_planet_prices()
        # company evaluates the prices seeing which mineral has the most potential for profit
        company.profit_minus_fuel = company.take_cost_of_fuel_per_unit()  # take that cost away from the profit potential
        company.tick = tick

        company.purchase = company.decide_to_buy()
        purchase = company.purchase

        company.sale = company.sell_minerals()
        sale = company.sale

        for planet in xrange(0, number_of_planets):  # cycles through each planet
            planets[planet].remove_minerals(purchase)  # remove minerals from planets when companies purchase them
            planets[planet].buy_minerals(sale)  # add minerals to planets planets when companies make a sale to them

        mineral_low_sell_price, mineral_best_sell_price = DataAggregator(planets, number_of_planets).mineral_lowest_sell_prices
        # aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
        mineral_high_buy_price, mineral_best_buy_price = DataAggregator(planets, number_of_planets).mineral_highest_buy_prices
        # aggregates all planets sell price data and sorts it into two lists, one of every price and one of the best prices
        # NEED TO WORK OUT HOW TO ORDER THE SELL DATA PERHAPS USING SORT(), IT ONLY NEEDS ORDERING FOR VIEWERS LEGIBILITY

    if tick >= 1000:
        # time.sleep(1)

        # PRINTING --------------------------------------------------------------------------------------------------
        for planet in planets:
            # planet = planets[int(raw_input("Choose planet number to view"))]
            print "---------------------------------------------------------------------"
            print "Planet Name -", planet.name
            print "locations   -", planet.location
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
        for company in companies:
            print "---------------------------"
            print "Company name", company.name
            print "PLANET DISTANCES", company.planet_distances
            print "Company Location", company.company_locations
            print "Company Money", locale.format('%d', company.company_money, grouping=True)
            print "Company Profit",  locale.format('%d', company.profit, grouping=True)
            print "Company Spent", locale.format('%d', company.spent, grouping=True)
            print "Company Expenses", locale.format('%d', company.expenses, grouping=True)
            print 'SIZE OF SPACEPORT', company.number_of_spaceports
            print "NUMBER OF SHIPS", company.number_of_ships
            print ""
            print "Company Profit Potential list-", company.profit_potential
            print "Company fuel cost            -", company.total_fuel_cost
            print "Profit Potential After Fuel  -", company.profit_minus_fuel
            print ""
            print "Company Minerals", company.company_minerals
            print "Average Price Paid", company.average_prices_bought_for
            print 'minerals in transit bought', company.minerals_in_transit_bought
            print 'minerals in transit sell', company.minerals_in_transit_sell
            print ""
            print "PURCHASE", company.purchase
            print "PURCHASE LIST", company.trade_list
            print 'SALE', company.sale
            print 'SALE LIST', company.sell_list
            print "Company Timer", company.tick
            print ""
        print "GALAXY STATISTICS -------------------------"
        print elements_rarity
        print elements
        print "Fuel Price", fuel_price.fuel_price
        print "Galactic Cycle", tick
        print "-------------------------------------------"
        for mineral_group in xrange(0, 3):
            print "BEST LOW SELL PRICE-", tags[mineral_group], mineral_best_sell_price[mineral_group]
        for mineral_group in xrange(0, 3):
            print "BEST HIGH BUY PRICE-", tags[mineral_group], mineral_best_buy_price[mineral_group]

    my_mongo_update(number_of_planets,
                    planets,
                    mineral_low_sell_price,
                    mineral_best_sell_price,
                    mineral_high_buy_price,
                    mineral_best_buy_price,
                    collection,
                    companies,
                    elements,
                    elements_rarity
                    )



