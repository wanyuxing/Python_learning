"""
Word Wrangler game
@Author: Henry Wan
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 1 or len(list1) == 0:
        return [item for item in list1]
    else:
        if list1[-1] == list1[-2]:
            return remove_duplicates(list1[:-1])
        else:
            new_list = remove_duplicates(list1[:-1])
            new_list.append(list1[-1])
            return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if len(list1) == 0 or len(list2) == 0:
        return []
    else:
        if list1[0] == list2[0]:
            new_list = list([list1[0]])
            new_list.extend(intersect(list1[1:], list2[1:]))
            return new_list
        elif list1[0] < list2[0]:
            return intersect(list1[1:], list2)
        else:
            return intersect(list1, list2[1:])

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    if len(list1) == 0 or len(list2) == 0:
        new_list = [item for item in list1]
        new_list.extend(list2)
        return new_list
    else:
        if list1[0] <= list2[0]:
            new_list = list([list1[0]])
            new_list.extend(merge(list1[1:], list2))
            return new_list
        else:
            new_list = list([list2[0]])
            new_list.extend(merge(list1, list2[1:]))
            return new_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 0 or len(list1) == 1:
        return [item for item in list1]
    else:
        mid = len(list1) / 2
        left = merge_sort(list1[:mid])
        right = merge_sort(list1[mid:])
        return merge(left, right)

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    else:
        first = word[0]
        rest = gen_all_strings(word[1:])
        new = []
        for item in rest:
            if len(item) > 0:
                for pos in range(len(item)):
                    new.append(item[:pos] + first + item[pos:])
                new.append(item + first)
        new.append(first)
        new.extend(rest)
        return new

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    ans = []
    for line in netfile.readlines():
        ans.append(line[:-1])
    return ans

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
