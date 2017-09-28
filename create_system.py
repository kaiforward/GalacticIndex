import random
import string
from math import floor
from language import word_creator
import copy

CLIMATE_MODIFIERS = {  # used in planet class
    # climate modifier where 0, 1 and 2 of array are gas, liquid, solid respectively
    'Tropical': [1.05, 0.95, 1],  # higher levels of gas
    'Oceanic': [1, 1.2, 0.6],  # higher level of liquid, less solid
    'Rocky': [0.7, 0.8, 1.15],  # higher level of solid, slightly less gas/liq
    'Desert': [0.9, 0.5, 1.05],  # more solid, much less liquid
    'Arctic': [1, 1.15, 0.85],
    'Continental': [1, 1, 1],
    'Gas Giant': [1.5, 0.75, 0.75],  # much higher gas, less liquid, less solid
    'Toxic': [1.15, 1.05, 0.8],  # higher gas, liquid, less solid
    'Frozen': [1, 1.1, 0.8],  # higher liquid
    'Metallic': [0.9, 0.8, 1.3],  # much higher solid
    'Barren': [0.5, 0.8, 1.1],  # higher solid, less gas and liquid
}

CLIMATE_LIFE_MODIFIERS = {
    # climate modifier where 0, 1 and 2 of array are land, plant and sea life
    'Tropical': [3, 1.2, 1.2],  # higher levels of gas
    'Oceanic': [0.5, 0.5, 4],  # higher level of liquid, less solid
    'Rocky': [1.2, 0.95, 0.5],  # higher level of solid, slightly less solid
    'Desert': [1, 0.5, 0.1],  # more solid, much less liquid
    'Arctic': [1, 1.05, 1],
    'Continental': [2, 2, 2],
    'Gas Giant': [0, 0, 0],  # much higher gas, less liquid, less solid
    'Toxic': [0, 0, 0],  # higher gas, liquid, less solid
    'Frozen': [0, 0, 0],  # higher liquid
    'Metallic': [0, 0, 0],  # much higher solid
    'Barren': [0, 0, 0],  # higher solid, less gas and liquid
}


def create_locations():
        location = [random.randint(1, 100), random.randint(1, 100)]
        previous_location = location
        while location == previous_location:
            location = [random.randint(1, 100), random.randint(1, 100)]
        return location


def create_all_planet_locations(number_of_planets, planets):
    # CREATES A LIST OF LOCATIONS, IS USED HERE SO REPEATS WILL BE RECOGNISED
    location_list = []
    for planet in xrange(0, number_of_planets):
        planets[planet].create_pop()
        current_location = create_locations()
        if current_location in location_list:  # if planet random location already used
            current_location = create_locations()
        location_list.append(current_location)
        planets[planet].location = location_list[planet]
    return location_list


def create_all_company_locations(number_of_planets, location_list):
    company_locations = []
    for company in xrange(0, number_of_planets):
        company_locations.append(location_list[company])
    return company_locations


class CreateGalaxySize(object):
    # The class "constructor"
    def __init__(self):
        self.number_of_planets = self.choose_number_of_planets()

    def choose_number_of_planets(self):
        number_of_planets = int(raw_input("Choose how many planets"))
        return number_of_planets


class FuelPrices(object):

    def __init__(self):
        self.fuel_price = 7.5
    # need to keep consistent variables after self.fuelprices() is run, so its stored here

    def fuel_prices(self):
        random_change = random.random()
        if random_change > 0.5:
            self.fuel_price += 0.5
            if self.fuel_price > 15:
                self.fuel_price = 15
        if random_change < 0.5:
            self.fuel_price -= 0.5
            if self.fuel_price < 5:
                self.fuel_price = 5
        return self.fuel_price


