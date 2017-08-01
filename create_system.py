import random
import string
from language import create_word

CLIMATE_MODIFIERS = {  # used in planet class
    # climate modifier where 0, 1 and 2 of array are gas, liquid, solid respectively
    'Tropical': [1.15, 1, 1],  # higher levels of gas
    'Oceanic': [1, 1.3, 0.8],  # higher level of liquid, less solid
    'rocky': [1, 0.95, 1.25],  # higher level of solid, slightly less solid
    'desert': [1, 0.5, 1.25],  # more solid, much less liquid
    'Gas Giant': [1.4, 0.8, 0.8],  # much higher gas, less liquid, less solid
    'Toxic': [1.15, 1.15, 1],  # higher gas, liquid, less solid
    'Frozen': [1, 1.25, 1],  # higher liquid
    'Metallic': [1, 0.8, 1.3],  # much higher solid
    'Barren': [0.8, 0.8, 1.25],  # higher solid, less gas and liquid
}


def create_locations():
        location = [random.randint(1, 100), random.randint(1, 100)]
        previous_location = location
        while location == previous_location:
            location = [random.randint(1, 100), random.randint(1, 100)]
        return location


class CreateGalaxySize(object):
    # The class "constructor"
    def __init__(self):
        self.number_of_planets = self.choose_number_of_planets()

    def choose_number_of_planets(self):
        number_of_planets = int(raw_input("Choose how many planets"))
        return number_of_planets


class FuelPrices(object):

    def __init__(self):
        self.fuel_price = 5

    def fuel_prices(self):
        random_change = random.random()
        if random_change > 0.5:
            self.fuel_price += 0.5
            if self.fuel_price > 10:
                self.fuel_price = 10
        if random_change < 0.5:
            self.fuel_price -= 0.5
            if self.fuel_price < 1:
                self.fuel_price = 1
        return self.fuel_price


