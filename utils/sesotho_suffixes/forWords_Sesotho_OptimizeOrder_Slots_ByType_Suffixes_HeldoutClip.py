# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from corpus import CORPUS
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff
from math import log, exp
from random import shuffle, randint, Random, choice



objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default=CORPUS)

# May be REAL, RANDOM, REVERSE, or a pointer to a file containing an ordering grammar.
parser.add_argument("--alpha", dest="alpha", type=float, default=1.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=4)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))



args=parser.parse_args()
print(args)


############################################################################################
############################################################################################


# for ordering
def getKey(word):
  return word[header["lemma"]][:2]

def getSegmentedFormsVerb(word):
   if "/" not in word[header["lemma"]] and "." not in word[header["lemma"]]:
     return [word]
   elif "/" in word[header["lemma"]]:
    lemmas = word[header["lemma"]].split("/")
    words = [word[::] for _ in lemmas]
    for i in range(len(lemmas)):
      words[i][0] = "_"
      words[i][1] = lemmas[i]
      words[i][3] = "v" if i == 0 else "sfx"      
#    print("SPLIT", words, word) # frequent: verb stem + past suffix merged
    return words
   else: # 
    print("TODO", word)
    assert False


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
    if lemmas[0] == "t^pf" and lemmas[1] == "m^in": # ~360 cases, mostly -e-. TODO think about the order of the morphemes in the allegedly merged morpheme.
      _ = 0
    elif word[header["analysis"]] == "REVERS.CAUS": # os (Doke and Mofokeng, section 345)
      _ = 0
    elif word[header["analysis"]] == "APPL.PRF": # ets (cf. Doke and Mofokeng, section 313?). Both APPL and PRF have relatively frequent suffix morphs of the form -ets- in the corpus.
      _ = 0
    elif word[header["analysis"]] == "PRF.CAUS": # dits. Also consider Doke and Mofokeng, section 369, rule 4.
      _ = 0
    elif word[header["analysis"]] == "DEP.PRF": #  e. DEP = participial mood (Doke and Mofokeng, section 431).
      _ = 0
    elif word[header["analysis"]] in ["PRF.PASS", "PRS.APPL", "cl.PRF", "IND.PRS", "PRF.REVERS", "NEG.PRF"]: # rare, together 10 data points
      _ = 0
    else:
#      print("SPLIT", word1, word2, word)
      pass
    return [word1, word2]
   else: # 
    print("TODO", word)
    assert word[1] == "m..." # occurs 1 time
    return None

def getNormalizedForm(word): # for prediction
#   print(word)
   return stoi_words[word[header["lemma"]]]

myID = args.idForProcess


TARGET_DIR = "results/"+__file__.replace(".py", "")

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



def getRepresentation(lemma):
   return names[lemma[header["lemma"]][:2]]

def getSurprisalRepresentation(lemma):
   return lemma[header["lemma"]]


from math import log, exp
from random import shuffle, randint, Random, choice




vocab_lemmas = {}

pairs = set()
counter = 0
Random(0).shuffle(words)
data_train = words[int(0.05*len(words)):]
data_dev = words[:int(0.05*len(words))]


#data = words

                                                                         
names = {'ng' : "Negation", 'om' : "Object", 'sm' : "Subject", 'sr' : "Subject", 't^' : "Tense/Aspect", 'ap' : "Valence", 'c' : "Valence", 'nt' : "Valence", 'rv' : "Derivation", 'rc' : "Valence", 'p' : "Voice", 'm^' : "Mood", 'wh' : "Interrogative", 'rl' : "Relative", "cl" : "Valence", "lc" : "Other_locative", "ps" : "Other_possessive", "mi" : "Other_mi", "cp" : "Other_copula", "pf" : "Other_perfective"}

def getSlot(x):
   if x == "sm":
      return "SUBJ"
   elif x in names:
      return names[x]
   else:
#     print(x)
     return x


#quit()
import torch.nn as nn
import torch
from torch.autograd import Variable


import numpy.random



import torch.cuda
import torch.nn.functional


from collections import defaultdict

prefixFrequency = defaultdict(int)
suffixFrequency = defaultdict(int)
dataChosen_train = []
dataChosen_dev = []
for data_, dataChosen in [(data_train, dataChosen_train), (data_dev, dataChosen_dev)]:
  for verbWithAff in data_:
    suffixesResult = []
    for x in verbWithAff:
      if x[header["type1"]] == "sfx":
         segmented = getSegmentedForms(x)
         if segmented is None:
           suffixesResult = None
           break
         suffixesResult += segmented
      elif x[header["type1"]] == "v":
         segmented = getSegmentedFormsVerb(x)
         for i, l in enumerate(segmented):
            l.append(f"SPLIT_{i}")
         suffixesResult += segmented
      else:
         suffixesResult.append(x)
    if suffixesResult is None: # remove this datapoint (affects <20 datapoints)
       continue
    if "wh" in [x[1] for x in suffixesResult]: # This is not a suffix, but a cliticized version of an independent word, according to Doke&Mofokeng.
