from collections import Counter


def collection_counter(list_1, list_2):
    """"Test if two list has the same values and return boolean value"""
    # https://stackoverflow.com/questions/26787743/efficiently-test-if-two-lists-have-the-same-elements-and-length
    what_value = sorted(list_1) == sorted(list_2)

    return what_value
