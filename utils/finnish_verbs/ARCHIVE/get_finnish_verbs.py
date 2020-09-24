# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Japanese_2.4")
parser.add_argument("--alpha", dest="alpha", type=float, default=0.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=15)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))
import random



args=parser.parse_args()
print(args)


assert args.alpha >= 0
assert args.alpha <= 1
assert args.delta >= 0
assert args.gamma >= 1





myID = args.idForProcess


TARGET_DIR = "/u/scr/mhahn/deps/memory-need-ngrams-morphology/"



posUni = set()

posFine = set()

def getRepresentation(lemma):
   if lemma == "させる" or lemma == "せる":
     return "CAUSATIVE"
   elif lemma == "れる" or lemma == "られる" or lemma == "える" or lemma == "得る" or lemma == "ける":
     return "PASSIVE_POTENTIAL"
   else:
     return lemma


from math import log, exp
from random import random, shuffle, randint, Random, choice

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]

from corpusIterator_V import CorpusIterator_V

originalDistanceWeights = {}

morphKeyValuePairs = set()

vocab_lemmas = {}

# import hungarian_segmenter
# def processVerb(verb): 
#    # assumption that each verb is a single word
#    for vb in verb:
#       labels = vb["morph"]
#       morphs = hungarian_segmenter.get_abstract_morphemes(labels)
#       data.append(morphs)

corpusTrain = CorpusIterator_V(args.language,"train", storeMorph=True).iterator(rejectShortSentences = False)
pairs = set()
counter = 0
data = []
for sentence in corpusTrain:
    verb = []
    for line in sentence:
       if line["posUni"] == "AUX":
          verb.append(line)
       elif line["posUni"] == "VERB":
          verb.append(line)
          data.append(verb)
          verb = []
       else:
         verb = []

# for lst in data:
#   if len(lst) > 1:
#     print(lst)
# quit()

import csv
with open("finnish_aux_verbs.tsv", "w") as fout:
   fc = csv.DictWriter(fout, fieldnames=data[0][0].keys(), dialect="excel-tab")
   fc.writeheader()
   for row in data:
      fc.writerows(row)
