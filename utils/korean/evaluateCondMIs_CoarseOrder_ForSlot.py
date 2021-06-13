#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Estimate memory-surprisal tradeoff 

import random
import sys
from estimateTradeoffHeldout_Pairs import calculateMemorySurprisalTradeoff
from math import log, exp
from corpusIterator_V import CorpusIterator_V
from random import shuffle, randint, Random, choice
from frozendict import frozendict
import copy

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Korean-Kaist_2.6")

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

posUni = set()

posFine = set()

from korean_morpheme_meanings_michael import automatic_morpheme_meaning


# Translate a verb into an underlying morpheme
def getRepresentation(lemma):
   return lemma["coarse"]

def getSurprisalRepresentation(lemma):
   #print(lemma)
   #quit()
   return lemma["coarse"]+"@"+lemma["fine"]

from math import log, exp
from random import random, shuffle, randint, Random, choice

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]

from corpusIterator_V import CorpusIterator_V

originalDistanceWeights = {}

morphKeyValuePairs = set()

vocab_lemmas = {}


import allomorphy
# using label_grapheme version bc it's easier to see if the verb processing is correct
def processVerb(verb, data_):
    if len(verb) > 0:
          posFine = verb[0]["posFine"].split("+")
          lemma = verb[0]["lemma"].split("+")
          verbs = [{"posFine" : [], "lemma" : []}]
          for i in range(len(lemma)):
              if posFine[i] == "px" and i>0:
                  verbs.append({"posFine" : [], "lemma" : []})
              verbs[-1]["lemma"].append(lemma[i])
              verbs[-1]["posFine"].append(posFine[i])
          for verb_ in verbs:
              processVerb2([verb_], data_)

def processVerb2(verb, data_):
      # get flattened list of labels + morphemes
      flattened = []
      for group in verb:
         for morpheme in zip(group["posFine"], group["lemma"]):
           morph, fine_label = allomorphy.get_underlying_morph(morpheme[1], morpheme[0])
           flattened.append(morph + "_" + fine_label)

      joined_nouns = []
      # join consecutive nouns (excluding verbal like nbn non-unit bound noun)
      # consecutive nouns are usually a form of compounding
      for item in flattened: 
        if item[0] == "n" and not item[:3] == "nbn":
          if len(joined_nouns) > 0:
            if joined_nouns[-1][0] == "n" and not joined_nouns[-1][:3] == "nbn":
              joined_nouns[-1] += "_" + item 
        else:
          joined_nouns.append(item)

      # split on nonconsecutive nouns
      start = 0
      lsts = []
      for i, item in enumerate(joined_nouns):
        if item[0] == "n" and not item[:3] == "nbn":
          lsts.append(joined_nouns[start:i]) 
          start = i # start a new verb list beginning at this noun
        if i == len(joined_nouns) - 1: 
          lsts.append(joined_nouns[start:]) # append the last verb list
      
      # add each verb list to data
      for lst in lsts:
        if len(lst) > 0:
          lst2 = []
          lastVerbDeriv = max([0]+[i for i in range(len(lst)) if "xsv" in lst[i] or "_".join(lst[i].split("_")[::-1]) in ["xsv_되", "jp_이", "xsv_하", "xsm_하", "xsm_스럽", "xsm_하", "xsv_하"]])
          if lastVerbDeriv > 1:
             newStart = "&".join(lst[:lastVerbDeriv])
             lst = [newStart] + lst[lastVerbDeriv:]
#             print("UNITE", lst)
          for x in lst:
#              print(x)
              morph_label = x.split("_")
 #             print(morph_label)
              morph, fine_label = "_".join(morph_label[:-1]), morph_label[-1]
  #            print("107", x, fine_label, morph)
              analyzed = automatic_morpheme_meaning(grapheme=morph, label=fine_label)
              for y in analyzed:
                  for z in y.split("+"):
   #                  print(z)
                     lst2.append(frozendict({"coarse" : z[:z.index("_")], "fine" : z}))
          endingMorpheme = [i for i in range(1,len(lst2)) if lst2[i]["coarse"] in ["CONNECTOR", "NOMINALIZER"]]
          if len(endingMorpheme) > 0 and endingMorpheme[-1]+1 < len(lst2):
 #             print("CUT", lst2)
              lst2 = lst2[:endingMorpheme[0]+1]
          if len([1 for x in lst2[2:] if x["coarse"] == "DERIVATION"]) > 0:
              print("DERIV", lst2)
#          print(lst2)
          data_.append(lst2)
    #      print(lst2)

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
            # Clear existing verb if you see punctuation
            processVerb(verb, data_)
            verb = []
        elif line["posUni"] == "VERB" or line["posUni"] == "ADJ":
            # Clear existing verb if you see a new verb
            processVerb(verb, data_)
            verb = []
            verb.append(line)
        # AUX
        elif line["posUni"] == "AUX":
            # Auxiliary is new verb
            processVerb(verb, data_)
            verb = []
            verb.append(line)
        elif line["posUni"] in ["CCONJ", "SCONJ"]:
            # Subordinating conjunction is a new verb if it has xsv (verb derivational suffix)
            processVerb(verb, data_)
            verb = []
            if "xsv" in line["posFine"] or "+e" in line["posFine"]:
               verb.append(line)
        elif "paa" == line["posFine"].split("+")[0] or "pvg" == line["posFine"].split("+")[0]:
            processVerb(verb, data_)
            verb = []
            verb.append(line)
        else:
            # Reached end of verb
            processVerb(verb, data_)
            verb = []

words = []

# Collect morphemes into itos and stoi. These morphemes will be used to parameterize ordering (for Korean, we could use underlying morphemes or the coarse-grained labels provided in Kaist like ef, etm, etc.)
affixFrequencies = {}
for verbWithAff in data_train:
  for affix in verbWithAff[1:]:
    slot = getRepresentation(affix)
    affixFrequencies[slot] = affixFrequencies.get(slot, 0) + 1

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
elif args.model == "UNIV":
  import compatible
  weights = compatible.sampleCompatibleOrdering(itos_)
  print(weights)
#  quit()
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
    # Order the datasets based on the given weights
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
    auc, devSurprisalTable, pmis = calculateMemorySurprisalTradeoff(train, dev, args)
    return pmis
   
pmis = calculateTradeoffForWeights(weights)

def mean(x):
  return sum(x)/len(x)

def coarse(x):
   if "@" in x:
     return x[:x.index("@")]
   if x in ["EOS", "SOS", "PAD"]:
     return x
   assert False, x
from collections import defaultdict

pmis_coarse = defaultdict(list)
for x, y in pmis:
   pmis_coarse[(coarse(x), coarse(y))] += pmis[(x,y)]

with open(f"cond_mi_bySlot/{__file__}_{args.language}_{args.model.split('_')[-1]}", "w") as outFile:
 for x1, x2 in sorted(list(pmis_coarse)):
   if "PAD" in [x1, x2]:
     continue
   if "SOS" in [x1, x2]:
     continue
   if "EOS" in [x1, x2]:
     continue
   if len(pmis_coarse[(x1,x2)]) == 1:
     continue
   print("\t".join([str(q) for q in [x2, x1, len(pmis_coarse[(x1,x2)]), mean(pmis_coarse[(x1,x2)])]]), file=outFile) # Note that x2 x1 are reversed because the text is reversed when calculating the PMIs

