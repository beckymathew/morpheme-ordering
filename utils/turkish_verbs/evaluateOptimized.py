PYTHON = "/u/nlp/anaconda/main/anaconda3/envs/py37-mhahn/bin/python"

import os
import subprocess
import sys
import glob

optimized = glob.glob("results/forWords_Turkish_OptimizeOrder_Coarse_FineSurprisal/optim*")

for o in optimized:
  subprocess.call([PYTHON, "forWords_Turkish_EvaluateWeights_Coarse.py", "--model="+o])
  subprocess.call([PYTHON, "forWords_Turkish_RandomOrder_Coarse_FineSurprisal.py", "--model="+o])

