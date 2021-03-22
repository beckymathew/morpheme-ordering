PYTHON = "/u/nlp/anaconda/main/anaconda3/envs/py37-mhahn/bin/python"

import os
import subprocess
import sys
import glob

optimized = glob.glob("results/*/optim*")

for o in optimized:
  subprocess.call([PYTHON, "forWords_Celex_EvaluateWeights_MorphemeGrammar_FullData.py", "--model="+o])
  subprocess.call([PYTHON, "forWords_Japanese_RandomOrder_FormsPhonemesFull_FullData_Heldout.py", "--model="+o])

