import random
import numpy as np


## POSSIBLE STRATEGIES ##
def always_defect(history, memory):
    return 0, memory


def always_cooperate(history, memory):
    return 1, memory

# SOLID STRATEGY THAT PLAYS NICELY WITH MOST
def default(history, memory):
    MAX = 0
    MIN = -4
    #RANDOMCOOP = 10
    coop_level = 0 if memory is None else memory

    n = history.shape[1]
    if n >= 1:
        coop_level += 1 if history[1, -1] else -1
        #if random.random() < 1 / RANDOMCOOP:
          #coop_level = MAX

    if coop_level > MAX:
        coop_level = MAX
    if coop_level < MIN:
        coop_level = MIN
    choice = coop_level >= 0

    return choice, coop_level


## SETTINGS (THESE WERE OPTIMIZED WITH ANOTHER ALGORITM) ##
FIRST_STRAT = default
DEFAULT_STRAT = default
#EMA_SMOOTHING = 2
#EMA_SAMPLE = 10
MA_SAMPLE = 15 # Used to determine a length of a "moving average" of the previous moves (reacts more quickly the lower the value is)
CORR_SAMPLE = 18 # Used to determine a length of a correlation calculation (reacts more quickly the lower this value is)
CORRELATION_THRESHOLD = 0.4 # When the correlation is below this threshold, the strategy determines that the opponent is not reacting.
TIT_FOR_TAT_THRESHOLD = 0.8 # When the correlation is above this, the strategy determines the opponent to be a "Tit for Tat" style strategy.
COOP_THRESHOLD = 0.8 # If the moving average is above this value, the strategy determines the opposing strategy to be cooperating, and will ignore defects until this is breached.
WRONGING_THRESHOLD = 1 # Number of times the bot must be defected against in a row to begin to change things up.
REVIVE_CHECK_NUM = 3 # Number of defects in a row that must occur to trigger a "revive."


def strategy(history, memory):
    # First round
    if history.shape[1] == 0:
        memory = { # Initialize the memory
            "strat": FIRST_STRAT,
            #"coop_ratio_ema": 0,
            "strat_memory": None,
            "wronged": False, # If the opponent has ever defected
            "concurrent_wrongings": 0, # Defects in a row (needed to trigger Wronged)
            "is_reviving": False, # Whether a revive is being undertaken
            "revive_failed": False, # Whether a revive has previously failed and soh
        }
        choice, memory["strat_memory"] = memory["strat"](history, memory["strat_memory"])
    # Remainder of the game
    else:
        # Some values used in calculations
        opponent_last = history[1, -1]
        turns_total = history.shape[1]

        # Exponential moving average of cooperation (weights more recent values highly)
        #c = EMA_SMOOTHING / (1 + EMA_SAMPLE)  # weighting constant for EMA
        #memory["coop_ratio_ema"] = opponent_last * c + memory["coop_ratio_ema"] * (1 - c)

        r = get_correlation(history, min(CORR_SAMPLE,turns_total))
        average = get_MA(history, MA_SAMPLE, turns_total)

        # Test for a "dead" TFT situation that needs a revive to revitalize score
        sum_defects = 0
        for i in range(-min(turns_total, REVIVE_CHECK_NUM), 0):
            sum_defects += (not history[0, i]) and (not history[1, i])
        if sum_defects == REVIVE_CHECK_NUM and not memory["revive_failed"]:
            memory["is_reviving"] = True

        # Makes whole strategy act like grimTrigger, but instead of just defecting, changes strategy based on data to best combat opponent
        if not memory["wronged"] and opponent_last == 0:
            memory["concurrent_wrongings"] += 1
            if memory["concurrent_wrongings"] >= WRONGING_THRESHOLD:
              memory["wronged"] = True
        else:
            memory["concurrent_wrongings"] = 0

        # Testing conditions to change the strategy
        curr_strat = memory["strat"]
        if memory["wronged"]:
            if memory["is_reviving"] and not memory["revive_failed"]:
                strat = always_cooperate
                if history[0,-1] and history[0, -2] and history[1, -1]:  #If opponent took the coop
                    memory["is_reviving"] = False
                    memory["wronged"] = False #become chums once again
                    strat = FIRST_STRAT
                elif history[0, -1] and history[0,-2] and not history[1, -1]:  # Oppenent continues to defect
                    memory["is_reviving"] = False
                    memory["revive_failed"] = True
                    strat = DEFAULT_STRAT
            elif r > TIT_FOR_TAT_THRESHOLD or average >= COOP_THRESHOLD:# If it is tit-for-tating or jossing then cooperate to get most points
              strat = always_cooperate
            elif r < CORRELATION_THRESHOLD:# If it is not responding then defect is the optimal strategy
              strat = always_defect
            else:
              # If all else fails, go back to basics
              strat = DEFAULT_STRAT
            memory["strat"] = strat

        # If the strategy has changed, reset memory
        if curr_strat is not memory["strat"]:  
            memory["strat_memory"] = None
        
        choice, memory["strat_memory"] = memory["strat"](history, memory["strat_memory"])
    return choice, memory


def get_correlation(history, turns):
    # Correlation between my moves and opponent's next moves
    sum_x = 0
    sum_y = 0
    sum_xy = 0
    n = turns - 1
    for i in range(-n, -1):
        last_move = history[0, i]
        opp_next_move = history[1, i + 1]
        sum_x += last_move
        sum_y += opp_next_move
        sum_xy += last_move * opp_next_move
    # moves are 0 and 1, so squaring makes no difference
    sum_xx, sum_yy = sum_x, sum_y
    denom = np.sqrt((n * sum_xx - sum_x * sum_x) * (n * sum_yy - sum_y * sum_y))
    return (n * sum_xy - sum_x * sum_y) / (denom if denom else 1)


def get_MA(history, length, turns_total):
    # Moving average of last n moves
    sum_moves = 0
    total = min(turns_total, length)
    for i in range(-total, 0):
        sum_moves += history[1, i]
    return sum_moves / total
