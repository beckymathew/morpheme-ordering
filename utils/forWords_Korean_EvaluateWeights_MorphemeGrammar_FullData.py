# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Japanese_2.4")
parser.add_argument("--model", dest="model", type=str)
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


from korean_romanization import romanize
def getRepresentation(lemma):
   label, grapheme = lemma.split("_")
   return romanize(grapheme)

from math import log, exp
from random import random, shuffle, randint, Random, choice

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]

from corpusIterator_V import CorpusIterator_V

originalDistanceWeights = {}

morphKeyValuePairs = set()

vocab_lemmas = {}

import allomorphy
def processVerb(verb):
    if len(verb) > 0:
      # get flattened list of labels + morphemes
      flattened = []
      for group in verb:
         for morpheme in zip(group["posFine"].split("+"), group["lemma"].split("+")):
           morph, fine_label = allomorphy.get_underlying_morph(morpheme[1], morpheme[0]) # check for allomorphs
           flattened.append(fine_label + "_" + morph)

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
          data.append(lst)

corpusTrain = CorpusIterator_V(args.language,"train", storeMorph=True).iterator(rejectShortSentences = False)
pairs = set()
counter = 0
data = []
import copy
for sentence in corpusTrain:
   verb = []
   for line in sentence:
      if line["posUni"] == "PUNCT":
         # Clear existing verb if you see punctuation
         processVerb(verb)
         verb = []
      elif line["posFine"].split("+")[-1] == "etm":
         # The existing verb is in adnominal form, so we won't consider it
         verb = []
      elif line["posFine"].split("+")[-1] == "etn":
         # The existing verb is nominalized, so we won't consider it
         verb = []
      elif "px" in line["posFine"].split("+"):
         if "pvg" in line["posFine"].split("+") or "paa" in line["posFine"].split("+"):
            processVerb(verb)
            verb = []
         posfine = line["posFine"].split("+")
         lemma = line["lemma"].split("+")

         posfine_lsts = [x.split("+") for x in line["posFine"].split("px")]
         
         for lst in posfine_lsts:
            if lst[0] == "":
               lst.insert(0, "px")

            while "" in lst: # removing some artefacts of splitting and joining
               lst.remove("")

         while ["px"] in posfine_lsts:
            posfine_lsts.remove(["px"])

         lemma_lsts = []
         idx = 0
         for lst in posfine_lsts:
            lemma_lsts.append(lemma[idx:idx + len(lst)])
            idx += len(lst)

         for i in range(len(posfine_lsts)):
            copied = copy.copy(line)
            copied["posFine"] = "+".join(posfine_lsts[i])
            copied["lemma"] = "+".join(lemma_lsts[i])
            if i == 0 and "px" not in posfine_lsts[i]:
               verb.append(copied)
               processVerb(verb)
               verb = []
            else:
               processVerb(verb)
               verb = []
               verb.append(copied)
      elif line["posUni"] == "VERB":
         # Clear existing verb if you see a new verb
         processVerb(verb)
         verb = []
         if not line["posFine"].split("+")[-1] in ["etm", "etn"]:
               # only use the new verb if it isn't adnominalized or nominalized
               verb.append(line)
      elif line["posUni"] == "AUX" and len(verb) > 0:
         # # Add auxiliary to existing verb
         # verb.append(line)
         # Auxiliary is new verb
         processVerb(verb)
         verb = []
         verb.append(line)
      elif line["posUni"] == "AUX" and len(verb) == 0 and ("px" in line["posFine"].split("+") or "pvg" in line["posFine"].split("+")):
         # Auxiliary is a verb if it has a px (auxiliary verb) or pvg (general verb)
         verb.append(line)
      elif line["word"] == "수" and len(verb) > 0:
         # Part of VERB + ㄹ/을 수 있다/없다 construction
         verb.append(line)
      elif line["posUni"] == "SCONJ" and ("pvg" in line["posFine"].split("+") or "paa" in line["posFine"].split("+")):
         # Subordinating conjunction is a new verb if it has pvg (general verb)
         processVerb(verb)
         verb = []
         verb.append(line)
         # TODO: can AUX appear after SCONJ in it?
      elif line["posUni"] == "SCONJ" and "xsv" in line["posFine"].split("+"):
         # Subordinating conjunction is a new verb if it has xsv (verb derivational suffix)
         processVerb(verb)
         verb = []
         verb.append(line)
      elif line["posUni"] == "SCONJ" and len(verb) > 0:
         # Add subordinating conjunction to existing verb
         verb.append(line)
      elif "있" in line["word"] or "없" in line["word"]:
         # These are bound roots that mean "to have" or "to not have"
         processVerb(verb)
         verb = []
         verb.append(line)
      else:
         # Reached end of verb
         processVerb(verb)
         verb = []

words = []


affixFrequencies = {}
for verbWithAff in data:
  for affix in verbWithAff[1:]:
    affixLemma = getRepresentation(affix)
    affixFrequencies[affixLemma] = affixFrequencies.get(affixLemma, 0) + 1
      

itos = set()
for verbWithAff in data:
  for affix in verbWithAff[1:]:
    affixLemma = getRepresentation(affix)
    itos.add(affixLemma)
itos = sorted(list(itos))
stoi = dict(list(zip(itos, range(len(itos)))))

itos_ = itos[::]
shuffle(itos_)
if args.model == "RANDOM":
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
   for verb in data:
      keyForThisVerb = " ".join([x for x in verb])
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


