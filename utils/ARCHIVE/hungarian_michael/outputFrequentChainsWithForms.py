# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from frozendict import frozendict

objectiveName = "LM"
from corpus import CORPUS
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default=CORPUS)
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

# TODO: update this for Korean
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

import hungarian_segmenter_coarse
import hungarian_segmenter
def processVerb(verb, data_):
    # assumption that each verb is a single word
   for vb in verb:
      labels = vb["morph"]
      morphs = hungarian_segmenter_coarse.get_abstract_morphemes(labels)
      fine = hungarian_segmenter.get_abstract_morphemes(labels)
      morphs[0] = vb["lemma"] # replace "ROOT" w actual root
      fine[0] = vb["lemma"] # replace "ROOT" w actual root
      lst_dict = []
      for i in range(len(fine)):
        morph_dict = {"fine": fine[i], "coarse": morphs[i]}
        lst_dict.append(morph_dict)
      data_.append({"parsed" : lst_dict, "original" : verb})

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

# bar_num_morphs(data)
words = []

data = data_train+data_dev
print(data[:5])
### splitting lemmas into morphemes -- each affix is a morpheme ###
affixFrequencies = {}
for verbWithAff in data:
  for affix in verbWithAff["parsed"][1:]: # TODO: why does this start at 1? mhahn: in Japanese, this is to only conider suffixes, not the stem. Should probably be changed for Korean.
        affixFrequencies[affix["coarse"]] = affixFrequencies.get(affix["coarse"], 0) + 1

itos = set() # set of affixes
for verbWithAff in data:
  for affix in verbWithAff["parsed"][1:]:
        itos.add(affix["coarse"])
itos = sorted(list(itos)) # sorted list of verb affixes
stoi = dict(list(zip(itos, range(len(itos))))) # assigning each affix and ID

itos_ = itos[::]
shuffle(itos_)
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # TODO: why?? mhahn: this amounts to a random assignment from affixes to even integers

from collections import defaultdict
affixChains = defaultdict(list)
for d in data:
   affixChains[tuple([y["fine"] for y in d["parsed"][1:]])].append(d["original"])

def prettyPrint(code, line, count):
    print("\t&\t".join(["+".join(code), line[0], line[1][0]["lemma"], line[1][0]["morph"], str(count)])+"  \\\\")

for x in sorted(list(affixChains), key=lambda x:len(affixChains[x]))[:]:
    chains = [("&".join([y["word"] for y in z]), z) for z in affixChains[x]]
    chainsCount = defaultdict(int)
    for z, _ in chains:
        chainsCount[z] += 1
    chainsCount = sorted(list(chainsCount.items()), key=lambda x:x[1], reverse=True)
 #   print("===========")
#    print(x, len(affixChains[x]))
    prettyPrint(x, [y for y in chains if y[0] == chainsCount[0][0]][0], chainsCount[0][1])
    for i in range(1,20):
      if(len(chainsCount)>i):
        prettyPrint(x, [y for y in chains if y[0] == chainsCount[i][0]][0], chainsCount[i][1])


