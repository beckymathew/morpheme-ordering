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

import allomorphy
from korean_morpheme_meanings import morpheme_meaning
# using label_grapheme version bc it's easier to see if the verb processing is correct
def processVerb(verb):
    if len(verb) > 0:
      # get flattened list of labels + morphemes
      flattened = []
      for group in verb:
         for morpheme in zip(group["posFine"].split("+"), group["lemma"].split("+")):
           morph, fine_label = allomorphy.get_underlying_morph(morpheme[1], morpheme[0])
           morpheme_slot = morpheme_meaning(grapheme=morph, label=fine_label) 
           flattened.append(morpheme_slot)
           
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
              # general verb or adjective is part of new verb
              processVerb(verb)
              verb = []
            posfine = line["posFine"].split("+")
            lemma = line["lemma"].split("+")

            posfine_lsts = [x.split("+") for x in line["posFine"].split("px")] # make list of lists, split on px
            
            for lst in posfine_lsts:
              if lst[0] == "":
                lst.insert(0, "px") # splitting deleted px, bring it back

              while "" in lst: # removing some artefacts of splitting and joining
                lst.remove("")

            while ["px"] in posfine_lsts: # removing lists that were originally empty
              posfine_lsts.remove(["px"])

            lemma_lsts = [] 
            idx = 0
            for lst in posfine_lsts: # find corresponding lemmas of posfine lsts
              lemma_lsts.append(lemma[idx:idx + len(lst)])
              idx += len(lst)

            for i in range(len(posfine_lsts)):
              copied = copy.copy(line)
              copied["posFine"] = "+".join(posfine_lsts[i])
              copied["lemma"] = "+".join(lemma_lsts[i])
              if i == 0 and "px" not in posfine_lsts[i]: # still part of previous verb
                verb.append(copied)
                processVerb(verb)
                verb = []
              else: # starts w px and is a new verb
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

# for sentence in corpusTrain:
#     verb = []
#     for line in sentence:
#        if line["posUni"] == "PUNCT":
#           processVerb(verb)
#           verb = []
#           continue
#        elif line["posUni"] == "VERB":
#           processVerb(verb)
#           verb = []
#           verb.append(line)
#        elif line["posUni"] == "AUX" and len(verb) > 0:
#           verb.append(line)
#        elif line["posUni"] == "SCONJ" and line["word"] == 'て':
#           verb.append(line)
#           processVerb(verb)
#           verb = []
#        else:
#           processVerb(verb)
#           verb = []


### look at all Korean words instead of just verbs ###
# data = []
# for sentence in corpusTrain:
#     for line in sentence:
#         # print(line)
#         if not line["posUni"] == "PUNCT":
#             data.append([line["lemma"]])


# print(len(data))
# with open('labeled_verbs_without_adnominals.txt', 'w') as fout:
#     for item in data:
#         fout.write("%s\n" % item)
# quit()

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

# bar_num_morphs(data)
words = []

### splitting lemmas into morphemes -- each affix is a morpheme ###
affixFrequencies = {}
for verbWithAff in data:
  for affix in verbWithAff[1:]: # TODO: why does this start at 1? mhahn: in Japanese, this is to only conider suffixes, not the stem. Should probably be changed for Korean.
        affixFrequencies[affix] = affixFrequencies.get(affix, 0) + 1

itos = set() # set of affixes
for verbWithAff in data:
  for affix in verbWithAff[1:]:
        itos.add(affix)
itos = sorted(list(itos)) # sorted list of verb affixes
stoi = dict(list(zip(itos, range(len(itos))))) # assigning each affix and ID

itos_ = itos[::]
shuffle(itos_)
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # TODO: why?? mhahn: this amounts to a random assignment from affixes to even integers

from collections import defaultdict
affixChains = defaultdict(int)
for d in data:
   affixChains[tuple(d[1:])] += 1

# freqs = {k: v for k, v in sorted(affixFrequencies.items(), key=lambda item: item[1])}
# with open("output/"+args.language+"_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
#   for x in freqs.keys():
#      print("\t".join([str(y) for y in [x, freqs[x]]]), file=outFile)

def getCorrectOrderCountPerMorpheme(weights, coordinate, newValue):
   correct = 0
   incorrect = 0
#   print(data[:10])
   for affixChain, count in affixChains.items():
#      print(affixChain, count)
      vb = affixChain
#      print(vb)
      
      seen = []
      for i in range(0, len(vb)):
         for j in range(0, i):
             if vb[i] == coordinate:
                weightI = newValue
             else:
                weightI = weights[getRepresentation(vb[i])]

             if vb[j] == coordinate:
                weightJ = newValue
             else:
                weightJ = weights[getRepresentation(vb[j])]
             if weightI > weightJ:
               correct+=count
             else:
               if not vb[i] in seen: # don't penalize for duplicated slots
                incorrect+=count
   return correct/(correct+incorrect)

lastMostCorrect = 0
for iteration in range(1000):

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
     if correctCount > mostCorrect:
        mostCorrectValue = newValue
        mostCorrect = correctCount
  print(iteration, mostCorrect)

  assert mostCorrect >= lastMostCorrect
  lastMostCorrect = mostCorrect

  weights[coordinate] = mostCorrectValue
  itos_ = sorted(itos, key=lambda x:weights[x])
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
  #assert getCorrectOrderCount(weights, None, None) == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))
  #assert mostCorrect == getCorrectOrderCount(weights, None, None), (mostCorrect, getCorrectOrderCount(weights, None, None))
  # for x in itos_:
  #  if affixFrequencies[x] >= 50:
  #    print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]))

#  print(weights)
with open("output/extracted_"+args.language+"_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
  for x in itos_:
  #   if affixFrequencies[x] < 10:
   #    continue
     print("\t".join([str(y) for y in [x, weights[x], affixFrequencies[x]]]), file=outFile)
