#FROZEN FILE
#DO NOT EDIT
import random
import numpy as np

def strategy(history, memory):
  MAX = 0
  MIN = -2
  if memory is None:
    coop_level = 0
  else:
    coop_level = memory
  n = history.shape[1]
  if n >= 1:
    coop_level += 1 if history[1,-1] else -1

  if coop_level > MAX:
    coop_level = MAX
  if coop_level < MIN:
    coop_level = MIN
  choice = coop_level >= 0

  return choice, coop_level