# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:50:37 2017

@author: Ken Alba
"""
## to do: fix the multiple-names problem that arises because of weird characters
## to do: identify which passages are deaths, or which passages are the same.

import nltk

f = open('list_of_the_dead.txt')
list_of_the_dead = [line[:-1].title() for line in f if len(line) > 1]

#translations = ["buckley", "butler", "chapman", "cowper", "derby", "kline", "langleafmyers", "pope"]
translations = ["buckley", "cowper", "derby"]
trans_dict = {}
char_dict = {}
pawns = []

def load_translations():
    for translation in translations:
        f = open("translations/" + translation + ".txt", "r", encoding="utf8")
        raw = f.read()
    # be smart about if "Gutenberg" in raw:
        tokens = nltk.sent_tokenize(raw)
        text = nltk.Text(tokens)
        trans_dict[translation] = text
    return trans_dict

def load_char_dict(trans_dict):
    for name in list_of_the_dead:
        print("Finding " + name)
        char_dict[name] = []
        for translation in trans_dict:
            for n in range(len(trans_dict[translation])):
                if name in trans_dict[translation][n]:
                    location =  n / len(trans_dict[translation])
                    char_dict[name].append((trans_dict[translation][n].strip("\n"), translation, location))
    return char_dict

def char_bio(name):
    print(name + " appears " + str(len(char_dict[name])) + " times across all translations.")
    for translation in translations:
        hits = [(line, location) for (line, source, location) in char_dict[name] if source == translation]
        print("~~~~~~~~~~~~~~~~~\n")
        print("{} appears {} times in {}\n".format(name, len(hits), translation))
        for x in range(len(hits)):
            print("{} at {}:".format(x+1, hits[x][1]))
            print(hits[x][0])
            print()

def get_pawns():
    pawns = [(char, len(char_dict[char])) for char in char_dict if len(char_dict[char]) < 20]
    return pawns

def get_one_hit_wonders():
    one_hit_wonders = [char for char in char_dict if len(char_dict[char]) == 3]
    return one_hit_wonders

def main():
    trans_dict = load_translations()
    char_dict = load_char_dict(trans_dict)
    command = input("Who do you want to see?\n")
    while command != "exit":
        char_bio(command)
        command = input("Who do you want to see?")