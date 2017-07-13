import os
import sys
from random import choice, randint
import string
import twitter

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    initial_text = ""

#     for filename in filenames:
#         text_file = open(filename)
#         body = body + text_file.read()
#         text_file.close()

#     return body

    for item in file_path:
        initial_text = initial_text + open(item).read()

    return initial_text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each n_gram (except the last) will be a key in chains:

    bigram example:
        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    split_text = text_string.split()

    split_length = len(split_text)

    n_gram_length = randint(2, 5)

    #Loop through all words in the split text list expect for final two words
    for i in range(split_length - n_gram_length):
        # Creates a list to hold n words for our n-gram
        tuple_list = []

        # Based on user inputted n-gram lengths we loop through split_text
        # and adds the specified number of words to the tuple_list
        for n in range(n_gram_length):
            tuple_list.append(split_text[i + n])

        n_gram = tuple(tuple_list)

        if n_gram in chains:
            chains[n_gram].append(split_text[i + n_gram_length])
        else:
            chains[n_gram] = [split_text[i + n_gram_length]]

    #Add final tuple using negative indicies
    final_tuple = tuple(split_text[-n_gram_length:])

    #if its in chains get the list and concat with a None type
    chains[final_tuple] = chains.get(final_tuple, []) + [None]

    return chains


def make_text(chains):
    """Return text from chains."""
    # Setting that won't allow result to exceed 140 characters
    max_characters = 140
    #  Counts character to ensure we are under 140 characters"
    char_count = 0

    words = []

    chosen_word = ""

    end_punct = ["?", ".", "!"]

    all_punct = string.punctuation

    #This loop means: While the chosen word is not None or "" (empty string).
    while not chosen_word:
        # Choosing initial tuple key & choosing random associated value.
        initial_key = choice(chains.keys())
        if initial_key[0][0].isupper():
            chosen_word = choice(chains[initial_key])

    # Adding inital key tuple, to make a logical start to the sentence
    # (initial tuple and chosen word tuple together).
    words.extend(initial_key + (chosen_word,))

    # Adds character count for the initial key & chosen word, with spaces between.
    char_count = char_count + len(" ".join(words))

    # New key is the 1st index of current(or ititial) key, plus chosen word tuple.
    # It then can be used/reassigned in the while loop below
    # (while chosen_word is not None)
    new_key = (initial_key[1:] + (chosen_word,))

    # This generates the Markov chain...we fear it is not DRY. Clean this up!
    while chosen_word is not None:
        # Rebinds current key to new_key, selects random value, and assigns
        # new key to evaluate.
        current_key = new_key
        chosen_word = choice(chains[current_key])
        new_key = (current_key[1:] + (chosen_word,))
        # Ensures that a None type is not added to our words list.
        if chosen_word is not None:
            # This checks to see if we are close to max characters and, if so,
            # selects a final word.
            if char_count < max_characters - 20:
                words.append(chosen_word)
                char_count = char_count + len(chosen_word) + 1
            else:
                # If final chosen word already has appropriate ending
                # punctuation, adds it to words and breaks loop.
                if chosen_word[-1] in end_punct:
                    words.append(chosen_word)
                    break
                else:
                    # Value found variable used to track whether any other
                    # associated values in current_key already has end
                    # punctuation and, if so, adds it to words and breaks loop.
                    value_found = False
                    for value in chains[current_key]:
                        if value[-1] in end_punct:
                            words.append(value)
                            value_found = True
                            break
                    # If no values for current_key have end punctuation,
                    # replaces any existing puctuation with end punctuation,
                    # or adds a random ending punctuation mark.
                    if value_found is False:
                        if chosen_word[-1] in all_punct:
                            chosen_word = chosen_word.replace(chosen_word[-1],
                                                              choice(end_punct))
                        else:
                            chosen_word = chosen_word + choice(end_punct)
                        words.append(chosen_word)
                        break
    # print char_count

    # returns a single string from words list, joined with a space between.
    return " ".join(words)


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # keep_tweeting = True

    while True:
        tweet_text = make_text(chains)
        status = api.PostUpdate(tweet_text)
        print status.text
        user_choice = raw_input("Press Enter to tweet again, or any other key to quit > ")
        # if user_choice.lower() != "q":
        #     break
        if user_choice == "":
            continue
        else:
            break


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

tweet(chains)

# -----------------HB CODE------

# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)

# def open_and_read_file(filenames):
#     """Given a list of files, open them, read the text, and return one long
#         string."""

#     body = ""

#     for filename in filenames:
#         text_file = open(filename)
#         body = body + text_file.read()
#         text_file.close()

#     return body


# def make_chains(text_string):
#     """Takes input text as string; returns dictionary of markov chains."""

#     chains = {}

#     words = text_string.split()

#     for i in range(len(words) - 2):
#         key = (words[i], words[i + 1])
#         value = words[i + 2]

#         if key not in chains:
#             chains[key] = []

#         chains[key].append(value)

#         # or we could replace the last three lines with:
#         #    chains.setdefault(key, []).append(value)

#     return chains


# def make_text(chains):
#     """Takes dictionary of markov chains; returns random text."""

#     key = choice(chains.keys())
#     words = [key[0], key[1]]
#     while key in chains:
#         # Keep looping until we have a key that isn't in the chains
#         # (which would mean it was the end of our original text)
#         #
#         # Note that for long texts (like a full book), this might mean
#         # it would run for a very long time.

#         word = choice(chains[key])
#         words.append(word)
#         key = (key[1], word)

#     return " ".join(words)