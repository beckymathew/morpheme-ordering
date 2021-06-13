#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Estimate memory-surprisal tradeoff 

import random
import sys
from corpus import CORPUS
from estimateTradeoffHeldout_Pairs import calculateMemorySurprisalTradeoff
from math import log, exp
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


############################################################################################
############################################################################################


# for ordering


def getSegmentedForms(word): # return a list , preprocessing
   if "/" not in word[header["lemma"]] and "." not in word[header["lemma"]]:
     return [word]
   elif "/" in word[header["lemma"]]:
    assert word[header["lemma"]].count("/") == 1
    lemmas = word[header["lemma"]].split("/")
    word1 = word[::]
    word2 = word[::]
    word1[1] = lemmas[0]
    word2[1] = lemmas[1]

    word1[0] = "_"
    word2[0] = "_"
    if lemmas[0].startswith("sm") and lemmas[1].startswith("t^"): # merger between subject and tense/aspect marker (> 100 cases in the corpus)
        _ = 0
    elif word[header["analysis"]] == "NEG.POT": #keke, kebe. Compare Doke and Mokofeng, section 424. Seems to be better treated as an auxiliary, as it is followed by subject prefixes in the corpus.
       return None
    elif word[header["analysis"]] == "almost.PRF": # batlile = batla+ile. This is an auxiliary, not a prefix. Doke and Mokofeng, section 575.
       return None
    elif word[header["analysis"]] == "POT.PRF": # kile. This seems to be a prefix, as it is followed by subject prefixes in the corpus.
       return None
    elif word[header["analysis"]] == "be.PRF": # bile . Better treated as an auxiliary, for the same reason.
       return None
    elif word[header["analysis"]] == "do.indeed.PRF": # hlile. Same
       return None
    elif word[header["analysis"]] == "fill.belly.PRF": # Occurs a single time, excluded.
       return None
    else:
       print("SPLIT", word1, word2, word)
       assert False
    return [word1, word2]
   elif word[header["lemma"]] == "a.name" or word[header["lemma"]] == "a.place": #  exclude these data
     return None
   elif word[header["lemma"]].startswith("t^p.om"):
    # print(word)
     lemma1 = word[1][:3]
     lemma2 = word[1][4:]
     #print(lemma2)
     word1 = word[::]
     word2 = word[::]
     word1[1] = lemma1
     word2[1] = lemma2
 
     word1[0] = "_"
     word2[0] = "_"
     if lemma1.startswith("t^") and lemma2.startswith("om"):
   #      print(word)
         assert word[2].startswith("PRS")
         return [word2]
         _ = 0
     else:
        print("SPLIT", word1, word2, word)
        assert False
        return [word1, word2]
   elif word[header["lemma"]].startswith("t^p.rf"):
     lemma1 = word[1][:3]
     lemma2 = word[1][4:]
     #print(lemma2)
     word1 = word[::]
     word2 = word[::]
     word1[1] = lemma1
     word2[1] = lemma2
 
     word1[0] = "_"
     word2[0] = "_"
     if lemma1.startswith("t^") and lemma2.startswith("rf"):
         assert word[2].startswith("PRS")
         return [word2]
         _ = 0
     else:
        print("SPLIT", word1, word2, word)
        assert False
        return [word1, word2]
   else: # exclude these data
     return None

def getNormalizedForm(word): # for prediction
#   print(word)
   return stoi_words[word[header["lemma"]]]

myID = args.idForProcess


TARGET_DIR = "estimates/"

words = []

header = ["form", "lemma", "analysis", "type1", "type2"]
header = dict(list(zip(header, range(len(header)))))

def processWord(word):
   nonAffix = [x[-3] for x in word if x[-3] not in ["sfx","pfx"]]
#   print(nonAffix, len(word))

   assert len(nonAffix) == 1
   if nonAffix[0] == "v":
#      print( [x[-3] for x in word if x[-3] in ["sfx","pfx"]])

      words.append([x[8:] for x in word])

posUni = set() 

posFine = set() 

currentWord = []
with open("/u/scr/mhahn/CODE/acqdiv-database/csv/morphemes5.csv", "r") as inFile:
  next(inFile)
  for line in inFile:
     line = line.strip().replace('","', ',').split(",")
     if len(line) > 14:
#       print(line)
#       assert len(line) == 15, len(line)
       line[9] = ",".join(line[9:-4])
       line = line[:10] + line[-4:]
 #      print(line)
       assert len(line) == 14, len(line)
#     print(len(line))
     assert len(line) == 14, line
     if line[4] == "Sesotho":
