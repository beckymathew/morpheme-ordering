import torch
from collections import defaultdict
import glob


def pretty(x):
   x = x.split("_")
   language = x[0]
   language = language[0].upper() + language[1:]
   if "prefixes" in x:
      language += " (Prefixes)"
   elif "suffixes" in x:
      language += " (Suffixes)"
   pos = "Nouns" if "nouns" in x else "Verbs"
   return f"{language}\t{pos}"

with open(f"visualize/{__file__}.tsv", "w") as outFile:
 for language in ["finnish_nouns_adj_joint", "finnish_verbs_joint", "hungarian_nouns", "hungarian_verbs", "japanese", "korean", "sesotho_prefixes", "sesotho_suffixes", "turkish_nouns_adj", "turkish_verbs"]:
  print(language)
  try:
    with open(f"{language}/universal_alignment.txt", "r") as inFile:
     alignment = [x.split("\t") for x in inFile.read().strip().split("\n")]
     alignment = {x[0] : x[-1] for x in alignment}
     print(alignment)
  except FileNotFoundError:
     alignment = {}
  mis = glob.glob(f"{language}/cond_mi_bySlot/evaluateCond*tsv")
  perUniversal = defaultdict(list)
  with open(mis[0], "r") as inFile:
     for line in inFile:
        line = line.strip().split("\t")
#        print(line)
        a1, a2 = line[0], line[1]
        if "prefixes" in language:
           a1, a2 = a2, a1
        if a1  == "ROOT" and a1 != a2:
           frequency, mean, sd = [float(q) for q in line[2:]]
#           print(alignment.get(a2, a2), a2, line[2:])
           perUniversal[alignment.get(a2, a2)].append((frequency, mean, sd))
  for category in perUniversal:
     frequencies, means, sds = [torch.FloatTensor(q) for q in zip(*perUniversal[category])]
     summed = (frequencies * means).sum()
     square_summed = (frequencies * (sds + means.pow(2))).sum()
     mean = float(summed/frequencies.sum())
     sd = float(square_summed/frequencies.sum()) - (mean**2)
     se = sd / float(frequencies.sum().sqrt())
     print("\t".join([str(q) for q in [pretty(language), category, mean, sd, se]]), file=outFile)