class Planet(object):  # Planet class creates all variables for individual planets
    # The class "constructor"
    def __init__(self):

        # SO MANY VARIABLES!
        climate, habitable = self.create_climate()  # get planet habitability and climate
        name = word_creator(random.randint(1, 2))
        name = name.title()
        affix = self.create_planet_affix()
        self.name = name+" "+affix  # creates random Planet Name
        self.habitable = habitable  # defines whether planet is habitable
        self.climate = climate  # based on habitability a climate is assigned
        self.location = [0, 0]  # Location not set inside class as it must be unique from other planets
        self.economic = "Steady"
        self.population = 0  # needs to know Habitability
        self.planet_features = self.planet_features()
        # these variables are stored this way as they need to hold the same values from the previous iteration of the functions
        # they all relate to planet minerals, their use, creation, prices to buy/sell and some info on that change
        self.minerals = [[0]*10, [0]*10, [0]*10]
        self.production = [[20]*10, [20]*10, [20]*10]
        self.requirement = [[20]*10, [20]*10, [20]*10]
        self.max_production = 35
        self.max_requirement = 35
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
        self.how_many_times_requirement_changed = [[0]*10, [0]*10, [0]*10]
        self.max_low_chance_prod = [45, 55]
        self.max_low_chance_req = [45, 55]
        # modified data needed for chart design's.
        self.chart_price_sell = [[0]*10, [0]*10, [0]*10]
        self.chart_price_buy = [[0]*10, [0]*10, [0]*10]
        self.chart_max_price_sell = [[0]*10, [0]*10, [0]*10]
        self.chart_max_price_buy = [[0]*10, [0]*10, [0]*10]
        self.chart_minerals = [[0]*10, [0]*10, [0]*10]
        self.chart_need = [[0]*10, [0]*10, [0]*10]

    def create_chart_values(self):  # this modifies some of my data for the DB, to make things more readable and interesting!
        self.chart_minerals = copy.deepcopy(self.minerals)
        self.chart_need = copy.deepcopy(self.need)
        for min_group in xrange(0, 3):
            for min in xrange(0, 10):
                # calculations for my price chart, so i can show low, present and high prices on one graph.
                self.chart_price_sell[min_group][min] = self.price_sell[min_group][min] - self.low_price_sell[min_group][min]
                self.chart_max_price_sell[min_group][min] = self.max_price_sell[min_group][min] - self.price_sell[min_group][min]
                #
                self.chart_price_buy[min_group][min] = self.price_buy[min_group][min] - self.low_price_buy[min_group][min]
                self.chart_max_price_buy[min_group][min] = self.max_price_buy[min_group][min] - self.price_buy[min_group][min]
                if self.chart_minerals[min_group][min] <= 0:
                    self.chart_minerals[min_group][min] = 0
                self.chart_need[min_group][min] = -self.chart_need[min_group][min]




    def create_planet_affix(self):
        affix_list = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota",
                      "Kappa", "Lambda", "Xi", "Omicron", "Pi", "San", "Rho", "Sigma", "Tau", 'Upsilon']
        affix_choice = random.choice(affix_list)
        return affix_choice

    def create_pop(self):
        if self.habitable == "Habitable":
            self.population = random.randint(1000000000, 10000000000)
        if self.habitable == "Inhabitable":
            self.population = random.randint(1000000, 1000000000)

    def create_climate(self):
        # RANDOMLY DECIDES WHETHER PLANET IS HABITABLE, IF IT IS HABITABLE IT CHOOSES WHAT CLIMATE IT IS
        decide_if_habitable = random.random()
        randomize_climate = ["Continental", "Tropical", "Oceanic", "Desert", "Rocky", "Arctic"]
        randomize_barren = ["Barren", "Gas Giant", "Metallic", "Frozen", "Toxic"]
        if decide_if_habitable >= 0.45:  # habitable
            current_climate = random.choice(randomize_climate)
            current_habitable = "Habitable"
        else:  # not habitable
            current_climate = random.choice(randomize_barren)
            current_habitable = "Inhabitable"
        return current_climate, current_habitable

    def planet_features(self):
        animal_species = 0
        plant_species = 0
        sea_species = 0
        planet_features = [animal_species, plant_species, sea_species]
        current_climate = self.climate
        climate_life_modifier = CLIMATE_LIFE_MODIFIERS[current_climate]  # use dict
        for species_group in xrange(0, 3):
            planet_features[species_group] = random.randint(0, 9000000) * climate_life_modifier[species_group]
            planet_features[species_group] = int(round(planet_features[species_group]))
        return planet_features

    def make_changes_based_on_economic(self):
        production_increase_from_pop = self.population / 1000000000
        standard_rate = 35 + production_increase_from_pop
        if self.economic == "Boom":  # give increased production bias
            self.max_low_chance_prod = [50, 95]
            self.max_low_chance_req = [5, 50]
            if self.habitable == "Habitable":
                self.max_production = standard_rate + standard_rate
            if self.habitable == "Inhabitable":
                self.max_production = standard_rate + random.randint(1, 10)
            self.max_requirement = 35 + (production_increase_from_pop / 3)
        if self.economic == "Crash":  # give reduced production bias
            self.max_low_chance_prod = [5, 50]
            self.max_low_chance_req = [50, 95]
            self.max_production = 35
            self.max_requirement = standard_rate + standard_rate
        if self.economic == "Steady":  # neutral production
            self.max_low_chance_prod = [40, 60]
            self.max_low_chance_req = [40, 60]
            self.max_production = standard_rate
            self.max_requirement = standard_rate

    def make_changes_based_on_pop(self):
        if self.habitable == "Habitable":
            self.population += random.randint(0, 10)
        if self.habitable == "Inhabitable":
            self.population += random.randint(0, 3)

    def decide_economic_status(self):
        # defines the maximum low chance and high chance of planet minerals changing. so 90 sort of equates to 90% percent chance
        if self.economic == "Steady":
            random_chance_of_change = random.randint(1, 10000)
            if random_chance_of_change >= 9995:
                if random.random() > 0.50:
                    self.economic = "Boom"
                else:
                    self.economic = "Crash"
        if self.economic == "Boom":
            random_chance_of_change = random.randint(1, 10000)
            if random_chance_of_change <= 1:
                self.economic = "Steady"
            elif random_chance_of_change >= 9995:
                self.economic = "Crash"
        if self.economic == "Crash":
            random_chance_of_change = random.randint(1, 10000)
            if random_chance_of_change <= 5:
                self.economic = "Steady"
            elif random_chance_of_change == 9999:
                self.economic = "Boom"

        self.make_changes_based_on_economic()
        self.make_changes_based_on_pop()  # must be second for modifier to be added

    def add_minerals(self, element_rarity):
        # WARNING THIS IS A DISGUSTINGLY LONG FUNCTION I DIDN'T HAVE TIME TO REDUCE
        # imports the mineral rarity variables to be used later on
        gas_rarity = element_rarity[0]
        liquid_rarity = element_rarity[1]
        solid_rarity = element_rarity[2]
        all_minerals_rarity = [gas_rarity, liquid_rarity, solid_rarity]

        # finds the planet climate and adds a climate modifier to results of mineral production
        current_climate = self.climate
        climate_modifier = CLIMATE_MODIFIERS[current_climate]
        # put into dictionary to get rid of "some" clutter

        for mineral_group in xrange(0, 3):
            # 1st loop cycles through mineral groups
            for mineral in xrange(0, 10):
                # 2nd loop cycles through each mineral
                chance_of_prod = random.randint(1, 100)
                chance_of_req = random.randint(1, 100)
                # generate random number for comparison, that decides whether production or requirement levels change

                # this way of creating the variable, means that im already targeting the list i want,
                # but not the individual values so the changes made here are always reflected in i.e self.minerals
                production_chances = self.production_chance[mineral_group]  # the percentage chance of change
                production = self.production[mineral_group]
                minerals = self.minerals[mineral_group]
                times_production_increased = self.how_many_times_production_changed[mineral_group]

                if self.economic == "Boom":
                    positive_economic_modifier = random.randint(1, 5)
                    negative_economic_modifier = 0
                elif self.economic == "Crash":
                    positive_economic_modifier = 0
                    negative_economic_modifier = random.randint(1, 5)
                else:
                    positive_economic_modifier = 0
                    negative_economic_modifier = 0

                if chance_of_prod <= production_chances[mineral]:
                    # if the chance of production is less than the random chance_of_prod, mineral production improves
                    production_chances[mineral] += random.randint(1, 3)
                    # better chance of improving next time
                    production[mineral] += 1 + positive_economic_modifier  # Higher increase next time
                    minerals[mineral] += (production[mineral] *
                                          climate_modifier[mineral_group]) / all_minerals_rarity[mineral_group][mineral]
                    # ^too long line, adds the planet amount of mineral production with modifiers to overall mineral level.
                    if production_chances[mineral] > self.max_low_chance_prod[1]:
                        production_chances[mineral] = self.max_low_chance_prod[1]
                    # makes sure chance of changing never goes above the set limits
                    if times_production_increased[mineral] < 0:
                        # if production was previously decreasing reset counter
                        times_production_increased[mineral] = 0
                    times_production_increased[mineral] += 1
                    # measures how many times production has improved in a row

                # these further elif does the same as above but with the reverse effect of mineral production decreasing slightly
                elif chance_of_prod > production_chances[mineral]:
                    production_chances[mineral] -= random.randint(1, 3)
                    production[mineral] -= 1 - negative_economic_modifier
                    minerals[mineral] += (production[mineral] *
                                          climate_modifier[mineral_group]) / all_minerals_rarity[mineral_group][mineral]
                    if production_chances[mineral] < self.max_low_chance_prod[0]:
                        production_chances[mineral] = self.max_low_chance_prod[0]
                    if times_production_increased[mineral] > 0:
                        times_production_increased[mineral] = 0
                    times_production_increased[mineral] -= 1

                # Again creating the variables here, to shorten lines in the actual functions
                requirement_chance = self.requirement_chance[mineral_group]
                requirement = self.requirement[mineral_group]
                times_requirement_changed = self.how_many_times_requirement_changed[mineral_group]

                if chance_of_req <= requirement_chance[mineral]:
                    requirement_chance[mineral] += random.randint(1, 3)
                    requirement[mineral] += 1 + positive_economic_modifier
                    minerals[mineral] -= requirement[mineral] / all_minerals_rarity[mineral_group][mineral]
                    if requirement_chance[mineral] > self.max_low_chance_req[1]:
                        requirement_chance[mineral] = self.max_low_chance_req[1]
                    if times_requirement_changed[mineral] < 0:
                        times_requirement_changed[mineral] = 0
                    times_requirement_changed[mineral] += 1

                elif chance_of_req > requirement_chance[mineral]:
                    requirement_chance[mineral] -= random.randint(1, 3)
                    requirement[mineral] -= 1 - negative_economic_modifier
                    minerals[mineral] -= requirement[mineral] / all_minerals_rarity[mineral_group][mineral]
                    if requirement_chance[mineral] < self.max_low_chance_req[0]:
                        requirement_chance[mineral] = self.max_low_chance_req[0]
                    if times_requirement_changed[mineral] > 0:
                        times_requirement_changed[mineral] = 0
                    times_requirement_changed[mineral] -= 1

                # the code below doesn't change the functioning of anything else,
                # just creates more readable var's for the database
                total_increase = self.total_increase[mineral_group]
                total_increase[mineral] = (production[mineral] *
                                           climate_modifier[mineral_group]) / all_minerals_rarity[mineral_group][mineral]
                total_increase[mineral] = int(round(total_increase[mineral]))
                # round result
                total_decrease = self.total_decrease[mineral_group]
                total_decrease[mineral] = (requirement[mineral] / all_minerals_rarity[mineral_group][mineral])
                total_decrease[mineral] = int(round(total_decrease[mineral]))
                # round result

                # round result of each mineral level for legibility
                minerals[mineral] = int(round(minerals[mineral]))
                # if mineral levels get ridiculous, turn production to lowest and requirement to highest
                if minerals[mineral] > 100000:
                    self.economic = "Crash"
                    production[mineral] = 10
                    requirement[mineral] = self.max_requirement-1
                if minerals[mineral] < -100000:
                    self.economic = "Boom"
                    production[mineral] = self.max_production-1
                    requirement[mineral] = 10

                # decides the min and max levels of minerals, starts at 10, as result is divided buy 10 or less later,
                # as well as other climate modifications to the amount
                if production[mineral] < 10:
                    production[mineral] = 10
                if production[mineral] > self.max_production:
                    production[mineral] = self.max_production-1
                if requirement[mineral] < 10:
                    requirement[mineral] = 10
                if requirement[mineral] > self.max_requirement:
                    requirement[mineral] = self.max_requirement-1

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
                    if sell_base_price > 10000:
                        sell_base_price = 10000
                    if random_price_change == 1:
                        sell_base_price += sell_base_price / random.randint(10, 20)
                    if random_price_change == 2:
                        sell_base_price -= sell_base_price / random.randint(10, 20)
                    # add a random small amount to the price, because its all made up anyway!
                self.price_sell[mineral_group][mineral] = sell_base_price

                if self.need[mineral_group][mineral] > 0:
                    buy_base_price = self.need[mineral_group][mineral] / 20
                    buy_base_price *= all_minerals_rarity[mineral_group][mineral]
                    # for buy price, the idea is reversed so the result is: more minerals needed = willing to pay more
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

    def remove_minerals(self, purchase):  # if planet sells minerals
        if len(purchase) > 7:
            if purchase[2] == self.name:
                print ""
                print self.minerals[purchase[4]][purchase[5]]
                self.minerals[purchase[4]][purchase[5]] -= purchase[7]
                print "success selling", self.name
                print self.minerals[purchase[4]][purchase[5]]

    def buy_minerals(self, sale):  # if planet buy minerals
        if len(sale) > 0:
            if sale[2] == self.name:
                print ""
                print self.minerals[sale[3]][sale[4]]
                self.minerals[sale[3]][sale[4]] += sale[6]
                print self.minerals[sale[3]][sale[4]]
                print "success buying", self.name


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

        for element_group in xrange(0, 3):  # this iterates through the three types of element
            current_element = all_elements[element_group]
            for element in xrange(0, 10):  # this iterates through each 10 elements of planet type
                current_prefix = word_creator(1)
                current_suffix = element_suffix[element_group]
                current_element[element] = current_prefix
                current_element[element] += random.choice(current_suffix)
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

    def create_mineral_price_list(self):
        all_mineral_price_list = []
        for mineral_groups in xrange(0, 3):
            all_mineral_price_list.append([])
            for minerals in xrange(0, 10):
                all_mineral_price_list[mineral_groups].append([])
        return all_mineral_price_list

    def create_mineral_sell_price_list(self):
        mineral_sell_price_list = self.create_mineral_price_list()
        for mineral_groups in xrange(0, 3):
            for minerals in xrange(0, 10):
                mineral_sell_price_list[mineral_groups][minerals] = 100000000, "None Available"
        return mineral_sell_price_list

    def create_mineral_buy_price_list(self):
        mineral_buy_price_list = self.create_mineral_price_list()
        for mineral_groups in xrange(0, 3):
            for minerals in xrange(0, 10):
                mineral_buy_price_list[mineral_groups][minerals] = 0, "None Needed"
        return mineral_buy_price_list

    def find_lowest_sell_prices(self):

            mineral_sell_price_lists = self.create_mineral_price_list()
            # HAVE TO FIND BETTER WAY TO WRITE THIS, IS THIS TOO MANY LIST'S!
            # each list contains the sell price of each mineral from all available planets
            for planet in xrange(0, self.number_of_planets):  # FINDS LOWEST PRICE FOR EACH MINERAL ON EACH PLANET
                for mineral_group in xrange(0, 3):

                    for mineral_price in xrange(0, 10):
                        if self.all_planets[planet].price_sell[mineral_group][mineral_price] > 0:
                            mineral_sell_price_lists[mineral_group][mineral_price].append(
                                self.all_planets[planet].price_sell[mineral_group][mineral_price])
                            mineral_sell_price_lists[mineral_group][mineral_price].append(self.all_planets[planet].name)

            mineral_best_sell_price = self.create_mineral_sell_price_list()
            for mineral_group in xrange(0, 3):  # FINDS BEST SELL PRICES FOR EACH MINERAL ACROSS THE GALAXY (ALL PLANETS)
                for mineral_price in xrange(0, 10):
                    current_length = len(mineral_sell_price_lists[mineral_group][mineral_price])
                    for planet_price in xrange(0, current_length, 2):
                            current_planet_price = mineral_sell_price_lists[mineral_group][mineral_price][planet_price]
                            int(round(current_planet_price))
                            current_planet_price_name = mineral_sell_price_lists[mineral_group][mineral_price][planet_price+1]
                            current_planet_details = [current_planet_price, current_planet_price_name]
                            if current_planet_details[0] < mineral_best_sell_price[mineral_group][mineral_price][0]:
                                mineral_best_sell_price[mineral_group][mineral_price] = current_planet_details

            return mineral_sell_price_lists, mineral_best_sell_price

    def find_highest_buy_prices(self):

            mineral_buy_price_lists = self.create_mineral_price_list()
            # HAVE TO FIND BETTER WAY TO WRITE THIS, IS THIS TOO MANY LIST'S!
            # each list contains the buy price of each mineral from all available planets
            for planet in xrange(0, self.number_of_planets):  # FINDS LOWEST PRICE FOR EACH MINERAL ON EACH PLANET (TOO NESTY)
                for mineral_group in xrange(0, 3):
                    for mineral_price in xrange(0, 10):
                        if self.all_planets[planet].price_buy[mineral_group][mineral_price] > 0:
                            mineral_buy_price_lists[mineral_group][mineral_price].append(
                                self.all_planets[planet].price_buy[mineral_group][mineral_price])
                            mineral_buy_price_lists[mineral_group][mineral_price].append(self.all_planets[planet].name)
                            # include planet name as id for mineral

            mineral_best_buy_price = self.create_mineral_buy_price_list()
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
    def __init__(self, elements, planet_locations, number_of_planets, mineral_best_buy_prices, mineral_best_sell_prices, planets, fuel_price, tick, company_location):
        self.elements = elements
        self.planets = planets
        self.number_of_planets = number_of_planets
        self.planet_locations = planet_locations
        self.mineral_best_buy_prices = mineral_best_buy_prices
        self.mineral_best_sell_prices = mineral_best_sell_prices
        self.tick = tick
        self.fuel_price = fuel_price

        self.name = self.create_company_name()
        self.company_locations = company_location
        self.planet_distances = self.find_planet_distances()
        self.company_money = 1000000  # variables needs to be preserved each loop so declared here
        self.number_of_spaceports = random.randint(1, 3)  # 1 represents 10 active trades possible at any one time for both purchase and sale
        self.number_of_ships = (self.number_of_spaceports*10)-random.randint(1, 5)  # this represents the size/amount of ships and goods that can be transported in one trip
        self.profit_potential = self.evaluate_planet_prices()
        self.total_fuel_cost = self.calculate_fuel_cost()
        self.profit_minus_fuel = self.take_cost_of_fuel_per_unit()

        self.company_minerals = [0]*10, [0]*10, [0]*10
        self.minerals_in_transit_bought = [0]*10, [0]*10, [0]*10
        self.minerals_in_transit_sell = [0] * 10, [0] * 10, [0] * 10
        self.average_prices_bought_for = [0] * 10, [0] * 10, [0] * 10
        self.trade_list = []
        self.sell_list = []
        self.profit = 0
        self.spent = 0
        self.purchase = self.decide_to_buy()
        self.sale = self.sell_minerals()
        self.expenses = 0
        self.stocks = 1000000
        self.stock_price = 0
        self.company_age = random.randint(0, 10000)

    def create_new_company(self):
        self.company_age += 1

        if self.company_money < -0:
            if len(self.trade_list) <= 0 and len(self.sell_list) <= 0:
                self.company_minerals = [0] * 10, [0] * 10, [0] * 10
                self.minerals_in_transit_bought = [0] * 10, [0] * 10, [0] * 10
                self.minerals_in_transit_sell = [0] * 10, [0] * 10, [0] * 10
                self.average_prices_bought_for = [0] * 10, [0] * 10, [0] * 10
                self.trade_list = []
                self.sell_list = []
                self.profit = 0
                self.spent = 0
                self.purchase = self.decide_to_buy()
                self.sale = self.sell_minerals()
                self.expenses = 0
                self.stocks = 1000000
                self.stock_price = 0
                self.company_age = 0
                self.company_money = 1000000  # variables needs to be preserved each loop so declared here

    def create_company_name(self):
        named_or_abbrv = random.randint(1, 2)
        company_letters = string.ascii_uppercase
        company_affix = ['Mogul',
                         'Enterprise',
                         'Express',
                         'Galactic',
                         'Universal',
                         'Express',
                         'Binary',
                         "Associates",
                         'Celestial',
                         'Cosmic',
                         'Brothers',
                         'Sisters']
        letters = random.randint(2, 3)
        abbreviated = ""

        if named_or_abbrv == 1:
            company_name = word_creator(1)  # use same word function to create
            company_name = company_name.title()
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

    def find_planet_distances(self):
        planet_distances = []
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
            planet_distances.append(planet_distance)

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
        current_fuel_price = self.fuel_price  # per unit distance
        planet_distances = self.planet_distances
        total_fuel_cost = [0]*self.number_of_planets

        for planet in xrange(0, self.number_of_planets):
            total_fuel_cost[planet] = [current_fuel_price * planet_distances[planet], self.planets[planet].name]
        return total_fuel_cost

    def choose_to_improve(self):
        if self.company_money >= 5000000:  # if company has 5 million
            if self.number_of_ships < self.number_of_spaceports*10:  # And spaceport size has increased
                self.number_of_ships += 1
                self.company_money -= 750000  # will spend 750k million on  a ship
        if self.company_money/20000000 >= self.number_of_spaceports:  # if money above 50 million
            if self.number_of_spaceports < 50:
                    self.number_of_spaceports += 1
                    self.company_money -= 10000000

    def remove_expenses(self):
        spaceport_expenses = 50*self.number_of_spaceports  # calculate money for spaceports
        ship_expenses = 1*(len(self.trade_list)+len(self.sell_list))  # calculate money for active ships
        self.company_money -= ship_expenses + spaceport_expenses  # remove money
        self.profit -= ship_expenses + spaceport_expenses  # remove expenses from profit
        self.spent -= ship_expenses + spaceport_expenses  # add to total spent
        self.expenses = ship_expenses + spaceport_expenses  # total expenses that turn to be sent to db

    def stock_prices(self):
        self.stock_price = (self.profit + self.company_money) / self.stocks  # stock price is equal to profit made divided by number of stocks

    def take_cost_of_fuel_per_unit(self):

        fuel_cost = self.calculate_fuel_cost()  # get fuel cost to each planet
        after_fuel_cost = self.evaluate_planet_prices()  # get mineral profit potential from planets SELLING minerals
        for mineral_group in xrange(0, 3):  # loop through mineral group
            for mineral in xrange(0, 10):  # loop through minerals
                for mineral_price in xrange(0, 2, 2):  # iterates 2 steps to skip planets name
                    for planet_fuel_cost in xrange(0, self.number_of_planets):  # loop through each planets planet fuel cost
                        if fuel_cost[planet_fuel_cost][1] == after_fuel_cost[mineral_group][mineral][mineral_price+1]:
                            after_fuel_cost[mineral_group][mineral][mineral_price] -= fuel_cost[planet_fuel_cost][0]
                            # ^^^^ THIS WORKS BUT SAYS IT SHOULDN'T!
        # print fuel_cost[planet_fuel_cost]  # <--- this should mean there is still an iterable list with a length of 1
        # if the planet name associated with the mineral being looked at matches a planet name
        # in the fuel cost list, that fuel cost is deducted from the profit potential
        return after_fuel_cost

    def most_profitable_mineral(self):
        # company will creat a potential purchase based on the most profitable mineral based on best prices, and its own fuel cost's
        possible_trades = self.take_cost_of_fuel_per_unit()
        previous_amount = [0, ""]
        chosen_amount = [0, "", 0, 0, 0, 0, ""]
        planet_distance = 0

        for mineral_group in xrange(0, 3):  # cycle through mineral groups
                    for mineral in xrange(0, 10):  # cycle through minerals
                        current_amount = possible_trades[mineral_group][mineral]  # current amount to be tested
                        if current_amount[0] > previous_amount[0]:  # if current amount is higher than previous
                            previous_amount[0] = current_amount[0]  # number to be tested against is updated
                            # Then create purchase list by..
                            for planet in xrange(0, self.number_of_planets):  # finding the distance of the planet selling
                                if current_amount[1] == self.planets[planet].name:  # if planet name matches purchase
                                    planet_distance = self.planet_distances[planet]  # use that planets distance
                            mineral_price = self.mineral_best_sell_prices[mineral_group][mineral][0]  # find original price
                            mineral_name = self.elements[mineral_group][mineral]  # find mineral name
                            chosen_amount = [
                                mineral_price,  # price
                                possible_trades[mineral_group][mineral][0],  # potential profit
                                possible_trades[mineral_group][mineral][1],  # planet name
                                planet_distance,  # distance from planet
                                mineral_group,  # mineral group index
                                mineral,  # mineral index
                                mineral_name  # mineral name
                            ]
        return chosen_amount

    def decide_to_buy(self):
        purchase = self.most_profitable_mineral()
        if len(self.trade_list) <= self.number_of_spaceports*5:  # 1 spaceport handles 5 ongoing trades at a time.
            if self.company_money <= 10000000000:
                if (self.company_money / 2) >= 10000:  # If half the companies money is above 10000 credits, it will spend money
                    if self.company_minerals[purchase[4]][purchase[5]] < 1000: # if company has less than a 1000 of this mineral it will buy them
                        amount_to_spend = self.company_money / 2  # company wont spend over half its money in one turn
                        # amount_to_spend /= random.randint(1, 3)  # randomly decide to be less risky

                        amount_of_minerals_can_buy = 0

                        if purchase[0] > 0:  # if price is above zero an amount can be calculated
                            amount_of_minerals_can_buy = amount_to_spend / purchase[0]  # divide total money over cost of minerals
                            amount_of_minerals_can_buy = floor(amount_of_minerals_can_buy)  # round number down
                            amount_of_minerals_can_buy = int(round(amount_of_minerals_can_buy))  # convert to int

                        if amount_of_minerals_can_buy >= self.number_of_ships:
                            amount_of_minerals_can_buy = self.number_of_ships  # add limit to purchase number

                        purchase.append(amount_of_minerals_can_buy)  # finalise purchase by adding amount of minerals
                        trade_timer = purchase[3]+self.tick  # sets a finish date for the purchase in ticks
                        purchase.append(trade_timer)
                        # pay the cost of the minerals
                        fuel_cost = 0
                        for planet in xrange(0, self.number_of_planets):  # calculate fuel cost
                            if purchase[2] == self.total_fuel_cost[planet][1]:
                                fuel_cost = self.total_fuel_cost[planet][0]

                        if purchase[7] > 0:  # if a purchase is being made
                            self.company_money -= (purchase[7] * purchase[0]) + (purchase[3] * fuel_cost)  # remove company money
                            self.spent -= (purchase[7] * purchase[0]) + (purchase[3] * fuel_cost)  # remove company money from spent
                            self.profit -= (purchase[7] * purchase[0]) + (purchase[3] * fuel_cost)  # remove company money from profit
                            self.trade_list.append(purchase)  # create a list of all trades
                            self.minerals_in_transit_bought[purchase[4]][purchase[5]] += purchase[7]

        if len(purchase) > 7:  # if actual purchase was made
            if purchase[0] > 0:  # calculate average price by dividing new price and last price paid by 2
                self.average_prices_bought_for[purchase[4]][purchase[5]] += purchase[0]
                self.average_prices_bought_for[purchase[4]][purchase[5]] /= 2
            else:
                self.average_prices_bought_for[purchase[4]][purchase[5]] = purchase[0]

        if len(self.trade_list) > 0:  # if there's anything to check in the list
            finished_trades = []
            for trades in xrange(len(self.trade_list)):  # cycles through all trades
                if self.tick >= self.trade_list[trades][8]:  # if current tick matches tick + travel time
                    self.company_minerals[self.trade_list[trades][4]][self.trade_list[trades][5]] += self.trade_list[trades][7]
                    self.minerals_in_transit_bought[self.trade_list[trades][4]][self.trade_list[trades][5]] -= self.trade_list[trades][7]
                    # the purchase is finalised by adding the minerals once time is reached
                    finished_trades.append(trades)  # create a list of all trades that were finished
            # remove these trades separately to not confuse the for loop ^^^
            if len(finished_trades) > 0:
                for finished_trade in reversed(finished_trades):  # ITERATE IN REVERSE SO NO INDEX ERRORS WHEN REMOVING - DOH!!!
                    list.__delitem__(self.trade_list, finished_trade)  # remove ongoing purchases from list.
        return purchase

    def take_cost_of_fuel_per_unit_sale(self):

        fuel_cost = self.total_fuel_cost  # get fuel cost to each planet
        after_fuel_cost_sale = self.mineral_best_buy_prices  # get highest price planets will BUY at
        for mineral_group in xrange(0, 3):  # loop through mineral group
            for mineral in xrange(0, 10):  # loop through minerals
                for mineral_price in xrange(0, 2, 2):  # iterates 2 steps to skip planets name
                    for planet_fuel_cost in xrange(0, self.number_of_planets):  # loop through each planets planet fuel cost
                        if fuel_cost[planet_fuel_cost][1] == after_fuel_cost_sale[mineral_group][mineral][mineral_price+1]:
                            after_fuel_cost_sale[mineral_group][mineral][mineral_price] -= fuel_cost[planet_fuel_cost][0]
                            # ^^^^ THIS WORKS BUT SAYS IT SHOULDN'T!
        # print fuel_cost[planet_fuel_cost]  # <--- this shows there is still an iterable list with a length of 1
        # if the planet name associated with the mineral being looked at matches a planet name
        # in the fuel cost list, that fuel cost is deducted from the profit potential
        return after_fuel_cost_sale

    def sell_minerals(self):
        sale = 'No Sale'
        travel_time = 0
        planets_buy_prices = self.take_cost_of_fuel_per_unit_sale()  # import planet prices for all elements
        if len(self.sell_list) <= (self.number_of_spaceports*5):  # 1 spaceport can handle 5 ongoing purchases at a timw
            for mineral_group in xrange(0, 3):  # loop through mineral group
                for mineral in xrange(0, 10):  # loop through minerals
                    if self.company_minerals[mineral_group][mineral] > 0:
                        if planets_buy_prices[mineral_group][mineral][0] > self.average_prices_bought_for[mineral_group][mineral]:
                            # sell the minerals
                            planet_to_sell_to = planets_buy_prices[mineral_group][mineral][1]
                            for planet in xrange(0, self.number_of_planets):  # finding the distance of the planet selling
                                if planets_buy_prices[mineral_group][mineral][1] == self.planets[planet].name:  # if planet name matches purchase
                                    travel_time = self.planet_distances[planet]+self.tick+1  # use that planets distance
                            price_sold_for = planets_buy_prices[mineral_group][mineral]  # price planet is buying for
                            amount_sold = self.company_minerals[mineral_group][mineral]  # total possible to sell to planet
                            profit = price_sold_for[0] - self.average_prices_bought_for[mineral_group][mineral]
                            # remove average price paid to find profit as individual prices paid aren't stored (TOOO MANY)
                            element = self.elements[mineral_group][mineral]  # the element in question
                            if amount_sold >= self.number_of_ships:
                                amount_sold = self.number_of_ships  # reduce actual amount sold to ships available
                            sale = [  # after all info has been gathered complete the sale
                                price_sold_for[0],
                                profit,
                                planet_to_sell_to,
                                mineral_group,
                                mineral,
                                element,
                                amount_sold,
                                travel_time,
                            ]
                            self.company_minerals[mineral_group][mineral] -= amount_sold  # remove minerals from saleable store
                            if sale[6] > 0:  # if an actual sale was created i.e amount sold above 0, add it to the list yo
                                self.sell_list.append(sale)  # create a list of all trades
                                self.minerals_in_transit_sell[sale[3]][sale[4]] += sale[6]

        # THE CODE BELOW ALSO OCCASIONALLY BREAKS I DUNNO WHY <--- THINK ITS FIXED (has to reverse for loops)!!!
        if len(self.sell_list) > 0:  # if there's any ongoing trades to check in the list
            finished_trades = []
            for trades in xrange(len(self.sell_list)):  # cycles through all trades
                if self.tick >= self.sell_list[trades][7]:  # if current tick matches tick + Travel Time
                    # complete transaction by adding money made once goods have reached destination
                    self.company_money += self.sell_list[trades][0] * self.sell_list[trades][6]  # money made is price sold * amount
                    self.profit += self.sell_list[trades][0] * self.sell_list[trades][6]  # profit is price sold * amount
                    # once profit goes in, amount spent has already been removed so figure should be correctly calculated
                    # removes minerals from Transit list.
                    self.minerals_in_transit_sell[self.sell_list[trades][3]][self.sell_list[trades][4]] -= self.sell_list[trades][6]
                    finished_trades.append(trades)  # create a list of all trades that were finished
            if len(finished_trades) > 0:
                for finished_trade in reversed(finished_trades):  # ITERATE IN REVERSE SO NO INDEX ERRORS WHEN REMOVING - DOH!!!!
                    list.__delitem__(self.sell_list, finished_trade)  # remove completed purchases from list.
        return sale
