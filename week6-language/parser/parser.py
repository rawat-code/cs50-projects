import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> S Conj S
S -> S Conj VP

NP -> N
NP -> Det N
NP -> Det Adj N
NP -> Det Adj Adj N
NP -> Det N PP
NP -> Det Adj N PP
NP -> Det Adj Adj N PP
NP -> N PP
NP -> NP Conj NP

VP -> V
VP -> V NP
VP -> V PP
VP -> V NP PP
VP -> V Adv
VP -> V NP Adv
VP -> V PP Adv
VP -> V NP PP Adv
VP -> Adv V
VP -> Adv V NP
VP -> Adv V PP
VP -> Adv V NP PP

PP -> P NP

"""



grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert sentence to a list of words.

    Preprocess sentence by converting it to lowercase and removing any
    words that do not contain at least one alphabetic character.
    """
    words = nltk.word_tokenize(sentence.lower())

    return [
        word
        for word in words
        if any(character.isalpha() for character in word)
    ]



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the tree.
    """
    chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            contains_np = any(
                child.label() == "NP"
                for child in subtree.subtrees()
                if child is not subtree
            )

            if not contains_np:
                chunks.append(subtree)

    return chunks



if __name__ == "__main__":
    main()
