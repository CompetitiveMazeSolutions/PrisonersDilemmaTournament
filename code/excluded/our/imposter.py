
#fake detective: always choses to defect after start
def strategy(history, memory):
    testingSchedule = [1,0,1,1]
    gameLength = history.shape[1]
    choice = None
    
    if gameLength < 4: # We're still in that initial testing stage.
        choice = testingSchedule[gameLength]
    else:
        choice = 0;
    
    return choice, None