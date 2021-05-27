## Detection Operation:
Start by cooperating

If the other side defects, then start using trying to detect their strategy

### Abusing cooperators

If the other side cooperates for a really long time, start defecting.
If the other side starts defecting, try to coax back into cooperation.
If coaxing fails, keep on defecting.

# Statistics From Moves
## Cooperate Ratios

Coop = 1, Defect = 0

### Moving Average
sum(lastnterms)/n

## React Correlation
Imagine moves on a graph, with our last move on the x-axis, and the opponent's next move
on the y-axis.

Finding the Correlation between the two will allow the algo to know if there is a response
from our moves.

# Most common strategies
static (don't react to our moves) --> alwaysDefect

tft -> tft

# IMPROVEMENTS TO BETTORDETECTOR
Detect flipping and always coop, if still flipping, defect

# Tit-for-Tat Rejuvination (dejosser)
Test if 3 double defects in a row
If so, do two coop
If the opponent responded with coop, engage coop mode (can still retest in future)
If the opponent responded with defect, never do this test again

#### MUST FIX
joss und detective