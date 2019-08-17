#!/bin/python
import string
def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    pass


def isPunctuation(word):
    punc = []
    for ch in string.punctuation:
        punc.append(ch)
    for c in word:
        if c not in punc:
            return False
    return True

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    months = ["jan, feb, mar, april, jun, jul, aug, sept, oct, october, nov, november, dec, december"]
    days = ["monday, tuesday, wednesday, thursday, friday, saturday, sunday"]
    conj = ["and, or, but, as, if, where, because, since"]
    nums = ["one, two, three, four, five , six, seven , eight, nine, ten"]
    colors = ["blue, black, red, yellow, green, orange, purple"]
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric() or word.lower() in nums:
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    if word.endswith("ly") or word.endswith("ward") or word.endswith("wise"):
        ftrs.append("IS_ADVERB")
    if word.endswith("ity") or word.endswith("ment") or word.endswith("ness") or word.endswith("acy") or word.endswith("ship") or word.lower() in months or word == "MAY" or word.lower() in days or (i != 0 and word.isupper()):
        ftrs.append("IS_NOUN")
    if word.endswith("ate") or word.endswith("en") or word.endswith("ize") or word.endswith("ure") or word.endswith("ify") or word.endswith("er") or word.endswith("dom") or word.endswith("ite") or word.endswith("age") or word.endswith("ation") or word.endswith("ion") or word.endswith("ment") or word.endswith("ness"):
        ftrs.append("IS_VERB")
    if word.startswith("dis") or word.startswith("de"):
        ftrs.append("IS_OPPOSITE")
    if word.startswith("http") or word.startswith("@") or word.startswith("#") or word == "RT":
        ftrs.append("UNTAGGED")
    if word.lower() in conj:
        ftrs.append("IS_CONJUNCTION")
    if word.lower() in colors:
        ftrs.append("IS_COLOR")

    '''if word.startswith("pro")  or word.startswith("re") or word.startswith("pre"):
        ftrs.append("IS_POSITIVE")'''

    '''if (not word.startswith("#") and not word.startswith("@")) and (word.lower() in colors or word.endswith("ial") or word.endswith("ical") or word.endswith("ous")):
        ftrs.append("IS_ADJECTIVE")'''

    '''if isPunctuation(sent[i]):
        ftrs.append("IS_PUNCTUATION")'''

    '''if word.startswith("co") or word.startswith("sub"):
        ftrs.append("IS_NOUN_PREFIX")

    if word.endswith("able") or word.endswith("ible") or word.endswith("ial") or word.endswith("ical") or word.endswith("al") or word.endswith("ar") or word.endswith("less") or word.endswith("ous") or word.endswith("ious"):
        ftrs.append("IS_ADJECTIVE")'''

    '''if word.lower() == "i"  or word == "me" or word.lower() == "you" or word == "she": #or word.lower() == "he" or word == "him" or word == "her" or word.lower() == "they" or word.lower() == "it" or word.lower() == "them" or word.lower() == "this" or word.lower() == "these" or word.lower() == "that" or word.lower() == "those" or word.lower() == "their":
        ftrs.append("IS_PRONOUN")'''


    '''if word == "ok" or word == "okay":
        ftrs.append("IS_OK")'''
    ''''''

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "food" ]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
