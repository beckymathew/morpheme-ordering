# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff
import os

objectiveName = "LM"
from corpus import CORPUS
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default=CORPUS)
parser.add_argument("--model", dest="model", type=str)
parser.add_argument("--alpha", dest="alpha", type=float, default=1.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=4)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))
import random



args=parser.parse_args()
print(args)


assert args.alpha >= 0
assert args.alpha <= 1
assert args.delta >= 0
assert args.gamma >= 1





myID = args.idForProcess


TARGET_DIR = "results/"+__file__.replace(".py", "")



posUni = set() 

posFine = set() 

def getRepresentation(lemma):
    return lemma["coarse"]

def getSurprisalRepresentation(lemma):
    return lemma["fine"]

from math import log, exp
from random import random, shuffle, randint, Random, choice

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]

from corpusIterator_V import CorpusIterator_V

originalDistanceWeights = {}

morphKeyValuePairs = set()

vocab_lemmas = {}

import turkish_segmenter_coarse
import turkish_segmenter
def processVerb(verb, data_):
    # assumption that each verb is a single word
   for vb in verb:
      labels = vb["morph"]
      morphs = turkish_segmenter_coarse.get_abstract_morphemes(labels)
      fine = turkish_segmenter.get_abstract_morphemes(labels)
      morphs[0] = vb["lemma"] # replace "ROOT" w actual root
      fine[0] = vb["lemma"] # replace "ROOT" w actual root
      assert len(morphs) == len(fine)
      lst_dict = []
      for i in range(len(fine)):
        morph_dict = {"fine": fine[i], "coarse": morphs[i]}
        lst_dict.append(morph_dict)
      data_.append(lst_dict)

corpusTrain = CorpusIterator_V(args.language,"train", storeMorph=True).iterator(rejectShortSentences = False)
corpusDev = CorpusIterator_V(args.language,"dev", storeMorph=True).iterator(rejectShortSentences = False)

pairs = set()
counter = 0
data_train = []
data_dev = []
for corpus, data_ in [(corpusTrain, data_train), (corpusDev, data_dev)]:
  for sentence in corpus:
    verb = []
    for line in sentence:
       if line["posUni"] == "VERB":
          if 'VerbForm=Vnoun' in line["morph"]:
               continue
          verb.append(line)
          processVerb(verb, data_)
          verb = []

with open("output/corpusSize.txt", "w") as outFile:
  print(len(data_train) + len(data_dev), file=outFile)
  print(len(data_train), file=outFile)

  print(len(data_dev), file=outFile)

