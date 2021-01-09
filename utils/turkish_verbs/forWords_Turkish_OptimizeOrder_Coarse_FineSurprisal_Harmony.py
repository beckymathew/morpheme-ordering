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


morphemesToPhonologicalForm = {}
with open("morphemes.txt", "r") as inFile:
   for line in inFile:
       if len(line) < 3:
           continue
       line = line.strip().split("\t")
       morphemesToPhonologicalForm[line[0]] = line[1]


myID = args.idForProcess


TARGET_DIR = "results/"+__file__.replace(".py", "")


vowels = "aeiouöüı"

def getVowelHarmonyForm(x):
 #   print(x)
    result = []
    lastVowel = None
    for i in range(len(x)):
        if i == 0:
            for c in  x[i]["fine"]:
                if c in vowels:
                    lastVowel = c
            result.append({"fine_vowels" : x[i]["fine"], "coarse" : x[i]["coarse"]})
        else:
            if x[i]["fine"] == "TAM1_AR":
               soFar = "".join([x["fine_vowels"] for x in result])
               if i == 1 and x[0]["fine"] in ["ol", "al", "gel", "ver", "gör", "bil", "kal", "bul", "dur", "san", "Ol", "var", "vur"]:
                   phon = "Ir"
               elif len([None for x in soFar if x in vowels]) <= 1:
                   phon = "Ar"
               else:
                   phon = "Ir"
            else: 
               phon = morphemesToPhonologicalForm[x[i]["fine"]]
#            print("phon", phon)
            surface = ""
            for c in phon:
                if c == "A":
                    if lastVowel in "aouı":
                       surface += "a"
                    else:
                       surface += "e"
                elif c == "I":
                    if lastVowel in "aı":
                       surface += "ı"
                    elif lastVowel in "ei":
                       surface += "i"
                    elif lastVowel in "ou":
                       surface += "u"
                    elif lastVowel in "öü":
                       surface += "ü"
                    else:
                        assert False, (c, phon, surface)
                else:
                    surface += c
                if surface[-1] in vowels:
                    lastVowel = surface[-1]
#            print(phon, "-->", surface)
            result.append({"fine_vowels" : surface, "coarse" : x[i]["coarse"]})
#    print(result)
    return result


posUni = set() 

posFine = set() 

def getRepresentation(lemma):
    return lemma["coarse"]

def getSurprisalRepresentation(lemma):
    return lemma["fine_vowels"]

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


def calculateTradeoffForWeights(weights):
    # Order the datasets based on the given weights
    train = []
    dev = []
    for data, processed in [(data_train, train), (data_dev, dev)]:
      for verb in data:
         affixes = verb[1:]
         affixes = sorted(affixes, key=lambda x:weights.get(getRepresentation(x), 0))
         for ch in getVowelHarmonyForm([verb[0]] + affixes):
            processed.append(getSurprisalRepresentation(ch))
         processed.append("EOS")
         for _ in range(args.cutoff+2):
           processed.append("PAD")
         processed.append("SOS")

    auc, devSurprisalTable = calculateMemorySurprisalTradeoff(train, dev, args)
    return auc, devSurprisalTable
   
mostCorrect = 1e100 
for iteration in range(1000):
  # Randomly select a morpheme whose position to update
  coordinate=choice(itos)

  # Stochastically filter out rare morphemes
  while affixFrequencies.get(coordinate, 0) < 10 and random() < 0.95:
     coordinate = choice(itos)

  # This will store the minimal AOC found so far and the corresponding position
  mostCorrectValue = weights[coordinate]

  # Iterate over possible new positions
  for newValue in [-1] + [2*x+1 for x in range(len(itos))]:

     # Stochastically exclude positions to save compute time
     if random() < 0.5:
        continue
     print(newValue, mostCorrect, coordinate, affixFrequencies.get(coordinate,0))
     # Updated weights, assuming the selected morpheme is moved to the position indicated by `newValue`.
     weights_ = {x : y if x != coordinate else newValue for x, y in weights.items()}

     # Calculate AOC for this updated assignment
     resultingAOC, _ = calculateTradeoffForWeights(weights_)

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
     if affixFrequencies.get(x,0) < 10:
       continue
     print("\t".join([str(y) for y in [x, weights[x], affixFrequencies.get(x,0)]]))
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
  



