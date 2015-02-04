import json 
import csv
from pprint import pprint 

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


def jsonDecode(filename):
  json_data = open(filename)
  data = json.load(json_data, object_hook=_decode_dict)
  json_data.close()

  #Sets are different categories of cards 
  #The sets are Missions, Classic, Curse of Naxxramas, System
  #Credits, Basic, Debug, Promotion, Reward, Goblins vs Gnomes
  allSets = data.keys()

  missionCards = data["Missions"]
  classicCards = data["Classic"]
  naxCards = data["Curse of Naxxramas"]
  systemCards = data["System"]
  creditsCards = data["Credits"]
  basicCards = data["Basic"]
  debugCards = data["Debug"]
  promotionCards = data["Promotion"]
  rewardCards = data["Reward"]
  gvgCards = data["Goblins vs Gnomes"]
  
  setSets = [missionCards, classicCards, naxCards, systemCards,
            creditsCards, basicCards, debugCards, 
            promotionCards,rewardCards, gvgCards]

  nameSets = ["missionCards", "classicCards", "naxCards", 
              "systemCards", "creditsCards", "basicCards", 
              "debugCards", "promotionCards", "rewardCards",
              "gvgCards"]


  maxKeys = []
  
  for cardSets in setSets: 
    for cards in cardSets:
      keys = cards.keys()
      if (len(keys) > len(maxKeys)):
        maxKeys = keys 

  #I don't know why this has to happen 
  maxKeys += ["elite", "durability"]

  i = 0 
  folder = "cardCSVs/"
  for cardSets in setSets: 
    f = open(folder + nameSets[i] + '.csv','wb')
    w = csv.DictWriter(f,maxKeys)
    w.writeheader()
    w.writerows(cardSets)
    f.close()
    i += 1

jsonDecode("AllSets.enUS.json")