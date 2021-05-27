#FROZEN FILE
#DO NOT CHANGE
import random
import numpy as np

def strategy(history, memory):
  
  if memory is None:
    MAX = 0
    coop_level = 0
  else:
    MAX, coop_level = memory
  n = history.shape[1]
  if n >= 1:
    coop_level += 1 if history[1,-1] else -1

  if coop_level > MAX:
    coop_level = MAX
  choice = coop_level >= 0

  return choice, (MAX,coop_level)