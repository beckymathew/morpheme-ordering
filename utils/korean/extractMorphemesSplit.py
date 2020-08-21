# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff

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
def getRepresentation(lemma):
    lst = lemma.split("_") # kaist_label, graph, kaist_label, graph, ...
    morpheme_slot = automatic_morpheme_meaning(grapheme=lst[1], label=lst[0]) 
    return morpheme_slot

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
          data_.append(lst)

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
        elif line["posFine"].split("+")[-1] == "etm":
            # The existing verb is in adnominal form, so we won't consider it
            verb = []
        elif line["posFine"].split("+")[-1] == "etn":
            # The existing verb is nominalized, so we won't consider it
            verb = []
        elif "px" in line["posFine"].split("+"):
            if "pvg" in line["posFine"].split("+") or "paa" in line["posFine"].split("+"):
              # general verb or adjective is part of new verb
              processVerb(verb, data_)
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
                processVerb(verb, data_)
                verb = []
              else: # starts w px and is a new verb
                processVerb(verb, data_)
                verb = []
                verb.append(copied)
        elif line["posUni"] == "VERB":
            # Clear existing verb if you see a new verb
            processVerb(verb, data_)
            verb = []
            if not line["posFine"].split("+")[-1] in ["etm", "etn"]:
                # only use the new verb if it isn't adnominalized or nominalized
                verb.append(line)
        elif line["posUni"] == "AUX" and len(verb) > 0:
            # Auxiliary is new verb
            processVerb(verb, data_)
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
            processVerb(verb, data_)
            verb = []
            verb.append(line)
        elif line["posUni"] == "SCONJ" and "xsv" in line["posFine"].split("+"):
            # Subordinating conjunction is a new verb if it has xsv (verb derivational suffix)
            processVerb(verb, data_)
            verb = []
            verb.append(line)
        elif line["posUni"] == "SCONJ" and len(verb) > 0:
            # Add subordinating conjunction to existing verb
            verb.append(line)
        elif "있" in line["word"] or "없" in line["word"]:
            # These are bound roots that mean "to have" or "to not have"
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
    affixLemma = getRepresentation(affix)
    for slot in affixLemma: 
      affixFrequency[slot] = affixFrequency.get(slot, 0) + 1
    # affixFrequency[affixLemma] = affixFrequency.get(affixLemma, 0)+1

from collections import defaultdict
counts = defaultdict(int) # all the first elems of outputs of getrepresentation
for data_ in [data_train, data_dev]:
  for verbWithAff in data_:
    for affix in verbWithAff[1:]:
      counts[((affix, "+".join(getRepresentation(affix))))]+=1
itos_keys = sorted(list(counts))

with open("../michael_scratch/output/matchedAllomorphs.tsv", "r") as inFile:
    data = [x.split("\t") for x in inFile.read().split("\n")]
data = dict([(x[1]+"_"+x[0], "\t".join(x[2:])) for x in data if len(x) > 2])


allMorphemes = defaultdict(int)

for x in itos_keys:
#    if counts[x] == 1: # no need to care aboit hapaxes for now
 #       continue
  #  if not ( "_" not in x[1] or "?" in x[1]):
   #     continue
    print(x[0], "\t", x[1], "\t", counts[x], data.get(x[0], ""))
    for k in x[1].split("+"):
        allMorphemes[k] += counts[x]
for x in sorted(list(allMorphemes)):
    print(x,"\t", allMorphemes[x])
