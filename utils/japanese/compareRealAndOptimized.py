import sys
import os

script = "forWords_Japanese_OptimizeOrder_MorphemeGrammar_Normalized_FullData_HeldoutClip"

with open("slot-names.txt", "r") as inFile:
    slotNames = [x.split("\t") for x in inFile.read().strip().split("\n")]
slotNames = {x[0] : x[3] for x in slotNames}
print(slotNames)

with open("output/"+os.listdir("output/")[0], "r") as inFile:
    real = [x.split("\t")[0] for x in inFile.read().strip().split("\n") if ord(x[0]) < 100]
with open(f"results/{script}/"+os.listdir(f"results/{script}/")[0], "r") as inFile:
    optimized = [x.split(" ")[0] for x in inFile.read().strip().split("\n")[1:] if ord(x[0]) < 100]
print(real)
print(optimized)
real = [x for x in real if slotNames[x] != "NA"]
optimized = [x for x in optimized if slotNames[x] != "NA"]

assert len(real) == len(optimized)
ioptim = dict(list(zip(optimized, range(len(optimized)))))

with open("visualize/comparison.tex", "w") as outFile:
   print("  \\begin{tikzpicture}[%", file=outFile)
   print("% common options for blocks:", file=outFile)
   print("block/.style = {draw, fill=blue!30, align=center, anchor=west,", file=outFile)
   print("            minimum height=0.65cm, inner sep=0},", file=outFile)
   print("% common options for the circles:", file=outFile)
   print("ball/.style = {circle, draw, align=center, anchor=north, inner sep=0}]", file=outFile)
   print("\\node[rectangle,text width=1.2cm,anchor=base] (A0) at (1,-0.3) {Real};", file=outFile)
   print("\\node[rectangle,text width=0.9cm,anchor=base] (B0) at (4,-0.3) {Optimized};", file=outFile)
   for i in range(len(real)):
       print("\\node[rectangle,text width=1.2cm,anchor=base] (A"+str(i+1)+") at (1,"+str(-i/2.0-1)+") {"+slotNames[real[i]]+"};", file=outFile)
   for i in range(len(optimized)):
       print("\\node[rectangle,text width=1.2cm,anchor=base] (B"+str(i+1)+") at (4,"+str(-i/2.0-1)+") {"+slotNames[optimized[i]]+"};", file=outFile)
   for i in range(len(optimized)):
       print("\\draw[->] (A"+str(i+1)+".east) to (B"+str(ioptim[real[i]]+1)+".west);", file=outFile)
   print("\end{tikzpicture}", file=outFile)
