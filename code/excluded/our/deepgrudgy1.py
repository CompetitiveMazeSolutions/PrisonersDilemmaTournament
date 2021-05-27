import random
import numpy as np

def strategy(history, memory):
  
  if memory is None:
    MAX = 0
    MIN = -2
    coop_level = 0
  else:
    MAX, MIN, coop_level = memory
  n = history.shape[1]
  if n >= 1:
    coop_level += 1 if history[1,-1] else -1.5
  if n >= 1:
    MAX += 0; MIN -= 1/n

  if coop_level > MAX:
    coop_level = MAX
  if coop_level < MIN:
    coop_level = MIN
  choice = coop_level >= 0

  return choice, (MAX,MIN,coop_level)