import random
import time


class Planet(object):  # Planet class creates all variables for individual planets
    # The class "constructor"
    def __init__(self):

        # SO MANY VARIABLES!
        climate, habitable = self.create_climate()  # get planet habitability and climate

        self.name = self.create_word()  # create's random Planet Name
        self.habitable = habitable  # defines whether planet is habitable
        self.climate = climate  # based on habitability a climate is assigned
        self.company_name = "huh"  # Not used yet
        self.economic = random.randint(1, 10)  # not used yet
        # using too many individual variables below, used 3 times more when i split the elements though >_<
        self.minerals = [[0]*10, [0]*10, [0]*10]
        self.production = [[20]*10, [20]*10, [20]*10]
        self.requirement = [[20]*10, [20]*10, [20]*10]
        self.production_chance = [[50]*10, [50]*10, [50]*10]
        self.requirement_chance = [[50]*10, [50]*10, [50]*10]
        self.need = [[0]*10, [0]*10, [0]*10]
        self.price_sell = [[0]*10, [0]*10, [0]*10]
        self.price_buy = [[0]*10, [0]*10, [0]*10]

    def get_language(self):
        # IMPORTS MY LANGUAGE TEXT FILE WHICH CONTAINS A LIST OF FICTIONAL "VERBS"
        lines = []
        with open('language.txt') as language:
            for line in language:
                lines.append(line.strip())
        return lines

    def create_word(self):
        # creates a word by getting the verb list and randomly selecting non-repeating verbs to make words
        verbs_list = self.get_language()
        word = ""  # created word
        previous_verb = ""  # previous used verb
        verbs = random.randint(2, 4)

        for x1 in xrange(0, verbs):
            random_verb = random.choice(verbs_list)
            if previous_verb == random_verb:
                while previous_verb == random_verb:
                    random_verb = random.choice(verbs_list)
            previous_verb = random_verb
            word += random_verb
        return word

    def create_climate(self):
        # RANDOMLY DECIDES WETHER PLANET IS HABITABLE, IF IT IS HABITABLE IT CHOOSES WHAT CLIMATE IT IS
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

def get_language2():
    # IMPORTS MY LANGUAGE TEXT FILE WHICH CONTAINS A LIST OF FICTIONAL "VERBS"
    lines = []
    with open('language.txt') as language:
        for line in language:
            lines.append(line.strip())
    return lines


def create_word2(minverb, maxverb):
    # creates a word by getting the verb list and randomly selecting non-repeating verbs to make words
    verbs_list = get_language2()
    word = ""  # created word
    previous_verb = ""  # previous used verb
    verbs = random.randint(minverb, maxverb)

    for x1 in xrange(0, verbs):
        random_verb = random.choice(verbs_list)
        if previous_verb == random_verb:
            while previous_verb == random_verb:
                random_verb = random.choice(verbs_list)
        previous_verb = random_verb
        word += random_verb
    return word


def create_elements():
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
        for x4 in xrange(0, 10):  # this iterates through each 10 elements of current type
            current_prefix = create_word2(1, 1)
            current_suffix = element_suffix[x7]
            current_element[x4] = current_prefix
            current_element[x4] += random.choice(current_suffix)
    return all_elements


def assign_minerals_rarity():
    gas_rarity = [0] * 10
    liquids_rarity = [0] * 10
    solids_rarity = [0] * 10

    element_rarity = [gas_rarity, liquids_rarity, solids_rarity]

    for x5 in xrange(0, 3):  # this iterates through the three types of element
        current_rarity = element_rarity[x5]
        for x6 in xrange(0, 10):  # this iterates through each 10 elements of current type
            current_rarity[x6] = random.randint(1, 10)

    return element_rarity


