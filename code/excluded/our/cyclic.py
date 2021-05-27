def strategy(history, memory):
  if memory==None:
    memory = 0
  else:
    memory = (memory+1) % len(CYCLE)
  return CYCLE[memory], memory

CYCLE = [0,0,0,1]