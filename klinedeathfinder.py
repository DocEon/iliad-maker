#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:24:44 2017

@author: kenalba
"""
import nltk
import re

# This is a much cheatier way to get to what I want than the dictmaker. 
# If I start with Kline's deaths, I can generate new deaths based on his. There's enough here for a start.
# And if I want to expand to other translations, I should be able to find correspondances.
translations = ["kline"]
char_dict = {}

def load_translations():
    for translation in translations:
        f = open("translations/" + translation + ".txt", "r", encoding="utf8")
        raw = f.read()
    # be smart about if "Gutenberg" in raw:
        trans_list = raw.split("\n")
        return trans_list

kline = load_translations()

kline_index = open("kline_index.txt", "r", encoding = "utf8")
kline_index_raw = kline_index.read()
kline_index_list = kline_index_raw.split("\n \n\n")
death_list = [hero for hero in kline_index_list if "Killed by" in hero or "killed by" in hero]

hero_list = [line.split("\n") for line in death_list]

death_dict = {}
uncaught = []
for hero in death_list:
    ## this regex needs work. It catches just over half of death_list.
    ## alternatively, split each index into a list demarcated by newlines, and extract the info that way - that's the smart way to do this.
    
    hero_r = re.split('([A-zöë]*).*\\n\\n([A-z ,’]*).*\\n.*(Bk.*) [Kk]illed by ([A-zöë]*).\\n', hero)
    if len(hero_r) == 6:
        name = hero_r[1]
        title = hero_r[2]
        death_location = hero_r[3]
        killer = hero_r[4]
        death = ""
        for line in kline:
            if name in line and killer in line:
                death = line
        if name in death_dict:
            name = name + "2"
        death_dict[name] = (title, death_location, killer, death)
    else: uncaught.append(hero)

def memorialize(death_dict):
    for hero in death_dict:
        print("{}, {}, was killed by {} at {}".format(hero, death_dict[hero][0], death_dict[hero][2], death_dict[hero][1]))
        print(death_dict[hero][3])
        print("~~~~~\n")
        
## ([A-z, ]*)\\n\\n([A-z ,.’]*)\\n.*(Bk.*) Killed by ([A-z]*).\\n