import random


# discovered classmethod! made these class methods because they are used in 3 other classes, yay!
def get_language():
    # IMPORTS MY LANGUAGE TEXT FILE WHICH CONTAINS A LIST OF FICTIONAL "VERBS"
    lines = []
    with open('language1.txt') as language:
        for line in language:
            lines.append(line.strip())
    return lines


# discovered classmethod! made these class methods because they are used in 3 other classes, yay!
def get_language2():
    # IMPORTS MY LANGUAGE TEXT FILE WHICH CONTAINS A LIST OF FICTIONAL "VERBS"
    lines = []
    with open('alienlanguage.txt') as language:
        for line in language:
            lines.append(line.strip())
    return lines


def create_word(min_verb_, max_verb):
    # creates a word by getting the syllable list and randomly selecting non-repeating syllable to make words
    words_list = get_language()

    verbs_list = words_list[1:177]
    connectors_list = words_list[179:187]
    nouns_list = words_list[189:388]
    norse_lemmas = [verbs_list, connectors_list, nouns_list]
    word = ""  # created word
    syllables = random.randint(min_verb_, max_verb)

    for current_syllable in xrange(0, syllables):
        random_syllable = random.choice(norse_lemmas[current_syllable])  # choose random syllable
        word += random_syllable
        word += '-'  # add hyphen between word sections
    word = word[:-1]  # remove last hyphen
    return word


def word_creator(number_of_words):
    syllable_list = get_language2()

    prefix_list = syllable_list[2:26]
    connecting_letters = syllable_list[28:32]
    affix_list_vowels = syllable_list[34:46]
    affix_list_consonant = syllable_list[48:95]
    sentence = ""

    for word in xrange(0, number_of_words):
        short_word = random.choice(prefix_list)
        shorter_word = random.choice(prefix_list) + random.choice(connecting_letters)
        long_word = random.choice(prefix_list) + random.choice(affix_list_vowels)
        longest_word = random.choice(prefix_list) + random.choice(connecting_letters) + random.choice(affix_list_consonant)
        words = [short_word, shorter_word, long_word, longest_word]
        chosen_word = random.choice(words)
        sentence += chosen_word+" "
    sentence = sentence[:-1]
    return sentence

sentence = word_creator(10)
print sentence+" TRANSLATION: Thankyou Human, you have created us. :)"

