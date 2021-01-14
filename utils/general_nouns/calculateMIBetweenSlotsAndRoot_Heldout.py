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
      lst_dict.append({"coarse" : "Function", "fine" :  vb["dep"]})
      data_.append(lst_dict)

corpusTrain = CorpusIterator_V(args.language,"train", storeMorph=True).iterator(rejectShortSentences = False)
corpusDev = CorpusIterator_V(args.language,"dev", storeMorph=True).iterator(rejectShortSentences = False)


import random
corpusTotal = list(corpusTrain) + list(corpusDev)
random.shuffle(corpusTotal)

corpusTrain = corpusTotal[int(0.1*len(corpusTotal)):]
corpusDev = corpusTotal[:int(0.1*len(corpusTotal))]


pairs = set()
counter = 0
data_train = []
data_dev = []
for corpus, data_ in [(corpusTrain, data_train), (corpusDev, data_dev)]:
  for sentence in corpus:
    verb = []
    for line in sentence:
       if line["posUni"] == "NOUN":
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

numberOfValuesObservedForStemAndSlot_cached = {}

print("Now collecting counts")

overallCountsPerSlot = defaultdict(int)
for verb in data_train:
     stem = getSurprisalRepresentation(verb[0])
     affixesPerSlot = {slot : "+".join([getSurprisalRepresentation(x) for x in verb[1:] if getRepresentation(x) == slot]) for slot in itos}
     for slot in affixesPerSlot:
         joints[slot][(stem, affixesPerSlot[slot])] += 1
         overallCountsPerSlot[slot] += 1
         marginal_aff[slot][affixesPerSlot[slot]] += 1
         marginal_stem[slot][stem] += 1
         if (slot, stem) not in numberOfValuesObservedForStemAndSlot_cached:
            numberOfValuesObservedForStemAndSlot_cached[(slot, stem)] = set()
         numberOfValuesObservedForStemAndSlot_cached[(slot, stem)].add(affixesPerSlot[slot])

from math import log


print("Now evaluating")

unigramSurprisalPerSlot = {slot : 0 for slot in joints}
bigramSurprisalPerSlot = {slot : 0 for slot in joints}
countPerSlot = {slot : 0 for slot in joints}

c=0

for verb in data_dev:
     c += 1
     if c % 1000 == 0:
         print(c/len(data_dev))
     stem = getSurprisalRepresentation(verb[0])
     affixesPerSlot = {slot : "+".join([getSurprisalRepresentation(x) for x in verb[1:] if getRepresentation(x) == slot]) for slot in itos}
     for slot in affixesPerSlot:
         value = affixesPerSlot[slot]
         # unigram surprisal of that suffix
         unigramProb = (marginal_aff[slot][value] + 0.5) / (overallCountsPerSlot[slot] + len(marginal_aff[slot]) * 0.5)
         unigramSurprisal = -log(unigramProb)
         assert unigramSurprisal >= 0, unigramSurprisal
        # bigram surprisal of that suffix
         numberOfValuesObservedForStemAndSlot = len(numberOfValuesObservedForStemAndSlot_cached.get((slot, stem), []))
         if marginal_stem[slot][stem] > 0:
            bigramSurprisal = -log(max(joints[slot][(stem, affixesPerSlot[slot])] - 1.0, 0.0) + 1.0*numberOfValuesObservedForStemAndSlot * unigramProb) + log(marginal_stem[slot][stem])
            assert bigramSurprisal >= 0, bigramSurprisal
         else:
            bigramSurprisal = unigramSurprisal
         unigramSurprisalPerSlot[slot] += unigramSurprisal
         bigramSurprisalPerSlot[slot] += bigramSurprisal
         countPerSlot[slot] += 1

        
with open(f"results/{__file__}.tsv", "a") as outFile:
 for slot in itos:
    if slot not in countPerSlot:
      continue
    mostCommonAffixes = "&".join([str(x) for x in sorted(marginal_aff[slot].items(), key=lambda x:-x[1])[:5]])
    print(slot, (unigramSurprisalPerSlot[slot] - bigramSurprisalPerSlot[slot])/countPerSlot[slot], countPerSlot[slot], mostCommonAffixes)
    print("\t".join([str(x) for x in [args.language, slot, (unigramSurprisalPerSlot[slot] - bigramSurprisalPerSlot[slot])/countPerSlot[slot], countPerSlot[slot], mostCommonAffixes]]), file=outFile)