class Planet(object):  # Planet class creates all variables for individual planets
    # The class "constructor"
    def __init__(self):

        # SO MANY VARIABLES!
        climate, habitable = self.create_climate()  # get planet habitability and climate

        self.name = create_word(2, 3)  # creates random Planet Name
        self.habitable = habitable  # defines whether planet is habitable
        self.climate = climate  # based on habitability a climate is assigned
        self.location = [0, 0]  # Location not set inside class as it must be unique from other planets
        self.economic = random.randint(1, 10)  # not used yet
        # using too many individual variables below, used 3 times more when i split the elements though >_<
        self.minerals = [[0]*10, [0]*10, [0]*10]
        self.production = [[20]*10, [20]*10, [20]*10]
        self.requirement = [[20]*10, [20]*10, [20]*10]
        self.total_increase = [[0]*10, [0]*10, [0]*10]
        self.total_decrease = [[0]*10, [0]*10, [0]*10]
        self.production_chance = [[50]*10, [50]*10, [50]*10]
        self.requirement_chance = [[50]*10, [50]*10, [50]*10]
        self.need = [[0]*10, [0]*10, [0]*10]
        self.price_sell = [[0]*10, [0]*10, [0]*10]
        self.price_buy = [[0]*10, [0]*10, [0]*10]
        self.max_price_sell = [[0]*10, [0]*10, [0]*10]
        self.low_price_sell = [[0]*10, [0]*10, [0]*10]
        self.max_price_buy = [[0]*10, [0]*10, [0]*10]
        self.low_price_buy = [[0]*10, [0]*10, [0]*10]
        self.how_many_times_production_changed = [[0]*10, [0]*10, [0]*10]
        self.how_many_times_requirement_changed = [[0] * 10, [0] * 10, [0] * 10]

    def create_climate(self):
        # RANDOMLY DECIDES WHETHER PLANET IS HABITABLE, IF IT IS HABITABLE IT CHOOSES WHAT CLIMATE IT IS
        decide_if_habitable = random.random()
        randomize_climate = ["Continental", "Tropical", "Oceanic", "Desert", "Rocky", "Arctic"]
        randomize_barren = ["Barren World", "Gas Giant", "Metallic World", "Frozen World", "Toxic World"]
        if decide_if_habitable >= 0.25:  # habitable
            current_climate = random.choice(randomize_climate)
            current_habitable = "Habitable"
        else:  # not habitable
            current_climate = random.choice(randomize_barren)
            current_habitable = "Inhabitable"
        return current_climate, current_habitable

    def add_minerals(self, element_rarity):

        # imports the mineral rarity variables to be used later on
        gas_rarity = element_rarity[0]
        liquid_rarity = element_rarity[1]
        solid_rarity = element_rarity[2]
        all_minerals_rarity = [gas_rarity, liquid_rarity, solid_rarity]

        # defines the maximum low chance and high chance of planet minerals changing. so 90 sort of equates to 90% percent chance
        low_chance = 40
        high_chance = 60

        # finds the planet climate and adds a climate modifier to results of mineral production
        # there maybe a better way of doing this??? PUT INTO DICTIONARY
        current_climate = self.climate
        climate_modifier = CLIMATE_MODIFIERS[current_climate]

        for mineral_group in xrange(0, 3):
            # 1st loop cycles through mineral groups
            for mineral in xrange(0, 10):
                # 2nd loop cycles through each mineral
                chance_of_prod = random.randint(1, 100)
                chance_of_req = random.randint(1, 100)
                # generate random number for comparison, that decides whether production or requirement levels change

                prod_chances = self.production_chance[mineral_group]
                if chance_of_prod <= prod_chances[mineral]:
                    # if the chance of production is less than the random chance_of_prod, mineral production improves
                    prod_chances[mineral] += random.randint(1, 3)
                    # better chance of improving next time
                    self.production[mineral_group][mineral] += 1  # Higher increase next time
                    self.minerals[mineral_group][mineral] += (self.production[mineral_group][mineral] *
                                                              climate_modifier[mineral_group]) / all_minerals_rarity[mineral_group][mineral]
                    # ^too long line, adds the planet amount of mineral production with modifiers to overall mineral level.
                    if prod_chances[mineral] > high_chance:
                        prod_chances[mineral] = high_chance
                    # makes sure chance of changing never goes above the set limits
                    if self.how_many_times_production_changed[mineral_group][mineral] < 0:
                        # if production was previously decreasing reset counter
                        self.how_many_times_production_changed[mineral_group][mineral] = 0
                    self.how_many_times_production_changed[mineral_group][mineral] += 1
                    # measures how many times production has improved in a row
                # these further elif does the same as above but with the reverse effect of mineral production decreasing slightly
                elif chance_of_prod > prod_chances[mineral]:
                    prod_chances[mineral] -= random.randint(1, 3)
                    self.production[mineral_group][mineral] -= 1
                    self.minerals[mineral_group][mineral] += (self.production[mineral_group][mineral] *
                                                              climate_modifier[mineral_group]) / all_minerals_rarity[mineral_group][mineral]
                    if prod_chances[mineral] < low_chance:
                        prod_chances[mineral] = low_chance
                    if self.how_many_times_production_changed[mineral_group][mineral] > 0:
                        self.how_many_times_production_changed[mineral_group][mineral] = 0
                    self.how_many_times_production_changed[mineral_group][mineral] -= 1
                # these if and elif statements both do the same as the above,
                # but in relation to mineral REQUIREMENT increasing/decreasing
                if chance_of_req <= self.requirement_chance[mineral_group][mineral]:
                    self.requirement_chance[mineral_group][mineral] += random.randint(1, 3)
                    self.requirement[mineral_group][mineral] += 1
                    self.minerals[mineral_group][mineral] -= self.requirement[mineral_group][mineral] / all_minerals_rarity[mineral_group][mineral]
                    if self.requirement_chance[mineral_group][mineral] > high_chance:
                        self.requirement_chance[mineral_group][mineral] = high_chance
                    if self.how_many_times_requirement_changed[mineral_group][mineral] < 0:
                        self.how_many_times_requirement_changed[mineral_group][mineral] = 0
                    self.how_many_times_requirement_changed[mineral_group][mineral] += 1

                elif chance_of_req > self.requirement_chance[mineral_group][mineral]:
                    self.requirement_chance[mineral_group][mineral] -= random.randint(1, 3)
                    self.requirement[mineral_group][mineral] -= 1
                    self.minerals[mineral_group][mineral] -= self.requirement[mineral_group][mineral] / all_minerals_rarity[mineral_group][mineral]
                    if self.requirement_chance[mineral_group][mineral] < low_chance:
                        self.requirement_chance[mineral_group][mineral] = low_chance
                    if self.how_many_times_requirement_changed[mineral_group][mineral] > 0:
                        self.how_many_times_requirement_changed[mineral_group][mineral] = 0
                    self.how_many_times_requirement_changed[mineral_group][mineral] -= 1

                # the code below doesn't change the functioning of anything else,
                # just creates more readable var's for the database
                self.total_increase[mineral_group][mineral] = (self.production[mineral_group][mineral] *
                                                               climate_modifier[mineral_group]) / all_minerals_rarity[mineral_group][mineral]
                self.total_increase[mineral_group][mineral] = int(round(self.total_increase[mineral_group][mineral]))
                # round result
                self.total_decrease[mineral_group][mineral] = (self.requirement[mineral_group][mineral] / all_minerals_rarity[mineral_group][mineral])
                self.total_decrease[mineral_group][mineral] = int(round(self.total_decrease[mineral_group][mineral]))
                # round result

                # round result of each mineral level for legibility
                self.minerals[mineral_group][mineral] = int(round(self.minerals[mineral_group][mineral]))

                # decides the min and max levels of minerals, starts at 10, as result is divided buy 10 or less later,
                # as well as other climate modifications to the amount
                if self.production[mineral_group][mineral] < 10:
                    self.production[mineral_group][mineral] = 10
                if self.production[mineral_group][mineral] > 35:
                    self.production[mineral_group][mineral] = 34
                if self.requirement[mineral_group][mineral] < 10:
                    self.requirement[mineral_group][mineral] = 10
                if self.requirement[mineral_group][mineral] > 35:
                    self.requirement[mineral_group][mineral] = 34

    def find_mineral_need(self):
        for mineral_group in xrange(0, 3):
            # 1st loop cycles through mineral groups
            for mineral in xrange(0, 10):
                # 2nd loop cycles through each mineral
                # convert mineral levels into need if mineral levels are in -int
                if self.minerals[mineral_group][mineral] < 0:
                    self.need[mineral_group][mineral] = self.minerals[mineral_group][mineral]
                    # change minerals need to positive integers for legibility
                    self.need[mineral_group][mineral] = -self.need[mineral_group][mineral]
                else:
                    self.need[mineral_group][mineral] = 0
                    # if a planets mineral level is not below 0, need will always be 0

    def find_price(self, element_rarity):
        # imports the mineral rarity variables to be used later on
        gas_rarity = element_rarity[0]
        liquid_rarity = element_rarity[1]
        solid_rarity = element_rarity[2]

        max_value = 250000
        all_minerals_rarity = [gas_rarity, liquid_rarity, solid_rarity]
        for mineral_group in xrange(0, 3):
            # 1st loop cycles through mineral groups
            for mineral in xrange(0, 10):
                # 2nd loop cycles through each mineral
                buy_base_price = 0
                sell_base_price = 0
                if self.minerals[mineral_group][mineral] > 0:
                    # if there are minerals to sell
                    sell_base_price = max_value / self.minerals[mineral_group][mineral]
                    sell_base_price *= all_minerals_rarity[mineral_group][mineral]
                    # get max value of products and divide by number of minerals, multiply this by rarity. 10 rarity is highest.
                    # this means the more minerals there are, the cheaper they are sold. more minerals to sell = pay less
                    random_price_change = random.randint(1, 2)
                    if sell_base_price > 100000:
                        sell_base_price = 100000
                    if random_price_change == 1:
                        sell_base_price += sell_base_price / random.randint(10, 20)
                    if random_price_change == 2:
                        sell_base_price -= sell_base_price / random.randint(10, 20)
                    # add a random small amount to the price, because its all made up anyway!
                self.price_sell[mineral_group][mineral] = sell_base_price

                if self.need[mineral_group][mineral] > 0:
                    buy_base_price = self.need[mineral_group][mineral] / 20
                    buy_base_price *= all_minerals_rarity[mineral_group][mineral]
                    # for buy price, the idea is reversed so the result is: more minerals needed = pay more
                    random_price_change = random.randint(1, 2)
                    if random_price_change == 1:
                        buy_base_price += buy_base_price / random.randint(10, 20)
                    if random_price_change == 2:
                        buy_base_price -= buy_base_price / random.randint(10, 20)
                self.price_buy[mineral_group][mineral] = buy_base_price

    def find_max_prices(self):
        for mineral_group in xrange(0, 3):
            # 1st loop cycles through mineral groups
            for mineral in xrange(0, 10):
                # Price of minerals sets high price and low price, similar to highs/lows of the day in stock trading
                # if price goes above previous high price, then it replaces it
                if self.price_buy[mineral_group][mineral] > self.max_price_buy[mineral_group][mineral]:
                    self.max_price_buy[mineral_group][mineral] = self.price_buy[mineral_group][mineral]
                # Same for the low price. In effect i will see numbers like e.g 3(low), 5(planet), 7(high)
                if self.price_buy[mineral_group][mineral] < self.low_price_buy[mineral_group][mineral]:
                    self.low_price_buy[mineral_group][mineral] = self.price_buy[mineral_group][mineral]

                if self.price_sell[mineral_group][mineral] > self.max_price_sell[mineral_group][mineral]:
                    self.max_price_sell[mineral_group][mineral] = self.price_sell[mineral_group][mineral]

                if self.price_sell[mineral_group][mineral] < self.low_price_sell[mineral_group][mineral]:
                    self.low_price_sell[mineral_group][mineral] = self.price_sell[mineral_group][mineral]

    def reset_max_prices(self):
        self.max_price_buy = [[0] * 10, [0] * 10, [0] * 10]
        self.low_price_buy = [[100000] * 10, [100000] * 10, [100000] * 10]
        self.max_price_sell = [[0] * 10, [0] * 10, [0] * 10]
        self.low_price_sell = [[100000] * 10, [100000] * 10, [100000] * 10]


