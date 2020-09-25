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
   key = lemma[header["lemma"]][:2]
   if key not in names:
     assert prefixFrequency[key] < 50, key
     return "Other_"+key
   else:
      return names[key]

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


print(weights)

print(prefixFrequency)
from collections import defaultdict

def getCorrectOrderCount(weights):
   correct = 0
   incorrect = 0
   errors = defaultdict(int)

   for vb in data_train:
      prefixes = [x for x in vb if x[header["type1"]] == "pfx"]
      suffixes = [x for x in vb if x[header["type1"]] == "sfx"]
      v = [x for x in vb if x[header["type1"]] == "v"]
      assert len(prefixes)+len(v)+len(suffixes)==len(vb)
  
      prefixes = [getRepresentation(x) for x in prefixes]
      for i in range(0, len(prefixes)):
         for j in range(0, i):
             weightI = weights[prefixes[i]]
             weightJ = weights[prefixes[j]]
  #           if SHOW:
   #              print(i, j, vb[i], vb[j], weightI, weightJ, weightI > weightJ)
             if weightI > weightJ:
               correct+=1
             elif prefixes[i] != prefixes[j]:
               errors[(prefixes[i], prefixes[j])] += 1
               incorrect+=1
#               if iteration > 15:
 #                  print(prefixes[i], prefixes[j], vb)      
   return correct/(correct+incorrect), errors

mostCorrect = 0
lastImprovement = -1
for iteration in range(1000):
  # Randomly select a morpheme whose position to update
  coordinate=choice(itos)

  # Stochastically filter out rare morphemes
  while (random() < 0.95 and affixFrequencies[coordinate] < 50 and iteration < 100) or affixFrequencies[coordinate] == 0: 
     coordinate = choice(itos)

  mostCorrectValue = weights[coordinate]

  # Iterate over possible new positions
  for newValue in [-1] + [2*x+1 for x in range(len(itos))]:
     if random() < 0.8 and newValue != weights[coordinate] and iteration < 50:
         continue
     weights_ = {x : y for x,y in weights.items()}
     weights_[coordinate] = newValue
     correctCount, errors = getCorrectOrderCount(weights_)
     if correctCount > mostCorrect:
        mostCorrectValue = newValue
        mostCorrect = correctCount
        lastImprovement = iteration
  print(iteration, mostCorrect, coordinate)
  if iteration - lastImprovement > 100:
     break

  weights[coordinate] = mostCorrectValue
 # assert getCorrectOrderCount(weights, None, None) == mostCorrect
  itos_ = sorted(itos, key=lambda x:weights[x])
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
  #assert getCorrectOrderCount(weights, None, None) == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))
  #assert mostCorrect == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))
  if iteration % 5 == 0:
     print(errors)
     for x in itos_:
      if affixFrequencies[x] >= 50:
        print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]))

with open("output/extracted_"+args.language+"_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
  for x in itos_:
     print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]), file=outFile)
