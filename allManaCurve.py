import json 
import numpy as np
import csv
from pprint import pprint 
import matplotlib.pyplot as plt

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def allManaCurve():
  json_data = open("AllSets.enUS.json")
  data = json.load(json_data, object_hook=_decode_dict)
  json_data.close()

  missionCards = filter(lambda x: ("collectible" in x), data["Missions"])
  classicCards = filter(lambda x: ("collectible" in x), data["Classic"])
  naxCards = filter(lambda x: ("collectible" in x), data["Curse of Naxxramas"])
  systemCards = filter(lambda x: ("collectible" in x),data["System"])
  creditsCards = filter(lambda x: ("collectible" in x),data["Credits"])
  basicCards = filter(lambda x: ("collectible" in x),data["Basic"])
  debugCards = filter(lambda x: ("collectible" in x),data["Debug"])
  promotionCards = filter(lambda x: ("collectible" in x),data["Promotion"])
  rewardCards = filter(lambda x: ("collectible" in x),data["Reward"])
  gvgCards = filter(lambda x: ("collectible" in x),data["Goblins vs Gnomes"])
  
  allCards = missionCards + classicCards + naxCards + systemCards + creditsCards + basicCards + debugCards + promotionCards + rewardCards + gvgCards

  allCards = filter(lambda x: ("cost" in x), allCards)

  types = {}
  for card in allCards: 
    typeCard = card["type"]
    if typeCard in types: 
      types[typeCard] += 1
    else:
      types[typeCard] = 1


  manas = [x for x in range(0,21)]
  minionDict = dict.fromkeys(manas,0)
  spellsDict = dict.fromkeys(manas,0)
  weaponsDict = dict.fromkeys(manas,0)

  for card in allCards:
    cost = card["cost"]
    typeCard = card["type"]
    if (typeCard == "Minion"):
      minionDict[cost] += 1
    elif (typeCard == "Spell"):
      spellsDict[cost] += 1
    else: 
      weaponsDict[cost] += 1


  fig, ax = plt.subplots()
  ind = np.arange(21)
  width = 0.35
  i = 0
  while (i < 21): 
    minion = minionDict[i]
    spell = spellsDict[i]
    weapon = weaponsDict[i]
    rect1 = ax.bar(ind[i], minion, width, color="green", align="center")
    rect2 = ax.bar(ind[i], spell, width, bottom=minionDict[i], color="blue", align="center")
    rect3 = ax.bar(ind[i], weapon, width, bottom=minion+spell, color="black", align="center")
    i += 1
  

  ax.set_ylabel('Number of cards')
  ax.set_title("Mana Curve for All Cards")
  ax.set_xlabel("Mana Cost")
  ax.set_xticks(ind)
  ax.legend([rect1, rect2, rect3], ['Minions', 'Spells', 'Weapons'])
  plt.show()

allManaCurve()