class Elements(object):
    # The class "constructor"
    def __init__(self):
        self.element_names = self.create_elements()
        self.element_rarity = self.assign_minerals_rarity()

    def create_elements(self):
        gas_suffix = ["xygen", "lium", "bium", "oron", ]
        liquid_suffix = ["giun", "allum", "niun", "siun", ]
        solid_suffix = ["omin", "dite", "dium", "tium", ]
        element_suffix = [gas_suffix, liquid_suffix, solid_suffix]

        gases = [""] * 10
        liquids = [""] * 10
        solids = [""] * 10
        all_elements = [gases, liquids, solids]

        for x7 in xrange(0, 3):  # this iterates through the three types of element
            current_element = all_elements[x7]
            for x4 in xrange(0, 10):  # this iterates through each 10 elements of planet type
                current_prefix = create_word(1, 1)
                current_suffix = element_suffix[x7]
                current_element[x4] = current_prefix
                current_element[x4] += random.choice(current_suffix)
        return all_elements

    def assign_minerals_rarity(self):
        gas_rarity = [0] * 10
        liquids_rarity = [0] * 10
        solids_rarity = [0] * 10

        element_rarity = [gas_rarity, liquids_rarity, solids_rarity]

        for x5 in xrange(0, 3):  # this iterates through the three types of element
            current_rarity = element_rarity[x5]
            for x6 in xrange(0, 10):  # this iterates through each 10 elements of planet type
                current_rarity[x6] = random.randint(1, 10)

        return element_rarity


