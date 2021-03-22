import statsmodels.stats.proportion
directories = ["finnish_nouns_adj", "turkish_nouns_adj", "hungarian_nouns", "finnish_verbs","hungarian_verbs", "turkish_verbs", "korean", "japanese", "sesotho_prefixes", "sesotho_suffixes"]
import os
import math
def mean(x):
    if len(x) == 0:
       return float("inf")
    return round(sum(x)/len(x),2)
def sd(l):
    return round(math.sqrt(max(0,mean([x**2 for x in l]) - mean(l)**2)),2)
def process(x):
      if len(x) == 0:
          return "--"
      else:
          return f"{mean(x)} ({sd(x)})"
with open("output/accuracies.tex", "w") as outFile:
 with open("output/accuracies.tsv", "w") as outTSV:
  for dCount, d in enumerate(directories):
    path = d+"/results/"
    files = [x for x in os.listdir(path) if x.startswith("accuracy")]
    accuracies = {"Optimized" : [], "Baseline" : [], "Universals" : []}
    for f in files:
        with open(path+"/"+f, "r") as inFile:
            resu = inFile.read().strip().split("\n")
            accuracies["Baseline" if "RANDOM" in f else ("Universals" if "UNIV" in f else "Optimized")].append([float(x) for x in resu[:4]])
    pos = "Nouns" if "noun" in d else "Verbs"
    rowName = d[:d.index("_")] if "_" in d else d
    rowName = rowName[0].upper() + rowName[1:]
    if "prefi" in d:
      rowName += " (P)"
    elif "suffi" in d:
      rowName += " (S)"

    language = rowName
    for c in ["Universals", "Baseline", "Optimized"]:
      if c == "Baseline":
         c1 = "Random"
      else:
        c1 = c
      for x in accuracies[c]:
       print("\t".join([pos, language, c1, str(x[0])]), file=outTSV)
    univ_pairs = process([x[0] for x in accuracies["Universals"]])
    bas_pairs = process([x[0] for x in accuracies["Baseline"]])
    bas_full = process([x[1] for x in accuracies["Baseline"]])
    bas_full_types = process([x[3] for x in accuracies["Baseline"]])
    opt_pairs = process([x[0] for x in accuracies["Optimized"]])
    opt_full = process([x[1] for x in accuracies["Optimized"]])
    opt_full_types = process([x[3] for x in accuracies["Optimized"]])
    meanOptimized = mean([x[0] for x in accuracies["Optimized"]])
    betterThan_u = sum([1 if x[0]<=meanOptimized else 0  for x in accuracies["Universals"]])
    total_u = len(accuracies["Universals"])+0.00001
    lower_u, higher_u = statsmodels.stats.proportion.proportion_confint(betterThan_u, total_u, method="jeffreys")
    betterThan = sum([1 if x[0]<=meanOptimized else 0  for x in accuracies["Baseline"]])
    total = len(accuracies["Baseline"])
    lower, higher = statsmodels.stats.proportion.proportion_confint(betterThan, total, method="jeffreys")
    if dCount == 0:
       firstColumn = "\multirow{3}{*}{Nouns}"
    elif dCount == 3:
       firstColumn = "\multirow{7}{*}{Verbs}"
    else:
       firstColumn = ""
    if total == 0:
       total = 0.0000001 
    # if the noun portion is over, print htis:  \hline
    print(f"{firstColumn} & {rowName} & {opt_pairs} & {bas_pairs} & {round(betterThan/total,2)}  [{round(lower,2)}, {round(higher, 2)}]  & {univ_pairs} &  {round(betterThan_u/total_u,2)}  [{round(lower_u,2)}, {round(higher_u, 2)}]  \\\\", file=outFile)                
    print(f"{firstColumn} & {rowName} & {opt_pairs} & {bas_pairs} & {round(betterThan/total,2)}  [{round(lower,2)}, {round(higher, 2)}]  & {univ_pairs} &  {round(betterThan_u/total_u,2)}  [{round(lower_u,2)}, {round(higher_u, 2)}]  \\\\")                
    if dCount == 2:
      print("\\hline", file=outFile)
#    print(f" & {d.replace('_', ' ')} & {opt_pairs} & {bas_pairs} & {opt_full} & {bas_full} & {opt_full_types} & {bas_full_types} \\\\")                

