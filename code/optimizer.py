import prisonersDilemma as pd
import threading
import importlib

PREFIX = "code/"
STRATEGY_FOLDER = "strategies"
RESULTS_FILE = "results.txt"
A = 0
C = 10
tlock = threading.Lock()

class optThread(threading.Thread):
  def __init__(self, a,b):
    threading.Thread.__init__(self)
    self.a = a
    self.b = b
  
  def run(self):
    runSegment(self.a, self.b)

def runSegment(a,b):
    bd = importlib.import_module("strategies.our.bettorDetector")
    maximum = 0
    current = 0, 0, 0
    max_inputs = current
    for i in range(a, b):
      bd.TIT_FOR_TAT_THRESHOLD = i/C
      for j in range(A, C):
        bd.CORRELATION_THRESHOLD = j/C
        for k in range(5, 26):
          bd.CORRELATION_SAMPLE = k
          score = pd.runFullPairingTournament(PREFIX+STRATEGY_FOLDER, PREFIX+RESULTS_FILE)
          current = i/C, j/C, k
          if score > maximum:
            maximum = score
            max_inputs = current
          print("Current: "+str(current), "Maximum: "+str(max_inputs),score,maximum)

threads = []

try:
  t1 = optThread(0,5)
  t2 = optThread(5,10)
  t1.start()
  t2.start()
  threads.append(t1)
  threads.append(t2)
except:
  print("Thread Error")

for t in threads:
  t.join()