# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from frozendict import frozendict

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Korean-Kaist_2.6")
parser.add_argument("--model", dest="model", type=str)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))



args=parser.parse_args()
print(args)







myID = args.idForProcess





from korean_morpheme_meanings_michael import automatic_morpheme_meaning

from math import log, exp
from random import random, shuffle, randint, Random, choice

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]

from corpusIterator_V import CorpusIterator_V

originalDistanceWeights = {}

morphKeyValuePairs = set()

vocab_lemmas = {}


def getRepresentation(lemma):
   return lemma["coarse"]

def getSurprisalRepresentation(lemma):
   return lemma["fine"]


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
    affix = getRepresentation(affix)
    affixFrequencies[affix] = affixFrequencies.get(affix, 0) + 1


itos = set()
for data_ in [data_train, data_dev]:
  for verbWithAff in data_:
    for affix in verbWithAff[1:]:
      itos.add(getRepresentation(affix))
itos = sorted(list(itos))
stoi = dict(list(zip(itos, range(len(itos)))))

itos_ = itos[::]
shuffle(itos_)
if args.model == "RANDOM": # Construct a random ordering of the morphemes
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
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

from collections import defaultdict

errors = defaultdict(int)

hasSeenType = set()

def getCorrectOrderCount(weights):
   correct = 0
   incorrect = 0
   correctFull = 0
   incorrectFull = 0

   correctTypes = 0
   incorrectTypes = 0
   correctFullTypes = 0
   incorrectFullTypes = 0
   for verb in data_train:
      keyForThisVerb = " ".join([getSurprisalRepresentation(x) for x in verb])
      hasSeenThisVerb = (keyForThisVerb in hasSeenType)
      hasMadeMistake = False
      for i in range(1, len(verb)):
         for j in range(1, i):
             weightI = weights[getRepresentation(verb[i])]
             weightJ = weights[getRepresentation(verb[j])]
             if weightI == weightJ:
                continue
             if weightI > weightJ:
               correct+=1
               if not hasSeenThisVerb:
                 correctTypes += 1
             else:
               incorrect+=1
               if not hasSeenThisVerb:
                 incorrectTypes += 1
               hasMadeMistake = True
#               print("MISTAKE", verb[i]["lemma"], weights[getRepresentation(verb[i]["lemma"])], verb[j], weights[getRepresentation(verb[j]["lemma"])], [x["lemma"] for x in verb])
               errors[(getRepresentation(verb[j]), getRepresentation(verb[i]))] += 1
      if len(verb) > 2:
        if not hasMadeMistake:
            correctFull += 1
            if not hasSeenThisVerb:
              correctFullTypes += 1
        else:
            incorrectFull += 1
            if not hasSeenThisVerb:
              incorrectFullTypes += 1
      if not hasSeenThisVerb:
        hasSeenType.add(keyForThisVerb)
   return correct/(correct+incorrect), correctFull/(correctFull+incorrectFull),correctTypes/(correctTypes+incorrectTypes), correctFullTypes/(correctFullTypes+incorrectFullTypes)

result = getCorrectOrderCount(weights)
print(errors)
print(result)

if args.model.endswith(".tsv"):
   model = args.model[args.model.rfind("_")+1:-4]   
else:
   model = args.model

with open("results/accuracy_"+__file__+"_"+str(myID)+"_"+model+".txt", "w") as outFile:
   print(result[0], file=outFile)
   print(result[1], file=outFile)
   print(result[2], file=outFile)
   print(result[3], file=outFile)
   errors = list(errors.items())
   errors.sort(key=lambda x:x[1], reverse=True)
   for x, y in errors:
      print(x[0], x[1], y, file=outFile)
print("ERRORS")
print(errors)
print(result)

print("results/accuracy_"+__file__+"_"+str(myID)+"_"+args.model+".txt")


