import random

# discovered classmethod! made these class methods because they are used in 3 other classes, yay!
def get_language():
    # IMPORTS MY LANGUAGE TEXT FILE WHICH CONTAINS A LIST OF FICTIONAL "VERBS"
    lines = []
    with open('language.txt') as language:
        for line in language:
            lines.append(line.strip())
    return lines


def create_word(min_verb_, max_verb):
    # creates a word by getting the verb list and randomly selecting non-repeating verbs to make words
    verbs_list = get_language()
    word = ""  # created word
    previous_verb = ""  # previous used verb
    verbs = random.randint(min_verb_, max_verb)
    for x1 in xrange(0, verbs):
        random_verb = random.choice(verbs_list)
        if previous_verb == random_verb:
            while previous_verb == random_verb:
                random_verb = random.choice(verbs_list)
        previous_verb = random_verb
        word += random_verb
    return word