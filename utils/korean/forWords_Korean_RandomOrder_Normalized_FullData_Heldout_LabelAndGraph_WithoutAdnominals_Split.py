# Estimate memory-surprisal tradeoff 

import random
import sys
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff
from math import log, exp
from corpusIterator_V import CorpusIterator_V
from random import shuffle, randint, Random, choice



objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default="Japanese-GSD_2.4")

# May be REAL, RANDOM, REVERSE, or a pointer to a file containing an ordering grammar.
parser.add_argument("--model", dest="model", type=str)

# parameters for n-gram smoothing. See also estimateTradeoffHeldout.py
parser.add_argument("--alpha", dest="alpha", type=float, default=1.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=12)

# An identifier for this run of this script.
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))



args=parser.parse_args()
print(args)


assert args.alpha >= 0
assert args.alpha <= 1
assert args.delta >= 0
assert args.gamma >= 1

myID = args.idForProcess


TARGET_DIR = "estimates/"

# Translate a verb into an underlying morpheme
def getRepresentation(lemma):
   if lemma == "させる" or lemma == "せる":
     return "CAUSATIVE"
   elif lemma == "れる" or lemma == "られる" or lemma == "える" or lemma == "得る" or lemma == "ける":
     return "PASSIVE_POTENTIAL"
   else:
     return lemma

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

# Load both training (for fitting n-gram model) and held-out dev (for evaluating cross-entropy) data
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
              processVerb(verb, data_)
              verb = []
            posfine = line["posFine"].split("+")
            lemma = line["lemma"].split("+")

            posfine_lsts = [x.split("+") for x in line["posFine"].split("px")]
            
            for lst in posfine_lsts:
              if lst[0] == "":
                lst.insert(0, "px")

              while "" in lst: # removing some artefacts of splitting and joining
                lst.remove("")

            while ["px"] in posfine_lsts:
              posfine_lsts.remove(["px"])

            lemma_lsts = []
            idx = 0
            for lst in posfine_lsts:
              lemma_lsts.append(lemma[idx:idx + len(lst)])
              idx += len(lst)

            for i in range(len(posfine_lsts)):
              copied = copy.copy(line)
              copied["posFine"] = "+".join(posfine_lsts[i])
              copied["lemma"] = "+".join(lemma_lsts[i])
              if i == 0 and "px" not in posfine_lsts[i]:
                verb.append(copied)
                processVerb(verb, data_)
                verb = []
              else:
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
            # # Add auxiliary to existing verb
            # verb.append(line)
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
            # TODO: can AUX appear after SCONJ in it?
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

# Collect morphemes into itos and stoi. These morphemes will be used to parameterize ordering (for Korean, we could use underlying morphemes or the coarse-grained labels provided in Kaist like ef, etm, etc.)
affixFrequency = {}
for verbWithAff in data_train:
  for affix in verbWithAff[1:]:
    affixFrequency[affix] = affixFrequency.get(affix, 0)+1


itos = set()
for verbWithAff in data_train:
  for affix in verbWithAff[1:]:
    itos.add(affix)
itos = sorted(list(itos))
stoi = dict(list(zip(itos, range(len(itos)))))

itos_ = itos[::]
shuffle(itos_)
if args.model == "RANDOM": # Construct a random ordering of the morphemes
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
elif args.model in ["REAL", "REVERSE"]: # Measure tradeoff for real or reverse ordering of suffixes.
  weights = None
elif args.model != "REAL": # Load the ordering from a file
  weights = {}
  import glob
  files = glob.glob(args.model)
  assert len(files) == 1
  assert "Normalized" in files[0]
  with open(files[0], "r") as inFile:
     next(inFile)
     for line in inFile:
        morpheme, weight = line.strip().split(" ")
        weights[morpheme] = int(weight)




def calculateTradeoffForWeights(weights):
    train = []
    dev = []
    # Iterate through the verb forms in the two data partitions, and linearize as a sequence of underlying morphemes
    for data, processed in [(data_train, train), (data_dev, dev)]:
      for verb in data:
         affixes = verb[1:]
         if args.model == "REAL": # Real ordering
            _ = 0
         elif args.model == "REVERSE": # Reverse affixs
            affixes = affixes[::-1]
         else: # Order based on weights
            affixes = sorted(affixes, key=lambda x:weights.get(x, 0))
         for ch in [verb[0]] + affixes: # Express as a sequence of underlying morphemes (could also instead be a sequence of phonemes if we can phonemize the Korean input)
            processed.append(getRepresentation(ch))
         processed.append("EOS") # Indicate end-of-sequence
         for _ in range(args.cutoff+2): # Interpose a padding symbol between each pair of successive verb forms. There is no relation between successive verb forms, and adding padding prevents the n-gram models from "trying to learn" any spurious relations between successive verb forms.
           processed.append("PAD")
         processed.append("SOS") # start-of-sequence for the next verb form
    
    # Calculate AUC and the surprisals over distances (see estimateTradeoffHeldout.py for further documentation)
    auc, devSurprisalTable = calculateMemorySurprisalTradeoff(train, dev, args)


    # Write results to a file
    model = args.model
    outpath = TARGET_DIR+args.language+"_"+__file__+"_model_"+str(myID)+"_"+model+".txt"
    print(outpath)
    with open(outpath, "w") as outFile:
       print(str(args), file=outFile)
       print(" ".join(map(str,devSurprisalTable)), file=outFile)
    return auc
   
auc = calculateTradeoffForWeights(weights)
print("AUC: ", auc)
