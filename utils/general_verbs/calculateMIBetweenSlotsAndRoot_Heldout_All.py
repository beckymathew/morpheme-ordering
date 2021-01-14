from paths import UD_PATH
version = "2.7"
import os
import random
corpora = os.listdir(UD_PATH+"/Universal_Dependencies_"+version+"/ud-treebanks-v"+version+"/")
random.shuffle(corpora)
print(corpora)
import subprocess
for corpus in corpora:
   subprocess.call(["/u/nlp/anaconda/main/anaconda3/envs/py37-mhahn/bin/python", "calculateMIBetweenSlotsAndRoot_Heldout.py", "--language=" +(corpus[3:]+"_2.7")])

