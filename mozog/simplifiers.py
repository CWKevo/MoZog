import typing as t

import string


DEFAULT_STOP_WORDS = {'a', 'an', 'so', 'the'}
PUNCTUATION = [punctuation for punctuation in string.punctuation]



def remove_punctuation(string: str, punctuation: t.Container[str]=PUNCTUATION) -> str:
    return ''.join([character for character in string if character not in punctuation])


def remove_stop_words(string: str, stop_words: t.Container[str]=DEFAULT_STOP_WORDS) -> str:
    return ' '.join([word for word in string.split(' ') if word not in stop_words])



if __name__ == "__main__":
    test_string = remove_stop_words(remove_punctuation("I have a giant, thicc, house with an object, so the house is joyful..."))

    print(test_string)
