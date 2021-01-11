# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys

objectiveName = "LM"
from corpus import CORPUS
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default=CORPUS)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))
import random



args=parser.parse_args()
print(args)





myID = args.idForProcess







def getRepresentation(lemma):
    return lemma["coarse"]

def getSurprisalRepresentation(lemma):
    return lemma["fine"]

from math import log, exp
from random import random, shuffle, randint, Random, choice


from corpusIterator_V import CorpusIterator_V




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
          if 'VerbForm=Vnoun' in line["morph"]:
               continue
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
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # TODO: why?? mhahn: this amounts to a random assignment from affixes to even integers

from collections import defaultdict
affixChains = defaultdict(int)
for data_ in [data_train, data_dev]:
 for d in data_:
   affixChains[tuple(map(getRepresentation, d[1:]))] += 1

def getCorrectOrderCountPerMorpheme(weights):
   correct = 0.0
   incorrect = 0.0

   for affixChain, count in affixChains.items():
      vb = affixChain
      for i in range(0, len(vb)):
         for j in range(0, i):
             weightI = weights[vb[i]]
             weightJ = weights[vb[j]]
  #           if SHOW:
   #              print(i, j, vb[i], vb[j], weightI, weightJ, weightI > weightJ)
             if weightI > weightJ:
               correct+=count
             elif vb[i] != vb[j]:
               incorrect+=count
   return correct/(correct+incorrect)

mostCorrect = 0
for iteration in range(1000):
  # Randomly select a morpheme whose position to update
  coordinate=choice(itos)

  # Stochastically filter out rare morphemes
  while random() < 0.8 and affixFrequencies[coordinate] < 50 and iteration < 100: 
     coordinate = choice(itos)

  mostCorrectValue = weights[coordinate]

  # Iterate over possible new positions
  for newValue in [-1] + [2*x+1 for x in range(len(itos))]:
     if random() < 0.8 and newValue != weights[coordinate] and iteration < 50:
         continue
     weights_ = {x : y for x,y in weights.items()}
     weights_[coordinate] = newValue
     correctCount = getCorrectOrderCountPerMorpheme(weights_)
     if correctCount > mostCorrect:
        mostCorrectValue = newValue
        mostCorrect = correctCount
  print(iteration, mostCorrect)


  weights[coordinate] = mostCorrectValue
 # assert getCorrectOrderCount(weights, None, None) == mostCorrect
  itos_ = sorted(itos, key=lambda x:weights[x])
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
  #assert getCorrectOrderCount(weights, None, None) == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))
  #assert mostCorrect == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))
  if iteration % 100 == 0:
     for x in itos_:
      if affixFrequencies[x] >= 50:
        print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]))

with open("output/extracted_"+args.language+"_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
  for x in itos_:
     print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]), file=outFile)
