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
    # creates a word by getting the syllable list and randomly selecting non-repeating syllable to make words
    words_list = get_language()

    verbs_list = words_list[1:184]
    connectors_list = words_list[186:194]
    nouns_list = words_list[196:395]
    norse_lemmas = [verbs_list, connectors_list, nouns_list]
    word = ""  # created word
    syllables = random.randint(min_verb_, max_verb)

    for current_syllable in xrange(0, syllables):
        random_syllable = random.choice(norse_lemmas[current_syllable])  # choose random syllable
        word += random_syllable
        word += '-'  # add hyphen between word sections
    word = word[:-1]  # remove last hyphen
    return word
