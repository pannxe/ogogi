# interactive_script.py
import sys
resultPath   = sys.argv[1]
problemDir   = sys.argv[2]
atCase       = sys.argv[3]

with open(resultPath) as f:
  res = [int(i) for i in f.read().strip().split()]
with open(problemDir + atCase + ".in") as f:
  sol = [int(i) for i in f.read().strip().split()]

if res != sorted(sol):
  print("P")
else:
  print("-")