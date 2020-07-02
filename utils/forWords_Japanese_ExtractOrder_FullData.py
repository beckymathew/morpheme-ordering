# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Japanese_2.4")
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
   if lemma == "させる" or lemma == "せる":
     return "CAUSATIVE"
   elif lemma == "れる" or lemma == "られる" or lemma == "える" or lemma == "得る" or lemma == "ける":
     return "PASSIVE_POTENTIAL"
   else:
     return lemma


from math import log, exp
from random import random, shuffle, randint, Random, choice

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]

from corpusIterator_V import CorpusIterator_V

originalDistanceWeights = {}

morphKeyValuePairs = set()

vocab_lemmas = {}


def processVerb(verb):
    if len(verb) > 0:
      if "VERB" in [x["posUni"] for x in verb[1:]]:
        print([x["word"] for x in verb])
      data.append([x["lemma"] for x in verb])

corpusTrain = CorpusIterator_V(args.language,"train", storeMorph=True).iterator(rejectShortSentences = False)
pairs = set()
counter = 0
data = []
for sentence in corpusTrain:
    verb = []
    for line in sentence:
       if line["posUni"] == "PUNCT":
          processVerb(verb)
          verb = []
          continue
       elif line["posUni"] == "VERB":
          processVerb(verb)
          verb = []
          verb.append(line)
       elif line["posUni"] == "AUX" and len(verb) > 0:
          verb.append(line)
       elif line["posUni"] == "SCONJ" and line["word"] == 'て':
          verb.append(line)
          processVerb(verb)
          verb = []
       else:
          processVerb(verb)
          verb = []


### look at all Korean words instead of just verbs ###
# data = []
# for sentence in corpusTrain:
#     for line in sentence:
#         # print(line)
#         if not line["posUni"] == "PUNCT":
#             data.append([line["lemma"]])


print(len(data))
# #quit()
# print(counter)
# #print(data)
# print(len(data))

from collections import Counter
import matplotlib.pyplot as plt

def bar_num_morphs(data):
    """
    Produces a bar chart of the number of morphemes in the word list.

    Params:
     - data: A list of lists of verbs, where each inner list item is a lemma that has morphemes delimited by "+"

    Returns:
     - nothing, creates a PNG of a bar chart of the distribution of number of morphemes
    """
    hist = Counter()
    wd_len = Counter()
    for wd_list in data:
        for wd in wd_list:
            morphs = wd.split("+")
            hist[len(morphs)] += 1
    plt.bar(hist.keys(), hist.values())
    plt.savefig("kor_num_morphs_all.png")

bar_num_morphs(data)

import torch.nn as nn
import torch
from torch.autograd import Variable
import numpy.random
import torch.cuda
import torch.nn.functional

words = []

### splitting verbs into lemmas -- each affix is a lemma ###
# affixFrequencies = {}
# for verbWithAff in data:
#   for affix in verbWithAff[1:]: # TODO: why does this start at 1?
#     affixLemma = getRepresentation(affix)
#     affixFrequencies[affixLemma] = affixFrequencies.get(affixLemma, 0)+1
#
# itos = set() # set of affixes
# for verbWithAff in data:
#   for affix in verbWithAff[1:]:
#     affixLemma = getRepresentation(affix)
#     itos.add(affixLemma)

### splitting lemmas into morphemes -- each affix is a morpheme ###
affixFrequencies = {}
for verbWithAff in data:
  for affix in verbWithAff[1:]: # TODO: why does this start at 1? mhahn: this is to only conider suffixes, not the stem.
    morphs = affix.split("+")
    for morph in morphs:
        affixFrequencies[morph] = affixFrequencies.get(morph, 0) + 1

itos = set() # set of affixes
for verbWithAff in data:
  for affix in verbWithAff[1:]:
    morphs = affix.split("+")
    for morph in morphs:
        itos.add(morph)
itos = sorted(list(itos)) # sorted list of verb affixes
stoi = dict(list(zip(itos, range(len(itos))))) # assigning each affix and ID

# print(itos)
# print(stoi)

itos_ = itos[::]
shuffle(itos_)
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # TODO: why?? mhahn: this amounts to a random assignment from affixes to even integers

# def getCorrectOrderCount(weights, coordinate, newValue):
#    correct = 0
#    incorrect = 0
#    for verb in data:
#       for i in range(1, len(verb)):
#          for j in range(1, i):
#              if verb[i] == coordinate:
#                  weightI = newValue
#              else:
#                 weightI = weights[getRepresentation(verb[i])]
#
#              if verb[j] == coordinate:
#                  weightJ = newValue
#              else:
#                 weightJ = weights[getRepresentation(verb[j])]
#              if weightI > weightJ:
#                correct+=1
#              else:
#                incorrect+=1
#    return correct/(correct+incorrect)

def getCorrectOrderCountPerMorpheme(weights, coordinate, newValue):
   correct = 0
   incorrect = 0
   for verb in data:
      vb = [] # create a flat list of morphemes in the verb
      for lemma in verb:
          vb.extend(lemma.split("+"))

      for i in range(len(verb[0]), len(vb)): # start after the first lemma
         for j in range(len(verb[0]), i):
             if vb[i] == coordinate:
                 weightI = newValue
             else:
                weightI = weights[getRepresentation(vb[i])]

             if vb[j] == coordinate:
                 weightJ = newValue
             else:
                weightJ = weights[getRepresentation(vb[j])]
             if weightI > weightJ:
               correct+=1
             else:
               incorrect+=1
   return correct/(correct+incorrect)

lastMostCorrect = 0
for iteration in range(200):
  coordinate = choice(itos)
  while random() < 0.8 and affixFrequencies[coordinate] < 50 and iteration < 100: # TODO: why? mhahn: this is to focus early iterations on frequent morphemes
     coordinate = choice(itos)

  mostCorrect, mostCorrectValue = 0, None
  for newValue in [-1] + [2*x+1 for x in range(len(itos))] + [weights[coordinate]]: # TODO: why is there -1 and +1 here? mhahn: this describes all ways of ordering the chosen morpheme between any two other morphemes
     if random() < 0.8 and newValue != weights[coordinate] and iteration < 50:
         continue
     weights_ = {x : y for x,y in weights.items()}
     weights_[coordinate] = newValue
     correctCount = getCorrectOrderCountPerMorpheme(weights_, None, None)
#     print(coordinate, newValue, iteration, correctCount)
     if correctCount > mostCorrect:
        mostCorrectValue = newValue
        mostCorrect = correctCount
  print(iteration, mostCorrect)

  assert mostCorrect >= lastMostCorrect
  lastMostCorrect = mostCorrect

  weights[coordinate] = mostCorrectValue
#  print(getCorrectOrderCount(weights, None, None) , mostCorrect)
 # assert getCorrectOrderCount(weights, None, None) == mostCorrect
  # TODO: shouldn't this only be done if the weights improved the correct score? mhahn: the score can never worsen, so this shouldn't be an issue.
  itos_ = sorted(itos, key=lambda x:weights[x])
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
  #assert getCorrectOrderCount(weights, None, None) == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))
  #assert mostCorrect == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))

#  print(weights)
 # for x in itos_:
  # if affixFrequencies[x] >= 50:
   #  print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]))
with open("output/extracted_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
  for x in itos_:
  #   if affixFrequencies[x] < 10:
   #    continue
     print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]), file=outFile)
