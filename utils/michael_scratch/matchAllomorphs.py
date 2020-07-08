import allomorphy
with open("../output/extracted_Korean-Kaist_2.6_forWords_Japanese_ExtractOrder_FullData_Flat_Fast_LabelAndGraph.py_7101840.tsv", "r") as inFile:
    morphemes = [x.split("\t") for x in inFile.read().strip().split("\n")]
from collections import defaultdict
reducedMorphemes = defaultdict(int)
allomorphs = defaultdict(list)
for x in morphemes:
    label, graph = x[0].split("_")
    normalized = allomorphy.get_underlying_morph(graph, label)
    frequency = int(x[2])
    print(label, graph, frequency, normalized)
    reducedMorphemes[normalized] += frequency
    allomorphs[normalized].append((graph, label))
reducedMorphemes = sorted(list(reducedMorphemes.items()), key=lambda x:x[0][1])
with open("output/matchedAllomorphs.tsv", "w") as outFile:
  for x, y in reducedMorphemes:
    print(f"{x[0]}\t{x[1]}\t{y}\t{allomorphs[x]}", file=outFile)
