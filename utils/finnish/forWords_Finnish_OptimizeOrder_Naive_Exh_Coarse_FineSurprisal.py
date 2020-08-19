# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from corpus import CORPUS
from estimateTradeoffInSample import estimateTradeoffInSample
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default=CORPUS)
parser.add_argument("--model", dest="model", type=str)
parser.add_argument("--alpha", dest="alpha", type=float, default=1.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=7)
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

import finnish_segmenter_coarse
import finnish_segmenter
def processVerb(verb, data_):
    # assumption that each verb is a single word
   for vb in verb:
      labels = vb["morph"]
      if "VerbForm=Part" in labels or "VerbForm=Inf" in labels:
          continue
      morphs = finnish_segmenter_coarse.get_abstract_morphemes(labels)
      fine = finnish_segmenter.get_abstract_morphemes(labels)
      morphs[0] = vb["lemma"] # replace "ROOT" w actual root
      fine[0] = vb["lemma"] # replace "ROOT" w actual root
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
          verb.append(line)
          processVerb(verb, data_)
          verb = []

words = []

affixFrequency = {}
for verbWithAff in data_train:
  for affix in verbWithAff[1:]:
    affixLemma = getRepresentation(affix)
    affixFrequency[affixLemma] = affixFrequency.get(affixLemma, 0)+1


itos = set()
for data_ in [data_train, data_dev]:
  for verbWithAff in data_:
    for affix in verbWithAff[1:]:
      itos.add(getRepresentation(affix))
itos = sorted(list(itos))
stoi = dict(list(zip(itos, range(len(itos)))))

itos_ = itos[::]
shuffle(itos_)
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # abstract slot

cached_stoi = {}
def getNumeric(x):
    if x not in cached_stoi:
      cached_stoi[x] = len(cached_stoi)+10
    return cached_stoi[x]

def calculateTradeoffForWeights(weights):
    # Order the datasets based on the given weights
    train = []
    dev = []
    for data, processed in [(data_train, train), (data_dev, dev)]:
      for verb in data:
         affixes = verb[1:]
         affixes = sorted(affixes, key=lambda x:weights.get(getRepresentation(x), 0)) 
         for ch in [verb[0]] + affixes:
            processed.append(getNumeric(getSurprisalRepresentation(ch)))
         processed.append(1)
         for _ in range(args.cutoff+2):
           processed.append(0)
         processed.append(2)
 #   print(processed[:100])
#    quit()
#    auc, devSurprisalTable = calculateMemorySurprisalTradeoff(train, train, args)

    auc, devSurprisalTable = estimateTradeoffInSample(train, args)
 #   print(auc, auc1)
  #  quit()
    return auc, devSurprisalTable
   

import os


print(itos)



from itertools import permutations 


# This will store the minimal AOC found so far and the corresponding position
mostCorrect, mostCorrectValue = 1e100, None

orders = list(permutations(itos))
shuffle(orders)

counter = 0
for order in orders:
   counter += 1
   weights_ = dict(list(zip(order, range(len(order)))))
   if counter % 10 == 0:
      print(counter)
      print(mostCorrectValue)
   resultingAOC, _ = calculateTradeoffForWeights(weights_)

   # Update variables if AOC is smaller than minimum AOC found so far
   if resultingAOC < mostCorrect:
      mostCorrectValue = weights_
      mostCorrect = resultingAOC
weights_ = mostCorrectValue
if True:
     _, surprisals = calculateTradeoffForWeights(weights_)

     if os.path.exists(TARGET_DIR):
       pass
     else:
       os.makedirs(TARGET_DIR)
     with open(TARGET_DIR+"/optimized_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
        print("-1", mostCorrect, str(args), surprisals, file=outFile)
        for key in itos_:
          print(key, weights_[key], file=outFile)
  
print(weights_)


