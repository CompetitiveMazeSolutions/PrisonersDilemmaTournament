def strategy(history, memory):
  if memory == None:
    memory = 1
  move = 0 if memory else 1
  return move, move 