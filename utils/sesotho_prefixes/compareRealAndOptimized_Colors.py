import sys
import os

script = "forWords_Sesotho_OptimizeOrder_Slots_ByType_Suffixes_HeldoutClip"

with open("universal_alignment.txt", "r") as inFile:
    alignment = [x.split("\t") for x in inFile.read().strip().split("\n")]
alignment = {x[0] : x[3] for x in alignment}
print(alignment)

universal = ["Valence", "Voice", "TAM", "Agreement"]


with open("output/"+os.listdir("output/")[0], "r") as inFile:
    real = [x.split("\t")[0] for x in inFile.read().strip().split("\n") if "Other" not in x and x.index("\t") > 2]
with open(f"results/{script}/"+os.listdir(f"results/{script}/")[0], "r") as inFile:
    optimized = [x.split(" ")[0] for x in inFile.read().strip().split("\n")[1:] if "Other" not in x]
print(real)
print(optimized)
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
       color = {"Valence" : "orange", "Voice" : "green", "TAM" : "blue", "Agreement" : "purple", "NA" : None}[alignment[real[i]]]
       print("\\node[rectangle,text width=1.2cm,anchor=base"+(", fill="+color+"!20" if color is not None else "") + "] (A"+str(i+1)+") at (1,"+str(-i/2.0-1)+") {"+real[i]+"};", file=outFile)
   for i in range(len(optimized)):
       color = {"Valence" : "orange", "Voice" : "green", "TAM" : "blue", "Agreement" : "purple", "NA" : None}[alignment[optimized[i]]]
       print("\\node[rectangle,text width=1.2cm,anchor=base"+(", fill="+color+"!20" if color is not None else "") + "] (B"+str(i+1)+") at (4,"+str(-i/2.0-1)+") {"+optimized[i]+"};", file=outFile)
   for i in range(len(optimized)):
       print("\\draw[->] (A"+str(i+1)+".east) to (B"+str(ioptim[real[i]]+1)+".west);", file=outFile)
   print("\end{tikzpicture}", file=outFile)
