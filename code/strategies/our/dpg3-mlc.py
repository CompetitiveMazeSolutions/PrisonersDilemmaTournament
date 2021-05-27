import random
import numpy as np

MAX = 1
MIN = -3
TESTLEN = 2
LASTCHANCE = 3
#DeeP Grudgy 3: Multiple Last Chance
def strategy(history, memory):
  n = history.shape[1]
  if memory is None:
    memory = {
      "LVL":0,
      "TESTRAT":False,
      "TESTCT":0,
      "CT":0,
      "RATIONAL":True
    }
    return 1, memory

  if memory["TESTCT"] > LASTCHANCE:
    return 0, memory

  coop_level = memory["LVL"]
  coop_level += 1 if history[1,-1] else -(1+np.log10(1+np.log10(n)))
  if coop_level > MAX:
    memory["RATIONAL"] = True
    coop_level = MAX
  if coop_level < MIN:
    coop_level = MIN
  memory["LVL"] = coop_level

  if memory["TESTRAT"]:
    if memory["CT"]:
      choice = 1
      memory["CT"] -= 1
      return choice, memory
    else:
      memory["RATIONAL"] = (sum(history[1,-TESTLEN:])>=1)
      memory["TESTRAT"] = False
  
  if coop_level < 0:
    if memory["RATIONAL"] and not memory["TESTRAT"]:
      memory["TESTRAT"]=True
      memory["CT"]=TESTLEN 
      memory["TESTCT"] += 1


  
  choice = coop_level >= 0 if memory["RATIONAL"] else 0
  return choice, memory