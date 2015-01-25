import json 
import csv
from pprint import pprint 

def jsonDecode(filename):
  json_data = open(filename)
  data = json.load(json_data)
  json_data.close()

  #Sets are different categories of cards 
  #The sets are Missions, Classic, Curse of Naxxramas, System
  #Credits, Basic, Debug, Promotion, Reward, Goblins vs Gnomes
  allSets = data.keys()

  missionsCards = data["Missions"]
  classicCards = data["Classic"]
  naxCards = data["Curse of Naxxramas"]
  systemCards = data["System"]
  creditsCards = data["Credits"]
  basicCards = data["Basic"]
  debugCards = data["Debug"]
  promotionCards = data["Promotion"]
  rewardCards = data["Reward"]
  gvgCards = data["Goblins vs Gnomes"]
  
  maxKeys = []
  for cards in missionsCards:
    keys = cards.keys()
    if (len(keys) > len(maxKeys)):
      maxKeys = keys 

  maxKeys += ["attack", "durability", "playerClass"]
  f = open('missioncards.csv','wb')
  w = csv.DictWriter(f,maxKeys)
  w.writeheader()
  w.writerows(missionsCards)
  f.close()

jsonDecode("AllSets.enUS.json")