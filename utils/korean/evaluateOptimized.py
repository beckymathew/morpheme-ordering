PYTHON = "/u/nlp/anaconda/main/anaconda3/envs/py37-mhahn/bin/python"

import os
import subprocess
import sys
import glob

optimized = glob.glob("results/*/optim*")

for o in optimized:
  subprocess.call([PYTHON, "forWords_Korean_EvaluateWeights_MorphemeMeanings_WithoutAdnominals_DoubleSplit_Repeats_Seg1.py", "--model="+o])
  subprocess.call([PYTHON, "forWords_Korean_RandomOrder_MorphemeMeanings_WithoutAdnominals_DoubleSplit_Repeats_Seg1.py", "--model="+o])


