import random


# discovered classmethod! made these class methods because they are used in 3 other classes, yay!
def get_language():
    # IMPORTS MY LANGUAGE TEXT FILE WHICH CONTAINS A LIST OF FICTIONAL "VERBS"
    lines = []
    with open('language1.txt') as language:
        for line in language:
            lines.append(line.strip())
    return lines


def create_word(min_verb_, max_verb):
    # creates a word by getting the verb list and randomly selecting non-repeating verbs to make words
    words_list = get_language()
    verbs_list = words_list[1:184]
    connectors_list = words_list[186:194]
    nouns_list = words_list[196:395]
    norse_lemmas = [verbs_list, connectors_list, nouns_list]
    word = ""  # created word
    previous_verb = ""  # previous used verb
    verbs = random.randint(min_verb_, max_verb)
    for verb in xrange(0, verbs):
        random_verb = random.choice(norse_lemmas[verb])
        if previous_verb == random_verb:
            while previous_verb == random_verb:
                random_verb = random.choice(verbs_list)
        previous_verb = random_verb
        word += random_verb
        if verb <= 1:
            word += '-'
    return word
