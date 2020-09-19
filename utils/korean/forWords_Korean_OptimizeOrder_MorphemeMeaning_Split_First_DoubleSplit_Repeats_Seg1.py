# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff
from frozendict import frozendict

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Korean-Kaist_2.6")
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

from korean_morpheme_meanings_michael import automatic_morpheme_meaning

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
             print("UNITE", lst)
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

corpusTrain = CorpusIterator_V(args.language,"train", storeMorph=True).iterator(rejectShortSentences = False)
corpusDev = CorpusIterator_V(args.language,"dev", storeMorph=True).iterator(rejectShortSentences = False)

pairs = set()
counter = 0
data_train = []
data_dev = []
import copy
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
#            print(line)
            processVerb(verb, data_)
            verb = []
            verb.append(line)
        else:
            # Reached end of verb
            processVerb(verb, data_)
            verb = []

words = []

affixFrequency = {}
for verbWithAff in data_train:
  for affix in verbWithAff[1:]:
    slot = affix["coarse"]
    affixFrequency[slot] = affixFrequency.get(slot, 0) + 1
    # affixFrequency[affixLemma] = affixFrequency.get(affixLemma, 0)+1


itos = set() # all the first elems of outputs of getrepresentation
for data_ in [data_train, data_dev]:
  for verbWithAff in data_:
    for affix in verbWithAff[1:]:
      slot = affix["coarse"]
      itos.add(slot) # getRepresentation[0]
itos = sorted(list(itos))
stoi = dict(list(zip(itos, range(len(itos)))))

itos_ = itos[::]
shuffle(itos_)
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # abstract slot


def calculateTradeoffForWeights(weights):
    # Order the datasets based on the given weights
    train = []
    dev = []
    for data, processed in [(data_train, train), (data_dev, dev)]:
      for verb in data:
         affixes = verb[1:]
         affixes = sorted(affixes, key=lambda x: weights[x["coarse"]]) # take the weight of the first morpheme slot
         for ch in [verb[0]] + affixes:
            processed.append(ch["fine"]) # grapheme morpheme, label_grapheme morpheme, don't call getRepresentation if abstract slot
         processed.append("EOS")
         for _ in range(args.cutoff+2):
           processed.append("PAD")
         processed.append("SOS")

    auc, devSurprisalTable = calculateMemorySurprisalTradeoff(train, dev, args)
    return auc, devSurprisalTable
   
lastCoordinate = None
mostCorrect = 1e100
import os
for iteration in range(1000):
  # Randomly select a morpheme whose position to update
  coordinate=choice(itos)

  # Stochastically filter out rare morphemes
  while (affixFrequency[coordinate] < 100 and random() < 0.95) or coordinate == lastCoordinate:
     coordinate = choice(itos)
  lastCoordinate = coordinate

  # This will store the minimal AOC found so far and the corresponding position
  mostCorrectValue = weights[coordinate]

  # Iterate over possible new positions
  for newValue in [-1] + [2*x+1 for x in range(len(itos))]:
     if random() < 0.3:
         continue
     print(newValue, "BestAUC:", mostCorrect, coordinate, affixFrequency[coordinate])
     # Updated weights, assuming the selected morpheme is moved to the position indicated by `newValue`.
     weights_ = {x : y if x != coordinate else newValue for x, y in weights.items()}

     # Calculate AOC for this updated assignment
     resultingAOC, _ = calculateTradeoffForWeights(weights_)
     print("Found", resultingAOC)
     # Update variables if AOC is smaller than minimum AOC found so far
     if resultingAOC < mostCorrect:
        mostCorrectValue = newValue
        mostCorrect = resultingAOC
  print(iteration, mostCorrect)
  weights[coordinate] = mostCorrectValue
  itos_ = sorted(itos, key=lambda x:weights[x])
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
  print(weights)
  for x in itos_:
     if affixFrequency[x] < 10:
       continue
     print("\t".join([str(y) for y in [x, weights[x], affixFrequency[x]]]))
  if (iteration + 1) % 50 == 0:
     _, surprisals = calculateTradeoffForWeights(weights_)

     if os.path.exists(TARGET_DIR):
      with open(TARGET_DIR+"/optimized_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
          print(iteration, mostCorrect, str(args), surprisals, file=outFile)
          for key in itos_:
            print(key, weights[key], file=outFile)
     else:
       os.makedirs(TARGET_DIR)
       with open(TARGET_DIR+"/optimized_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
          print(iteration, mostCorrect, str(args), surprisals, file=outFile)
          for key in itos_:
            print(key, weights[key], file=outFile)
  



