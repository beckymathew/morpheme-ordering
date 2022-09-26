#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Estimate memory-surprisal tradeoff 

import random
import sys
from estimateTradeoffHeldout_Pairs import calculateMemorySurprisalTradeoff
from math import log, exp, sqrt



objectiveName = "LM"


class Arguments:
    pass
args = Arguments()

# Adapt as needed
# May be REAL, RANDOM, REVERSE, TOTALLY_RANDOM (see explanation below), or a pointer to a file containing an ordering grammar.
args.model = "REAL"

# parameters for n-gram smoothing. See also estimateTradeoffHeldout_Pairs.py. If tuning these, I'd recommend tuning them for held-out surprisal of counterfactual orderings (not the real ones -- that would be unfair)
args.alpha=1.0
args.gamma=1
args.delta=1.0
args.cutoff=12

args.affixesUnderConsideration = "prefixes" # should be "prefixes" or "suffixes"

print(args)


assert args.alpha >= 0
assert args.alpha <= 1
assert args.delta >= 0
assert args.gamma >= 1

randomState = random.Random(10)




# These three functions take the representation of a morpheme (e.g., a tuple ``(underlying form, slot, maybe some other info)''), and extracts information that should enter averaging of MI, parameterization of counterfactual (e.g., optimized) orderings, and computation of surprisal.

# Besides a morpheme representation, the first and third of the functions also need to the deal with the input "EOS" (end of word), "SOS" (start of word), "PAD" (padding sequence in between adjacent words), in which case they should just return those.

# This is what I referred to as 'makeCoarse' in our meeting. It could be the underlying form or the distance from the root for an affix, and "ROOT" for the root.
def extractRepresentationForAveragingMI(morpheme):
   if morpheme in ["EOS", "SOS", "PAD"]:
     return morpheme
   else:
     return ..............

# This is for parameterizing counterfactual orderings that use orderings by slots (currently not necessary, in the absence of slot annotation). It is assumed that it returns "ROOT" for the root. For the affixes, it should return some kind of identifier for the slot (e.g., an integer or "VALENCE")
def extractRepresentationForOrdering(morpheme):
   return ...............

# This is the form that should enter surprisal calculation; it is most likely the underlying form, both for affixes and the root. It's important that this is always a string.
def getSurprisalRepresentation(morpheme):
   if morpheme in ["EOS", "SOS", "PAD"]:
     return morpheme
   else:
     return ..............




# Load both training (for fitting n-gram model) and held-out dev (for evaluating cross-entropy) data
data_train = ............
data_heldout = .............


# shuffle the two datasets to avoid any ordering artifacts, as we discussed
randomState.shuffle(data_train)
randomState.shuffle(data_heldout)

words = []

# Collect slots into itos ('integer to string') and stoi ('string to integer').
itos = set() # set of affixes
for data_ in [data_train, data_heldout]:
  for verbWithAff in data_:
    for affix in verbWithAff[1:]:
      itos.add(extractRepresentationForOrdering(affix))
itos = sorted(list(itos)) # sorted list of verb affixes
stoi = dict(list(zip(itos, range(len(itos))))) # assigning each affix and ID

itos_ = itos[::]
randomState.shuffle(itos_)
if args.model == "RANDOM": # Construct a random ordering of the morpheme slots
  weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))])))
elif args.model in ["REAL", "REVERSE"]: # Measure tradeoff for real or reverse ordering of affixes.
  weights = None
elif args.model in ["TOTALLY_RANDOM"]: # Totally random ordering within each word, without regard for any morpheme slots (not in the Open Mind paper, but could be interesting to look into in the absence of annotated slot information)
  weights = None
elif args.model == "UNIV": # a random ordering of the morpheme slots that respects the universals, as described in the Open Mind paper
  import compatible
  weights = compatible.sampleCompatibleOrdering(itos_)
  print(weights)
elif args.model != "REAL": # Load the ordering of slots from a file
  weights = {}
  import glob
  files = glob.glob(args.model)
  assert len(files) == 1
  with open(files[0], "r") as inFile:
     next(inFile)
     for line in inFile:
        morpheme, weight = line.strip().split(" ")
        weights[morpheme] = int(weight)

def calculateTradeoffForWeights(weights):
    # Order the datasets based on the given weights (if present, else do REAL or REVERSE ordering)
    train = []
    heldout = []
    if args.model == "TOTALLY_RANDOM":
      randomStateForTotallyRandomOrdering = random.Random(10)
    # Iterate through the verb forms in the two data partitions, and linearize as a sequence of underlying morphemes
    for data, processed in [(data_train, train), (data_heldout, heldout)]:
      for verb in data:

         positionOfRoot = [extractRepresentationForOrdering(x) for x in verb].index("ROOT")
         root = verb[positionOfRoot]

         if args.affixesUnderConsideration == "prefixes":
            affixes = verb[:positionOfRoot]
         else:
            affixes = verb[positionOfRoot+1:]

         if args.model == "REAL": # Real ordering
            pass
         elif args.model == "REVERSE": # Reverse affixes
            affixes = affixes[::-1]
         elif args.model == "TOTALLY_RANDOM":
            randomStateForTotallyRandomOrdering.shuffle(affixes)
         else: # Counterfactual (e.g., optimized or random ordering)
            affixes = sorted([weights[extractRepresentationForOrdering[x]] for x in affixes])

         if args.affixesUnderConsideration == "prefixes":
            processed = affixes + [root]
         else:
            processed = [root] + affixes 
        
         
         processed.append("EOS") # Indicate end-of-sequence
         for _ in range(args.cutoff+2): # Interpose a padding symbol between each pair of successive verb forms. There is no relation between successive verb forms, and adding padding prevents the n-gram models from "trying to learn" any spurious relations between successive verb forms.
           processed.append("PAD")
         processed.append("SOS") # start-of-sequence for the next verb form
    
    # Calculate AUC and the surprisals over distances (see estimateTradeoffHeldout.py for further documentation)
    auc, heldoutSurprisalTable, pmis = calculateMemorySurprisalTradeoff(train, heldout, args, getSurprisalRepresentation, extractRepresentationForAveragingMI)
    return pmis
   
auc, heldoutSurprisalTable, pmis = calculateTradeoffForWeights(weights)

# Write the PMIs to a file
with open(f"cond_mi_bySlot/{__file__}_{args.language}_{args.model.split('_')[-1]}", "w") as outFile:
 for x1, x2 in sorted(list(pmis)):
   if "PAD" in [x1, x2]:
     continue
   if "SOS" in [x1, x2]:
     continue
   if "EOS" in [x1, x2]:
     continue
   if len(pmis_coarse[(x1,x2)]) == 1:
     continue
   print("\t".join([str(q) for q in [x2, x1, len(pmis_coarse[(x1,x2)]), mean(pmis_coarse[(x1,x2)]), sd(pmis_coarse[(x1,x2)])]]), file=outFile) 