def add_minerals(number_of_planets, element_rarity):
    # cycles through planets using xrange as objects don't provide an index and i need that further on!
    for planet in xrange(0, number_of_planets):
        # imports the mineral rarity variables to be used later on
        gas_rarity = element_rarity[0]
        liquid_rarity = element_rarity[1]
        solid_rarity = element_rarity[2]
        all_minerals_rarity = [gas_rarity, liquid_rarity, solid_rarity]

        # defines the maximum low chance and high chance of planet minerals changing. so 90 sort of equates to 90% percent chance
        low_chance = 10
        high_chance = 90

        # finds the current climate and adds a climate modifier to results of mineral production
        # there maybe a better way of doing this???
        current_climate = planets[planet].climate
        climate_modifier = [1, 1, 1]
        # climate modifier where 0, 1 and 2 of array are gas, liquid, solid respectively
        if current_climate == "Tropical":  # higher levels of gas
            climate_modifier[0] = 1.5
        elif current_climate == 'Oceanic':  # much higher levels of water, less solid
            climate_modifier[1] = 2
            climate_modifier[2] = 0.8
        elif current_climate == 'Rocky':  # higher levels or solids
            climate_modifier[2] = 1.5
        elif current_climate == 'desert':  # higher levels or solids, no use-able amount of water
            climate_modifier[1] = 0.8
            climate_modifier[2] = 1.75
        elif current_climate == 'Gas Giant':  # huge levels of gas, no liquid or solid
            climate_modifier[0] = 2
            climate_modifier[1] = 0.8
            climate_modifier[2] = 0.8
        elif current_climate == 'Toxic':  # higher levels of gas
            climate_modifier[0] = 1.5
        elif current_climate == 'Frozen World':  # higher levels of liquid
            climate_modifier[1] = 1.5
        elif current_climate == 'Metallic World':  # huge levels of solids, no liquid
            climate_modifier[1] = 0.8
            climate_modifier[2] = 2
        elif current_climate == 'Barren World':  # higher levels of solids, no liquids or gases
            climate_modifier[0] = 0.8
            climate_modifier[1] = 0.8
            climate_modifier[2] = 1.5
        else:
            climate_modifier = [1, 1, 1]

        for mineral_group in xrange(0, 3):
            # 1st loop cycles through mineral groups
            for mineral in xrange(0, 10):
                # 2nd loop cycles through each mineral
                chance_of_prod = random.randint(1, 100)
                chance_of_req = random.randint(1, 100)
                # generate random number for comparison, that decides whether production or requirement levels change
                if planets[planet].production_chance[mineral_group][mineral] <= chance_of_prod:
                    # if the chance of production is less than the random chance_of_prod, mineral production improves
                    planets[planet].production_chance[mineral_group][mineral] += random.randint(1, 3)  # better chance of improving next time
                    planets[planet].production[mineral_group][mineral] += 1  # Higher increase next time
                    planets[planet].minerals[mineral_group][mineral] \
                        += (planets[planet].production[mineral_group][mineral] * climate_modifier[mineral_group]) \
                        * (all_minerals_rarity[mineral_group][mineral] / 1.5)
                    # ^too long line, adds the current amount of mineral production with modifiers to overall mineral level.
                if planets[planet].production_chance[mineral_group][mineral] >= high_chance:
                        planets[planet].production_chance[mineral_group][mineral] = high_chance
                        # makes sure chance of changing never goes above the set limits

                elif planets[planet].production_chance[mineral_group][mineral] > chance_of_prod:
                    planets[planet].production_chance[mineral_group][mineral] -= random.randint(1, 3)
                    planets[planet].production[mineral_group][mineral] -= 1
                    planets[planet].minerals[mineral_group][mineral] += (planets[planet].production[mineral_group][mineral] * climate_modifier[mineral_group]) * (all_minerals_rarity[mineral_group][mineral] /1.5)
                    if planets[planet].production_chance[mineral_group][mineral] <= low_chance:
                        planets[planet].production_chance[mineral_group][mineral] = low_chance

                if planets[planet].requirement_chance[mineral_group][mineral] <= chance_of_req:
                    planets[planet].requirement_chance[mineral_group][mineral] += random.randint(1, 3)
                    planets[planet].requirement[mineral_group][mineral] += 1
                    planets[planet].minerals[mineral_group][mineral] -= planets[planet].requirement[mineral_group][mineral] * (all_minerals_rarity[mineral_group][mineral] /1.5)
                    if planets[planet].requirement_chance[mineral_group][mineral] >= high_chance:
                        planets[planet].requirement_chance[mineral_group][mineral] = high_chance

                elif planets[planet].requirement_chance[mineral_group][mineral] > chance_of_req:
                    planets[planet].requirement_chance[mineral_group][mineral] -= random.randint(1, 3)
                    planets[planet].requirement[mineral_group][mineral] -= 1
                    planets[planet].minerals[mineral_group][mineral] -= planets[planet].requirement[mineral_group][mineral] * (all_minerals_rarity[mineral_group][mineral] /1.5)
                    if planets[planet].requirement_chance[mineral_group][mineral] <= low_chance:
                        planets[planet].requirement_chance[mineral_group][mineral] = low_chance

                # round result of each mineral level for legibility
                planets[planet].minerals[mineral_group][mineral] = int(round(planets[planet].minerals[mineral_group][mineral]))

                # convert mineral levels into need if mineral levels are in -int
                if planets[planet].minerals[mineral_group][mineral] < 0:
                    planets[planet].need[mineral_group][mineral] = planets[planet].minerals[mineral_group][mineral]
                    # change minerals need to positive integers for legibility
                    planets[planet].need[mineral_group][mineral] = -planets[planet].need[mineral_group][mineral]
                else:
                    planets[planet].need[mineral_group][mineral] = 0
                    # if a planets mineral level is not below 0, need will always be 0


def find_price(number_of_planets, element_rarity):
    # cycles through planets using xrange as objects don't provide an index and i need that further on!
    for planet in xrange(0, number_of_planets):
        # imports the mineral rarity variables to be used later on
        gas_rarity = element_rarity[0]
        liquid_rarity = element_rarity[1]
        solid_rarity = element_rarity[2]

        max_value = 123456789
        all_minerals_rarity = [gas_rarity, liquid_rarity, solid_rarity]
        for mineral_group in xrange(0, 3):
            # 1st loop cycles through mineral groups
            for mineral in xrange(0, 10):
                base_price = 0
                # 2nd loop cycles through each mineral
                if planets[planet].minerals[mineral_group][mineral] > 0:
                    base_price = max_value / planets[planet].minerals[mineral_group][mineral]
                    random_price_change = random.randint(1, 2)
                    if random_price_change == 1:
                        base_price += base_price / random.randint(10, 20)
                    if random_price_change == 2:
                        base_price -= base_price / random.randint(10, 20)
                planets[planet].price_sell[mineral_group][mineral] = base_price

number_of_planets = int(raw_input("Choose how many planets"))

elements = create_elements()
elements_rarity = assign_minerals_rarity()

planets = [Planet() for x in xrange(number_of_planets)]

for tick in xrange(1, 100):
    add_minerals(number_of_planets, elements_rarity)
    find_price(number_of_planets, elements_rarity)
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

# the code works but it seems like this is bad practise is some way? compiler says it shouldn't work
