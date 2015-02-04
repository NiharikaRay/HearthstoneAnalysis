import json 
import numpy as np
import csv
from pprint import pprint 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

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

def getMechCards():
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

  allCards = filter(lambda x: (x["type"] == "Minion"), allCards)

  mechCards = []
  for card in allCards: 
    if ("race" in card):
      race = card["race"]
      if (race == "Mech"):
        mechCards += [card]

  return mechCards

def countClass():
  mechCards = getMechCards()
  classCount = {}
  classToCards = {}

  for card in mechCards:
    if ("playerClass" in card):
      playerClass = card["playerClass"]
      if (playerClass in classCount):
        classCount[playerClass] += 1
        classToCards[playerClass] += [card["name"]]
      else:
        classCount[playerClass] = 1
        classToCards[playerClass] = [card["name"]]
    else: #it's a neutral card
      if ("Neutral" in classCount):
        classCount["Neutral"] += 1
        classToCards["Neutral"] += [card["name"]]
      else:
        classCount["Neutral"] = 1
        classToCards["Neutral"] = [card["name"]]


  for (k, v) in classCount.iteritems():
    print "There are " + str(v) + " " + k + " mech cards"
    print "The " + k + " mech cards are: "
    pprint(classToCards[k])
    print "\n"



countClass()

