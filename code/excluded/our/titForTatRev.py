def strategy(history, memory):
    choice = 0
    if history.shape[1] >= 1 and history[1,-1] == 0: # Choose to cooperate if and only if the opponent just defected.
        choice = 1
    return choice, None