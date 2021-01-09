# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from frozendict import frozendict

objectiveName = "LM"
from corpus import CORPUS
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str, default=CORPUS)
parser.add_argument("--alpha", dest="alpha", type=float, default=0.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=15)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))
import random



args=parser.parse_args()
#print(args)


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


TARGET_DIR = "/u/scr/mhahn/deps/memory-need-ngrams-morphology/"



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
               phon = morphemesToPhonologicalForm.get(x[i]["fine"], x[i]["fine"].split("_")[-1])
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

# TODO: update this for Korean
def getRepresentation(lemma):
    return lemma["coarse"]

def getSurprisalRepresentation(lemma):
    return lemma["fine"]

from math import log, exp
from random import random, shuffle, randint, Random, choice

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]

from corpusIterator_V import CorpusIterator_V

originalDistanceWeights = {}

morphKeyValuePairs = set()

vocab_lemmas = {}

import turkish_segmenter
import turkish_segmenter as turkish_segmenter_coarse
def processVerb(verb, data_):
    # assumption that each verb is a single word
   for vb in verb:
      labels = vb["morph"]
      morphs = turkish_segmenter_coarse.get_abstract_morphemes(labels)
      fine = turkish_segmenter.get_abstract_morphemes(labels)
      morphs[0] = vb["lemma"] # replace "ROOT" w actual root
      fine[0] = vb["lemma"] # replace "ROOT" w actual root
      lst_dict = []
      for i in range(len(fine)):
        morph_dict = {"fine": fine[i], "coarse": morphs[i]}
        lst_dict.append(morph_dict)
      data_.append({"parsed" : lst_dict, "original" : verb})

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

# bar_num_morphs(data)
words = []

data = data_train+data_dev
#print(data[:5])
### splitting lemmas into morphemes -- each affix is a morpheme ###
affixFrequencies = {}
for verbWithAff in data:
  for affix in verbWithAff["parsed"][1:]: # TODO: why does this start at 1? mhahn: in Japanese, this is to only conider suffixes, not the stem. Should probably be changed for Korean.
        affixFrequencies[affix["coarse"]] = affixFrequencies.get(affix["coarse"], 0) + 1

itos = set() # set of affixes
for verbWithAff in data:
  for affix in verbWithAff["parsed"][1:]:
        itos.add(affix["coarse"])
itos = sorted(list(itos)) # sorted list of verb affixes
stoi = dict(list(zip(itos, range(len(itos))))) # assigning each affix and ID

itos_ = itos[::]
shuffle(itos_)
weights = dict(list(zip(itos_, [2*x for x in range(len(itos_))]))) # TODO: why?? mhahn: this amounts to a random assignment from affixes to even integers


def assimilation(x):
    x = x.replace("aa", "aya")
#    x = x.replace("ee", "e")
#    x = x.replace("ıı", "ı")
#    x = x.replace("uu", "i")
    x = x.replace("ki", "ği")
#    x = x.replace("eiy", "iy")
    x = x.replace("eiyordu", "iyordu")
    x = x.replace("aıyordu", "ıyordu")
    x = x.replace("aıyorum", "ıyorum")
    x = x.replace("duum", "dum")
    x = x.replace("diim", "dim")
    x = x.replace("düüm", "düm")
    x = x.replace("dıım", "dım")
    x = x.replace("iril", "il")
    x = x.replace("tisin", "tin")
    x = x.replace("dusun", "dun")
    x = x.replace("aıl", "an")
    x = x.replace("lılı", "lını")
    x = x.replace("tırıl", "tıl")
    x = x.replace("tiril", "til")
    x = x.replace("türül", "tül")
    x = x.replace("tiim", "tim")
    x = x.replace("eili", "eni")
    x = x.replace("eile", "ene")
    x = x.replace("yeer", "yer")
    x = x.replace("yee", "yiye")
    x = x.replace("liim", "liyim")
    x = x.replace("türür", "tür")
    x = x.replace("seim", "sem")
    x = x.replace("saım", "sam")
    x = x.replace("eiy", "iy")
    x = x.replace("meez", "mez")
    return x

from collections import defaultdict
affixChains = defaultdict(list)
for d in data:
   predicted = getVowelHarmonyForm(d["parsed"])
   d["original"][0]["predicted"] = assimilation("".join([x["fine_vowels"] for x in predicted]))
   affixChains[tuple([y["fine"] for y in d["parsed"][1:]])].append(d["original"])

def ignoreDiffs(x):
    x = x.replace("t", "T")
    x = x.replace("d", "T")
    x = x.replace("ğ", "K")
    x = x.replace("k", "K")
    x = x.replace("eye", "E")
    x = x.replace("ee", "E")
    x = x.replace("ıı", "I")
    x = x.replace("ı", "I")
    return x

def prettyPrint(code, line, count):
#  if ignoreDiffs(line[1][0]["predicted"]) != ignoreDiffs(line[0]):
    print("\t&\t".join(["+".join(code), ("!!! " if ignoreDiffs(line[1][0]["predicted"]) != ignoreDiffs(line[0]) else "# ")+line[1][0]["predicted"], line[0], line[1][0]["lemma"], line[1][0]["morph"], str(count)])+"  \\\\")

for x in sorted(list(affixChains), key=lambda x:len(affixChains[x]))[:]:
    chains = [("&".join([y["word"] for y in z]), z) for z in affixChains[x]]
    chains = [x for x in chains if "VerbForm" not in str(x)]
    chainsCount = defaultdict(int)
    for z, _ in chains:
        chainsCount[z] += 1
    chainsCount = sorted(list(chainsCount.items()), key=lambda x:x[1], reverse=True)
 #   print("===========")
#    print(x, len(affixChains[x]))
    if len(chainsCount)>0:
      prettyPrint(x, [y for y in chains if y[0] == chainsCount[0][0]][0], chainsCount[0][1])
    if(len(chainsCount)>1):
      prettyPrint(x, [y for y in chains if y[0] == chainsCount[1][0]][0], chainsCount[1][1])
    if(len(chainsCount)>2):
      prettyPrint(x, [y for y in chains if y[0] == chainsCount[2][0]][0], chainsCount[2][1])



