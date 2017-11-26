#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:24:44 2017

@author: kenalba
"""
# import nltk
import re
import json

translations = ["kline"]

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
hero_dict = {}
reject_heroes = {}

def get_death(hero):
    # hero should be a dictionary entry of the form dict[hero][0] = (short_hero, title, death_loc, killer)
    # n.b. this should eventually take 'translation' as an argument; for now, it's just using Kline
    short_hero = hero[0]
    if " " not in hero[3]:
        killer = hero[3]
    else:
        temp = hero[3].split(" ")
        killer = temp[0]
    death = ""
    for line in kline:
        if short_hero in line and killer in line:
            death = line
    return death

for hero in hero_list:
    name = hero[0]
    for line in hero:
        if line.startswith("A") or line.startswith("The") or line.startswith("He"):
            title = line.split(".")[0]
        if "Killed" in line or "killed" in line:
            killed_line = line
        killed_re = re.split('(Bk.*) (?:Killed by) ([A-z öïë]*)\.', killed_line)
        killer = ""
        killed_at = ""
        short_name = name.split(",")
        if len(short_name) > 0:
            short_name = short_name[0]
        if len(killed_re) == 4:
            killer = killed_re[2]
            killed_at = killed_re[1]
            hero_info = (short_name, title, killed_at, killer)
            death = get_death(hero_info)
            hero_dict[name] = (short_name, title, killed_at, killer, death)
        else:
            killed_re = re.split('(Bk[XVI0-9]*) .*(?:killed by) ([A-z öëï]*)\.', killed_line)
            if len(killed_re) == 4:
                killer = killed_re[2]
                killed_at = killed_re[1]
                hero_info = (short_name, title, killed_at, killer)
                death = get_death(hero_info)
                hero_dict[name] = (short_name, title, killed_at, killer, death)
            else:
                reject_heroes[name] = (name, killed_line)
        
with open('deaths.json', 'w') as fp:
    json.dump(hero_dict, fp, indent=1)
    
def memorialize(death_dict):
    for hero in death_dict:
        print("{}, {}, was killed by {} at {}".format(hero, death_dict[hero][1], death_dict[hero][3], death_dict[hero][2]))
        print(death_dict[hero][4])
        print("~~~~~\n")