class DataAggregator(object):

    # this currently aggregates some planet data based on certain requirements,
    # like lowest price of single mineral across all planets
    def __init__(self, planets, number_of_planets):
        self.all_planets = planets  # IMPORTS PLANET DATA
        self.number_of_planets = number_of_planets  # IMPORTS NUMBER OF PLANETS
        self.mineral_lowest_sell_prices = self.find_lowest_sell_prices()  # FUNCTIONS FINDS LOWEST SELL PRICES
        self.mineral_highest_buy_prices = self.find_highest_buy_prices()  # FUNCTIONS FINDS LOWEST SELL PRICES

    def find_lowest_sell_prices(self):

            mineral_sell_price_lists = \
                [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]
            # HAVE TO FIND BETTER WAY TO WRITE THIS, IS THIS TOO MANY LIST'S!
            # each list contains the sell price of each mineral from all available planets
            for planet in xrange(0, self.number_of_planets):  # FINDS LOWEST PRICE FOR EACH MINERAL ON EACH PLANET
                for mineral_group in xrange(0, 3):
                    for mineral_price in xrange(0, 10):
                        if self.all_planets[planet].price_sell[mineral_group][mineral_price] > 0:
                            mineral_sell_price_lists[mineral_group][mineral_price].append(
                                self.all_planets[planet].price_sell[mineral_group][mineral_price])
                            mineral_sell_price_lists[mineral_group][mineral_price].append(self.all_planets[planet].name)

            mineral_best_sell_price = [[[1000000000, "None Available"]]*10, [[1000000000, "None Available"]]*10, [[1000000000, "None Available"]]*10]
            # print mineral_best_sell_price[0][0][0]
            for mineral_group in xrange(0, 3):  # FINDS BEST SELL PRICES FOR EACH MINERAL ACROSS THE GALAXY (ALL PLANETS)
                for mineral_price in xrange(0, 10):
                    current_length = len(mineral_sell_price_lists[mineral_group][mineral_price])
                    for planet_price in xrange(0, current_length, 2):
                            current_planet_price = mineral_sell_price_lists[mineral_group][mineral_price][planet_price]
                            current_planet_price_name = mineral_sell_price_lists[mineral_group][mineral_price][planet_price+1]
                            current_planet_details = [current_planet_price, current_planet_price_name]
                            if current_planet_details[0] < mineral_best_sell_price[mineral_group][mineral_price][0]:
                                mineral_best_sell_price[mineral_group][mineral_price] = current_planet_details

            return mineral_sell_price_lists, mineral_best_sell_price

    def find_highest_buy_prices(self):

            mineral_buy_price_lists = \
                [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[],[],[]]
            # HAVE TO FIND BETTER WAY TO WRITE THIS, IS THIS TOO MANY LIST'S!
            # each list contains the buy price of each mineral from all available planets
            for planet in xrange(0, self.number_of_planets):  # FINDS LOWEST PRICE FOR EACH MINERAL ON EACH PLANET
                for mineral_group in xrange(0, 3):
                    for mineral_price in xrange(0, 10):
                        if self.all_planets[planet].price_buy[mineral_group][mineral_price] > 0:
                            mineral_buy_price_lists[mineral_group][mineral_price].append(
                                self.all_planets[planet].price_buy[mineral_group][mineral_price])
                            mineral_buy_price_lists[mineral_group][mineral_price].append(self.all_planets[planet].name)
                            # include planet name as id for mineral

            mineral_best_buy_price = [[[0, "None Needed"]]*10, [[0, "None Needed"]]*10, [[0, "None Needed"]]*10]
            # print mineral_best_sell_price[0][0][0]
            for mineral_group in xrange(0, 3):  # FINDS BEST SELL PRICES FOR EACH MINERAL ACROSS THE GALAXY (ALL PLANETS)
                for mineral_price in xrange(0, 10):
                    current_length = len(mineral_buy_price_lists[mineral_group][mineral_price])
                    for planet_price in xrange(0, current_length, 2):
                            current_planet_price = mineral_buy_price_lists[mineral_group][mineral_price][planet_price]
                            current_planet_price_name = mineral_buy_price_lists[mineral_group][mineral_price][planet_price+1]
                            current_planet_details = [current_planet_price, current_planet_price_name]
                            if current_planet_details[0] > mineral_best_buy_price[mineral_group][mineral_price][0]:
                                mineral_best_buy_price[mineral_group][mineral_price] = current_planet_details

            return mineral_buy_price_lists, mineral_best_buy_price


