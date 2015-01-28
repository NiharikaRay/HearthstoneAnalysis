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
  allCards = filter(lambda x: (x["type"] == "Minion"), allCards)

  manas = [x for x in range(0,21)]
  minionDict = dict.fromkeys(manas,0)

  for card in allCards:
    cost = card["cost"]
    minionDict[cost] += 1


  fig, ax = plt.subplots()
  ind = np.arange(21)
  indString = map(lambda x: str(x), ind)
  width = 0.75
  i = 0
  while (i < 21): 
    minion = minionDict[i]
    rect1 = ax.bar(ind[i], minion, width, color="green", align="center")
    if (minion != 0):
      ax.text(ind[i], minion + 1.05,  '%d'%int(minion),
                ha='center', va='bottom', fontsize=12, 
                fontname='Calibri')
    i += 1
  
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.set_axis_bgcolor('#ffefd5')
  ax.set_yticks(np.arange(90,step=10))
  ax.set_ylabel('Number of cards', fontsize=12, fontname='Calibri')
  ax.set_xlabel("Mana Cost", fontsize=12, fontname='Calibri')
  ax.set_xticks(ind)
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')
  ax.set_title("Minion Mana Curve", fontsize=20, fontname='Calibri')

  for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Calibri')
    label.set_fontsize(10)

  #plt.show()
  plt.savefig('minionManaCurve.png', bbox_inches='tight', facecolor='#ffefd5')

allManaCurve()