#       print(line)
       if line[-3] == "sfx":
         currentWord.append(line)
       elif line[-3] == "pfx" and len(currentWord) > 0 and currentWord[-1][-3] != "pfx":
         #print([x[-3] for x in currentWord])
         processWord(currentWord)
         currentWord = []
  #       print("---")
         currentWord.append(line)
       elif line[-3] == "pfx":
         currentWord.append(line)
       elif line[-3] != "sfx" and len(currentWord) > 0 and currentWord[-1][-3] == "sfx":
         #print([x[-3] for x in currentWord])
         processWord(currentWord)
         currentWord = []
 #        print("---")
         currentWord.append(line)
       elif line[-3] not in ["sfx", "pfx"] and len(currentWord) > 0 and currentWord[-1][-3] != "pfx":
         #print([x[-3] for x in currentWord])
         processWord(currentWord)
         currentWord = []
#         print("---")
         currentWord.append(line)
       else:
          currentWord.append(line)
   #    print(line[-3])

#print(words)
#quit()



# Translate a verb into an underlying morpheme
def getRepresentation(lemma):
   key = lemma[header["lemma"]][:2]
   if key not in names:
     assert prefixFrequency[key] < 50, key
     return "Other_"+key
   else:
      return names[key]

def getSurprisalRepresentation(lemma):
   if "ROOT" in lemma[header["lemma"]]:
      return lemma[header["lemma"]]
   else:
      return names.get(lemma[header["lemma"]][:2], "<OOV>")+"@"+lemma[header["lemma"]]


from math import log, exp
from random import random, shuffle, randint, Random, choice




vocab_lemmas = {}

pairs = set()
counter = 0
Random(0).shuffle(words)
data_train = words[int(0.05*len(words)):]
data_dev = words[:int(0.05*len(words))]


#data = words

                                                                         
names = {'ng' : "Negation", 'om' : "Object/reflexive", 'sm' : "Subject", 'sr' : "Subject", 't^' : "Tense/aspect", 'ap' : "Valence", 'c' : "Valence", 'nt' : "Valence", 'rv' : "Derivation", 'rc' : "Valence", 'p' : "Voice", 'm^' : "Mood", 'wh' : "Int/Rel", 'rl' : "Int/Rel", "cl" : "Valence", "lc" : "Other_locative", "ps" : "Other_possessive", "mi" : "Other_mi", "cp" : "Other_copula", "pf" : "Other_perfective", "if" : "Infinitive", "rf" : "Object/reflexive"}

#defaultdict(<class 'int'>, {'SUBJ': 34567, 'Tense/aspect': 16019, 'Object': 7985, 'Subject': 738, 'Infinitive': 1018, 'rf': 768, '17': 32, 'Int/Rel': 212, 'Negation': 482, 'Valence': 1, 'Mood': 5, 'Other_copula': 36, '7': 5, 'wo': 16, 'di': 8, 'ij': 4, '9': 19, 'av': 11, '5': 11, 'lo': 5, '8': 1, '2a': 49, 'a.': 32, 'f^': 1, 'Other_locative': 3, '6': 7, '1s': 3, 'ht': 3, '10': 16, 'fi': 1, '1': 3, '3': 2, 'pr': 3, 'Other_possessive': 1, '2s': 1, '2': 10, 'pn': 1, '..': 1, 'wa': 1, '14': 1, 'st': 1, 'ei': 1, '9a': 1, 'cj': 1})

#{'..': 0, '1': 2, '2': 4, 'Object': 6, 'if': 8, 'Mood': 10, '2a': 12, 'cj': 14, 'f^': 16, 'Negation': 18, '7': 20, 'Int/Rel': 22, '9a': 24, '3': 26, 'st': 28, 'Other_locative': 30, 'av': 32, '1s': 34, '10': 36, '8': 38, 'lo': 40, '2s': 42, 'wa': 44, 'ht': 46, 'Subject': 48, '17': 50, 'Other_copula': 52, 'SUBJ': 54, 'Other_possessive': 56, 'rf': 58, 'ei': 60, 'di': 62, 'pn': 64, 'ij': 66, 'Tense/aspect': 68, '9': 70, 'fi': 72, 'a.': 74, '14': 76, 'Valence': 78, 'pr': 80, '6': 82, '5': 84, 'wo': 86}



#quit()
import torch.nn as nn
import torch
from torch.autograd import Variable


import numpy.random



import torch.cuda
import torch.nn.functional


from collections import defaultdict

