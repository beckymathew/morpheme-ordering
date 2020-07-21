# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Korean_2.6")
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
from korean_morpheme_meanings import morpheme_meaning, automatic_morpheme_meaning
# using label_grapheme version bc it's easier to see if the verb processing is correct
def processVerb(verb):
    if len(verb) > 0:
      # get flattened list of labels + morphemes
      flattened = []
      for group in verb:
         for morpheme in zip(group["posFine"].split("+"), group["lemma"].split("+")):
           morph, fine_label = allomorphy.get_underlying_morph(morpheme[1], morpheme[0])
           morpheme_slot = automatic_morpheme_meaning(grapheme=morph, label=fine_label) 
           for slot in morpheme_slot: 
             if not slot == "UNKNOWN":
               flattened.append({"SLOT": slot, "MORPHEME": morpheme})
          #  if not morpheme_slot == "UNKNOWN":
          #      flattened.append({"SLOT" : morpheme_slot, "MORPHEME" : morpheme})

      joined_nouns = []
      # join consecutive nouns (excluding verbal like nbn non-unit bound noun)
      # consecutive nouns are usually a form of compounding
      for item in flattened: 
        if item["SLOT"][0] == "n" and not item["SLOT"][:3] == "nbn":
          if len(joined_nouns) > 0:
            if joined_nouns[-1][0] == "n" and not joined_nouns[-1][:3] == "nbn":
              joined_nouns[-1] += "_" + item 
        else:
          joined_nouns.append(item)

      # split on nonconsecutive nouns
      start = 0
      lsts = []
      for i, item in enumerate(joined_nouns):
        if item["SLOT"][0] == "n" and not item["SLOT"][:3] == "nbn":
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
        elif line["posUni"] == "VERB":
            # Clear existing verb if you see a new verb
            processVerb(verb)
            verb = []
            if not line["posFine"].split("+")[-1] in ["etm", "etn"]:
                # only use the new verb if it isn't adnominalized or nominalized
                verb.append(line)
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
            idx = 0
            for pos in posfine:
              if pos == "px":
                break
              idx += 1
            before = copy.copy(line)
            after = copy.copy(line)
            before_posfine = "+".join(posfine[:idx])
            after_posfine = "+".join(posfine[idx:])
            if before_posfine:
             before["posFine"] = "+".join(posfine[:idx])
             before["lemma"] = "+".join(lemma[:idx])
             verb.append(before)
             processVerb(verb)
             verb = []
            if after_posfine:
              after["posFine"] = "+".join(posfine[idx:])
              after["lemma"] = "+".join(lemma[idx:])
              processVerb(verb)
              verb = []
              verb.append(after) 
            continue
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
        affixFrequencies[affix["SLOT"]] = affixFrequencies.get(affix["SLOT"], 0) + 1

itos = set() # set of affixes
for verbWithAff in data:
  for affix in verbWithAff[1:]:
        itos.add(affix["SLOT"])
itos = sorted(list(itos)) # sorted list of verb affixes
stoi = dict(list(zip(itos, range(len(itos))))) # assigning each affix and ID

itos_ = itos[::]
shuffle(itos_)
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # TODO: why?? mhahn: this amounts to a random assignment from affixes to even integers

print(weights)

# with open("output/extracted_Korean_2.6_forWords_Korean_ExtractOrder_MorphemeMeanings_WithoutAdnominals_UnknownDiscard.py_4821478.tsv", "r") as outFile:
with open("output/extracted_Korean_forWords_Korean_ExtractOrder_MorphemeMeanings_WithoutAdnominals_UnknownDiscard_Repeats.py_5102554.tsv", "r") as outFile:
  for x in outFile:
      x = x.strip().split("\t")
      print(x)
      assert x[0] in weights, x
      weights[x[0]] = int(x[1])
print(weights)

from collections import defaultdict
affixChains = defaultdict(int)
fromAffixChainsToMorphemeSeqs = defaultdict(list)
for d in data:
   affixChain = tuple([x["SLOT"] for x in d[1:]])
   affixChains[affixChain] += 1
   fromAffixChainsToMorphemeSeqs[affixChain].append(d)

freqs = {k: v for k, v in sorted(affixFrequencies.items(), key=lambda item: item[1])}

from collections import defaultdict
errors = defaultdict(int)
correct_connectors = []

def getCorrectOrderCountPerMorpheme(weights, coordinate, newValue):
   correct = 0
   incorrect = 0
#   print(data[:10])
   for affixChain, count in affixChains.items():
#      print(affixChain, count)
      vb = affixChain
#      print(vb)
      foundError=False
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
             if not vb[i] in seen: 
              if weightI > weightJ: # allow for repeated slots
                if "CONNECTOR" in vb:
                  correct_connectors.append(fromAffixChainsToMorphemeSeqs[vb])
                correct+=count
              else:
                incorrect+=count
                foundError=True
         seen.append(vb[i])
      if foundError:
          errors[vb] += 1
   return correct/(correct+incorrect)
getCorrectOrderCountPerMorpheme(weights, None, None)
errors = sorted(list(errors.items()), key=lambda x:x[1])
with open("output/errors_becky_repeats_3.txt", "w") as outFile:
  for error, count in errors:
      print("====", file=outFile)
      print("ERROR: Incompatible Suffix Chain: ", error, file=outFile)
      print("Occurrences: ", count, file=outFile)
      print("Relevant Examples:", file=outFile)
      for x in fromAffixChainsToMorphemeSeqs[error]:
          print(x, file=outFile)
  #print(errors)

with open("output/correct_connectors.txt", "w") as fout:
  for line in correct_connectors:
    for x in line:
      print(x, file=fout)