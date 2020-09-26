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
          verb.append(line)
          processVerb(verb, data_)
          verb = []

words = []

### splitting lemmas into morphemes -- each affix is a morpheme ###
affixFrequencies = {}
for verbWithAff in data_train:
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
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # abstract slot

from collections import defaultdict

joints = {slot : defaultdict(int) for slot in itos}
marginal_stem = {slot : defaultdict(int) for slot in itos}
marginal_aff = {slot : defaultdict(int) for slot in itos}

for verb in data_train:
     stem = getSurprisalRepresentation(verb[0])
     affixesPerSlot = {slot : "+".join([getSurprisalRepresentation(x) for x in verb[1:] if getRepresentation(x) == slot]) for slot in itos}
     for slot in affixesPerSlot:
         joints[slot][(stem, affixesPerSlot[slot])] += 1
         marginal_aff[slot][affixesPerSlot[slot]] += 1
         marginal_stem[slot][stem] += 1

from math import log

for slot in itos:
    total = sum([x for _, x in joints[slot].items()])
    assert total == len(data_train)
    totalMI = 0
    jointProbs = 0
    for stem, aff in joints[slot]:
        jointProb = joints[slot][(stem, aff)] / total
        jointProbs += jointProb
        marginalStem = marginal_stem[slot][stem] / total
        marginalAff = marginal_aff[slot][aff] / total
        totalMI += (jointProb * (log(jointProb) - log(marginalStem) - log(marginalAff)))
    print(slot, totalMI, jointProbs)
       