dataChosen_train = []
dataChosen_dev = []
for data_, dataChosen in [(data_train, dataChosen_train), (data_dev, dataChosen_dev)]:
  for verbWithAff in data_:
    prefixesResult = []
    for x in verbWithAff:
      if x[header["type1"]] == "pfx":
         segmented = getSegmentedForms(x)
         if segmented is None:
           prefixesResult = None
           break
         prefixesResult += segmented
      else:
         prefixesResult.append(x)
    if prefixesResult is None: # remove this datapoint (affects <20 datapoints)
       continue
    dataChosen.append(prefixesResult)
 #   if "Tense/aspect" in slots and "Subject" in slots: # and slots.index("Tense/aspect") < slots.index("Subject"):
#       print(slots, prefixesResult)

   
data_train = dataChosen_train
data_dev = dataChosen_dev



prefixFrequency = defaultdict(int)
suffixFrequency = defaultdict(int)

words = set()

# For each verb form, select only the main verb form
for data_ in [data_train, data_dev]:
  for q in range(len(data_)):
     verb = data_[q]
  #   prefixes_keys = [getKey(x) for x in verb if x[header["type1"]] == "pfx"]
  
     segmentation = []
     for j in range(len(verb)):
        # subject prefix?
        if ".SBJ" in verb[j][header["analysis"]]:
           segmentation.append([])
           segmentation[-1].append(verb[j])
        else:
           if len(segmentation) == 0:
             segmentation.append([])
           segmentation[-1].append(verb[j])
     ###############################################################################   
     # Restrict to the last verb, chopping off initial auxiliaries and their affixes
     ###############################################################################
  
     verb = segmentation[-1]
  
     data_[q] = verb
     for word in verb:
       words.add(word[header["lemma"]])
     for affix in verb:
       affixLemma = getRepresentation(affix) #[header[RELEVANT_KEY]]
       if affix[header["type1"]] == "pfx":
          prefixFrequency[affixLemma] += 1
       elif affix[header["type1"]] == "sfx":
          suffixFrequency[affixLemma] += 1
 

words = list(words)
itos_words = ["PAD", "SOS", "EOS"] + words
stoi_words = dict(zip(itos_words, range(len(itos_words))))
print(stoi_words)









itos_pfx = sorted(list((prefixFrequency)))
stoi_pfx = dict(list(zip(itos_pfx, range(len(itos_pfx)))))

itos_sfx = sorted(list((suffixFrequency)))
stoi_sfx = dict(list(zip(itos_sfx, range(len(itos_sfx)))))

print(prefixFrequency)
print(suffixFrequency)

print(itos_pfx)
print(itos_sfx)

itos_pfx_ = itos_pfx[::]
shuffle(itos_pfx_)
weights_pfx = dict(list(zip(itos_pfx_, [2*x for x in range(len(itos_pfx_))])))

itos_sfx_ = itos_sfx[::]
shuffle(itos_sfx_)
weights_sfx = dict(list(zip(itos_sfx_, [2*x for x in range(len(itos_sfx_))])))








############################################################################################
############################################################################################


itos = itos_pfx
weights = weights_pfx
affixFrequencies = prefixFrequency  



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
else:
  weights = {}
  weights = {}
  files = args.model
  with open(files, "r") as inFile:
     next(inFile)
     for line in inFile:
        if "extract" in files:
           morpheme, weight, _ = line.strip().split("\t")
        else:
           morpheme, weight = line.strip().split(" ")
        weights[morpheme] = int(weight)

def calculateTradeoffForWeights(weights):
    # Order the datasets based on the given weights
    train = []
    dev = []
    # Iterate through the verb forms in the two data partitions, and linearize as a sequence of underlying morphemes
    for data, processed in [(data_train, train), (data_dev, dev)]:
      for verb in data:

         prefixes = [x for x in verb if x[header["type1"]] == "pfx"]
         suffixes = [x for x in verb if x[header["type1"]] == "sfx"]
         v = [x for x in verb if x[header["type1"]] == "v"]
         assert len(prefixes)+len(v)+len(suffixes)==len(verb)
 

         if args.model == "REAL": # Real ordering
            _ = 0
         elif args.model == "REVERSE": # Reverse prefixes
            prefixes = prefixes[::-1]
         else: # Order based on weights
            prefixes = sorted(prefixes, key=lambda x:weights.get(getRepresentation(x), 0))

#         print(v, header["lemma"])
         v[0][header["lemma"]] = "ROOT@"+v[0][header["lemma"]]
         ordered = prefixes + v + suffixes
 

         for ch in ordered:
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

