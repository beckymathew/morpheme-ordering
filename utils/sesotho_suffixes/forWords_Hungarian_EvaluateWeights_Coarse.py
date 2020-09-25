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
parser.add_argument("--model", dest="model", type=str)
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
    elif word[header["analysis"]] == "REVERS.CAUS": # os (Doke and Mokofeng, section 345)
      _ = 0
    elif word[header["analysis"]] == "APPL.PRF": # ets (cf. Doke and Mokofeng, section 313?). Both APPL and PRF have relatively frequent suffix morphs of the form -ets- in the corpus.
      _ = 0
    elif word[header["analysis"]] == "PRF.CAUS": # dits. Also consider Doke and Mokofeng, section 369, rule 4.
      _ = 0
    elif word[header["analysis"]] == "DEP.PRF": #  e. DEP = participial mood (Doke and Mokofeng, section 431).
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
from random import random, shuffle, randint, Random, choice




vocab_lemmas = {}

pairs = set()
counter = 0
Random(0).shuffle(words)
data_train = words[int(0.05*len(words)):]
data_dev = words[:int(0.05*len(words))]


#data = words

                                                                         
names = {'ng' : "Negation", 'om' : "Object", 'sm' : "Subject", 'sr' : "Subject", 't^' : "Tense/aspect", 'ap' : "Valence", 'c' : "Valence", 'nt' : "Valence", 'rv' : "Derivation", 'rc' : "Valence", 'p' : "Voice", 'm^' : "Mood", 'wh' : "Int/Rel", 'rl' : "Int/Rel", "cl" : "Valence", "lc" : "Other_locative", "ps" : "Other_possessive", "mi" : "Other_mi", "cp" : "Other_copula", "pf" : "Other_perfective"}

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
         suffixesResult += segmented
      else:
         suffixesResult.append(x)
    if suffixesResult is None: # remove this datapoint (affects <20 datapoints)i
       continue
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


      prefixes = [x for x in verb if x[header["type1"]] == "pfx"]
      suffixes = [x for x in verb if x[header["type1"]] == "sfx"]
      v = [x for x in verb if x[header["type1"]] == "v"]
      assert len(prefixes)+len(v)+len(suffixes)==len(verb)
#      print(len(suffixes), suffixes )


      for i in range(1, len(suffixes)):
         for j in range(1, i):
             weightI = weights[getRepresentation(suffixes[i])]
             weightJ = weights[getRepresentation(suffixes[j])]
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
#               print("MISTAKE", suffixes[i]["lemma"], weights[getRepresentation(suffixes[i]["lemma"])], suffixes[j], weights[getRepresentation(suffixes[j]["lemma"])], [x["lemma"] for x in suffixes])
               errors[(getRepresentation(suffixes[j]), getRepresentation(suffixes[i]))] += 1
      if len(suffixes) > 2:
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
   print(correct, incorrect, len(data_train), correctFull, incorrectFull)
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