#       print(suffixesResult)
       suffixesResult = [x for x in suffixesResult if x[1] != "wh"]
    splitTense = [i for i in suffixesResult if "sfx" in i and "SPLIT" in i[-1] and "t^" in i[1]] # It can happen that a tense suffix is marked as fused with the stem, but belongs further back as a morpheme.
    if len(splitTense) > 0 and len([x for x in suffixesResult if "sfx" in x]) > 2:
       j = suffixesResult.index(splitTense[0])
       nextMorpheme = suffixesResult[j+1]
       if nextMorpheme[1].startswith("m^"):
            pass
       else: #if nextMorpheme[1].startswith("p"): In almost all cases where this happens, the next morpheme is a passive suffix
         suffixesResult[j], suffixesResult[j+1] = suffixesResult[j+1], suffixesResult[j]
    tense = [i for i in range(len(suffixesResult)) if "sfx" in suffixesResult[i] and "t^" in suffixesResult[i][1]]
    voice = [i for i in range(len(suffixesResult)) if "sfx" in suffixesResult[i] and "p" in suffixesResult[i][1]]
    if len(tense) > 0 and len(voice) > 0:
       if tense[0] < voice[0]:
           print(suffixesResult)

    dataChosen.append(suffixesResult)
    for affix in suffixesResult:
      affixLemma = getSlot(getKey(affix)) #[header[RELEVANT_KEY]]
      if affix[header["type1"]] == "pfx":
         prefixFrequency[affixLemma] += 1
      elif affix[header["type1"]] == "sfx":
         suffixFrequency[affixLemma] += 1
data_train = dataChosen_train
data_dev = dataChosen_dev


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


itos = itos_sfx
weights = weights_sfx
affixFrequencies = suffixFrequency  



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
  
         suffixes.sort(key=lambda x:weights[getRepresentation(x)])
         ordered = prefixes + v + suffixes
 

         for ch in ordered:
            processed.append(getSurprisalRepresentation(ch))
         processed.append("EOS") # Indicate end-of-sequence
         for _ in range(args.cutoff+2): # Interpose a padding symbol between each pair of successive verb forms. There is no relation between successive verb forms, and adding padding prevents the n-gram models from "trying to learn" any spurious relations between successive verb forms.
           processed.append("PAD")
         processed.append("SOS") # start-of-sequence for the next verb form
    
    # Calculate AUC and the surprisals over distances (see estimateTradeoffHeldout.py for further documentation)
    auc, devSurprisalTable = calculateMemorySurprisalTradeoff(train, dev, args)
    return auc, devSurprisalTable
   

import os

mostCorrect = 1e100
for iteration in range(10000):
  # Randomly select a morpheme whose position to update
  coordinate=choice(itos)

  # Stochastically filter out rare morphemes
  while affixFrequencies.get(coordinate, 0) < 50 and iteration < 200:
     coordinate = choice(itos)
  while affixFrequencies.get(coordinate, 0) < 5:
     coordinate = choice(itos)

  mostCorrectCoordinate = weights[coordinate]

  # Iterate over possible new positions
  for newValue in [random.choice([-1] + [2*x+1 for x in range(len(itos))])]:

     print(newValue, mostCorrect, coordinate, affixFrequencies.get(coordinate,0))
     # Updated weights, assuming the selected morpheme is moved to the position indicated by `newValue`.
     weights_ = {x : y if x != coordinate else newValue for x, y in weights.items()}

     # Calculate AOC for this updated assignment
     resultingAOC, _ = calculateTradeoffForWeights(weights_)

     # Update variables if AOC is smaller than minimum AOC found so far
  if resultingAOC < mostCorrect:
     print("Accept", coordinate, newValue)
     weights[coordinate] = newValue
     mostCorrect = resultingAOC
  else:
     print("Reject")
  assert mostCorrect < 1e99
  print(iteration, mostCorrect)
  itos_ = sorted(itos, key=lambda x:weights[x])
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
  for x in itos_:
     if affixFrequencies.get(x,0) < 10:
       continue
     print("\t".join([str(y) for y in [x, weights[x], affixFrequencies.get(x,0)]]))
  if (iteration + 1) % 50 == 0:
     _, surprisals = calculateTradeoffForWeights(weights_)

     if os.path.exists(TARGET_DIR):
       pass
     else:
       os.makedirs(TARGET_DIR)
     with open(TARGET_DIR+"/optimized_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
        print(iteration, mostCorrect, str(args), surprisals, file=outFile)
        for key in itos_:
          print(key, weights[key], file=outFile)
  



