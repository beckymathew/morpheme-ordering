#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Estimate memory-surprisal tradeoff 

import random
import sys
from corpus import CORPUS
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff
from math import log, exp
from corpusIterator_V import CorpusIterator_V
from random import shuffle, randint, Random, choice



objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default=CORPUS)

# May be REAL, RANDOM, REVERSE, or a pointer to a file containing an ordering grammar.
parser.add_argument("--model", dest="model", type=str)

# parameters for n-gram smoothing. See also estimateTradeoffHeldout.py
parser.add_argument("--alpha", dest="alpha", type=float, default=1.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=12)

# An identifier for this run of this script.
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))



args=parser.parse_args()
print(args)


assert args.alpha >= 0
assert args.alpha <= 1
assert args.delta >= 0
assert args.gamma >= 1

myID = args.idForProcess


TARGET_DIR = "estimates/"





def getRepresentation(lemma):
   return lemma["coarse"]

def getSurprisalRepresentation(lemma):
   return lemma["fine"]

from math import log, exp
from random import random, shuffle, randint, Random, choice


from corpusIterator_V import CorpusIterator_V



import japanese_segmenter_coarse
import japanese_segmenter
def processVerb(verb, data_):
    if len(verb) > 0:
      if "VERB" in [x["posUni"] for x in verb[1:]]:
        print([x["word"] for x in verb])
      morphs = [japanese_segmenter_coarse.get_abstract_morphemes(x["lemma"]) for x in verb]
      fine = [japanese_segmenter.get_abstract_morphemes(x["lemma"]) for x in verb]
      morphs[0] = verb[0]["lemma"]
      fine[0] = verb[0]["lemma"]
      assert len(morphs) == len(fine)
      lst_dict = []
      for i in range(len(fine)):
        morph_dict = {"fine": fine[i], "coarse": morphs[i]}
        lst_dict.append(morph_dict)
      data_.append(lst_dict)

# Load both training (for fitting n-gram model) and held-out dev (for evaluating cross-entropy) data
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
       if line["posUni"] == "PUNCT":
          processVerb(verb, data_)
          verb = []
          continue
       elif line["posUni"] == "VERB":
          processVerb(verb, data_)
          verb = []
          verb.append(line)
       elif line["posUni"] == "AUX" and len(verb) > 0:
          verb.append(line)
       elif line["posUni"] == "SCONJ" and line["word"] == 'て':
          verb.append(line)
          processVerb(verb, data_)
          verb = []
       else:
          processVerb(verb, data_)
          verb = []

words = []

# Collect morphemes into itos and stoi. These morphemes will be used to parameterize ordering (for Korean, we could use underlying morphemes or the coarse-grained labels provided in Kaist like ef, etm, etc.)
affixFrequencies = {}
for data_ in [data_train, data_dev]:
  for verbWithAff in data_:
    for affix in verbWithAff[1:]:
      affixLemma = getRepresentation(affix)
      affixFrequencies[affixLemma] = affixFrequencies.get(affixLemma, 0) + 1

itos = set() # set of affixes
for data_ in [data_train, data_dev]:
  for verbWithAff in data_:
    for affix in verbWithAff[1:]:
      itos.add(getRepresentation(affix))
itos = sorted(list(itos)) # sorted list of verb affixes
stoi = dict(list(zip(itos, range(len(itos))))) # assigning each affix and ID

itos_ = itos[::]
shuffle(itos_)
if args.model == "RANDOM": # Construct a random ordering of the morphemes
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
elif args.model in ["REAL", "REVERSE"]: # Measure tradeoff for real or reverse ordering of suffixes.
  weights = None
elif args.model != "REAL": # Load the ordering from a file
  weights = {}
  import glob
  files = glob.glob(args.model)
  assert len(files) == 1
  with open(files[0], "r") as inFile:
     next(inFile)
     for line in inFile:
        morpheme, weight = line.strip().split(" ")
        weights[morpheme] = int(weight)


def calculateTradeoffForWeights(weights):
    train = []
    dev = []
    # Iterate through the verb forms in the two data partitions, and linearize as a sequence of underlying morphemes
    for data, processed in [(data_train, train), (data_dev, dev)]:
      for verb in data:
         affixes = verb[1:]
         if args.model == "REAL": # Real ordering
            _ = 0
         elif args.model == "REVERSE": # Reverse affixes
            affixes = affixes[::-1]
         else: # Order based on weights
            affixes = sorted(affixes, key=lambda x:weights.get(getRepresentation(x), 0))


         for ch in [verb[0]] + affixes: # Express as a sequence of underlying morphemes (could also instead be a sequence of phonemes if we can phonemize the Korean input)
            processed.append(getSurprisalRepresentation(ch))
         processed.append("EOS") # Indicate end-of-sequence
         for _ in range(args.cutoff+2): # Interpose a padding symbol between each pair of successive verb forms. There is no relation between successive verb forms, and adding padding prevents the n-gram models from "trying to learn" any spurious relations between successive verb forms.
           processed.append("PAD")
         processed.append("SOS") # start-of-sequence for the next verb form
    
    # Calculate AUC and the surprisals over distances (see estimateTradeoffHeldout.py for further documentation)
    auc, devSurprisalTable = calculateMemorySurprisalTradeoff(train, dev, args)


    # Write results to a file
    model = args.model
    if "/" in model:
        model = model[model.rfind("_"):-4]+"-OPTIM"
    outpath = TARGET_DIR+args.language+"_"+__file__+"_model_"+(str(myID)+"-"+model if model == "RANDOM" else model)+".txt"
    print(outpath)
    with open(outpath, "w") as outFile:
       print(str(args), file=outFile)
       print(" ".join(map(str,devSurprisalTable)), file=outFile)
    return auc
   
auc = calculateTradeoffForWeights(weights)
print("AUC: ", auc)