class Company(object):  # Company class creates all variables for individual planets
    # The class "constructor"
    def __init__(self, planet_locations, number_of_planets, mineral_best_buy_prices, mineral_best_sell_prices, planets, fuel_price):
        self.planets = planets
        self.number_of_planets = number_of_planets
        self.planet_locations = planet_locations
        self.mineral_best_buy_prices = mineral_best_buy_prices
        self.mineral_best_sell_prices = mineral_best_sell_prices
        self.fuel_price = fuel_price

        self.name = self.create_company_name()
        self.company_locations = self.company_location()
        self.planet_distances = self.find_planet_distances()
        self.company_money = self.create_company_status()
        self.profit_potential = self.evaluate_planet_prices()
        self.total_fuel_cost = self.calculate_fuel_cost()
        self.profit_minus_fuel = self.take_cost_of_fuel_per_unit()

    def create_company_name(self):
        named_or_abbrv = random.randint(1, 2)
        company_letters = string.ascii_uppercase
        company_affix = ['Mogul', 'Enterprise', 'Company', 'Galactic', 'Universal', 'Nebulae', 'Binary', ]
        letters = random.randint(2, 3)
        abbreviated = ""

        if named_or_abbrv == 1:
            company_name = create_word(2, 3)  # use same word function to create
            company_name += " "
            company_name += random.choice(company_affix)
            return company_name
        else:  # THIS ADD AN ABBREVIATED COMPANY NAME INSTEAD OF FULL NAME.
            for x2 in xrange(0, letters):
                random_letter = random.choice(company_letters)
                abbreviated += random_letter
                if x2 <= letters - 2:  ##this add dots between abbreviation but stops before last letter
                    abbreviated += "."
            abbreviated += " "
            abbreviated += random.choice(company_affix)
            return abbreviated

    def create_company_status(self):
        money = random.randint(10000, 20000)
        return money

    def company_location(self):
        random_location = random.choice(self.planet_locations)
        return random_location

    def find_planet_distances(self):
        planet_distances = [0]*self.number_of_planets
        for planet in xrange(0, self.number_of_planets):
            # USES GEOMETRIC X, Y LOCATION, PYTHAGORAS STYLE
            planet_distance_x = abs(self.company_locations[0] - self.planet_locations[planet][0])
            # find difference in x coordinates
            planet_distance_y = abs(self.company_locations[1] - self.planet_locations[planet][1])
            # find difference in y coordinates
            planet_distance = ((planet_distance_x ** 2) + (planet_distance_y ** 2)) ** 0.5
            # difference in x, y coordinates are squared and added together, then find the square root of the result.
            planet_distance = round(planet_distance)
            # round result for simplicity, (sod floats)
            planet_distances[planet] = planet_distance  # insert into the list

        return planet_distances

    def evaluate_planet_prices(self):
        profit_potential = [[[0, "None Needed"]]*10, [[0, "None Needed"]]*10, [[0, "None Needed"]]*10]
        for mineral_group in xrange(0, 3):
            for mineral in xrange(0, 10):
                for mineral_price in xrange(0, 2, 2):  # iterates 2 steps to skip planets name
                    profit_potential[mineral_group][mineral] = [(  # find profit by finding sell price - buy price
                        self.mineral_best_buy_prices[mineral_group][mineral][mineral_price] -
                        self.mineral_best_sell_prices[mineral_group][mineral][mineral_price]),
                        self.mineral_best_sell_prices[mineral_group][mineral][mineral_price+1]]
        return profit_potential

    def calculate_fuel_cost(self):
        current_fuel_price = self.fuel_price # per unit distance
        planet_distances = self.planet_distances
        total_fuel_cost = [0]*self.number_of_planets

        for planet in xrange(0, self.number_of_planets):
            total_fuel_cost[planet] = [current_fuel_price * planet_distances[planet], self.planets[planet].name]
        return total_fuel_cost

    def take_cost_of_fuel_per_unit(self):

        fuel_cost = self.calculate_fuel_cost()  # get fuel cost to each planet
        after_fuel_cost = self.evaluate_planet_prices() # get mineral profit potential
        for mineral_group in xrange(0, 3):  # loop through mineral group
            for mineral in xrange(0, 10): # loop through minerals
                for mineral_price in xrange(0, 2, 2):  # iterates 2 steps to skip planets name
                    for planet_fuel_cost in xrange(0, self.number_of_planets):  # loop through each planets planet fuel cost
                        if fuel_cost[planet_fuel_cost][1] == after_fuel_cost[mineral_group][mineral][mineral_price+1]:
                            after_fuel_cost[mineral_group][mineral][mineral_price] -= fuel_cost[planet_fuel_cost][0]
                            # ^^^^ THIS WORKS BUT SAYS IT SHOULDN'T!
        # print fuel_cost[planet_fuel_cost]  # <--- this should mean there is still an iterable list with a length of 1
        # if the planet name associated with the mineral being looked at matches a planet name
        # in the fuel cost list, that fuel cost is deducted from the profit potential
        return after_fuel_cost
