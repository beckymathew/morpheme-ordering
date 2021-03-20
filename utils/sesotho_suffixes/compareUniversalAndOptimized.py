import sys
import os

script = "forWords_Sesotho_OptimizeOrder_Slots_ByType_Suffixes_HeldoutClip"

with open(f"results/{script}/"+os.listdir(f"results/{script}/")[0], "r") as inFile:
    optimized = [x.split(" ")[0] for x in inFile.read().strip().split("\n")[1:] if "Other" not in x]

with open("universal_alignment.txt", "r") as inFile:
    alignment = [x.split("\t") for x in inFile.read().strip().split("\n")]
alignment = {x[0] : x[3] for x in alignment}
print(alignment)

universal = ["Valence", "Voice", "TAM", "Agreement"]

print(optimized)
ioptim = dict(list(zip(optimized, range(len(optimized)))))
iuniv = dict(list(zip(universal, range(len(universal)))))

with open("visualize/comparison-opt-uni.tex", "w") as outFile:
   print("  \\begin{tikzpicture}[%", file=outFile)
   print("% common options for blocks:", file=outFile)
   print("block/.style = {draw, fill=blue!30, align=center, anchor=west,", file=outFile)
   print("            minimum height=0.65cm, inner sep=0},", file=outFile)
   print("% common options for the circles:", file=outFile)
   print("ball/.style = {circle, draw, align=center, anchor=north, inner sep=0}]", file=outFile)
   print("\\node[rectangle,text width=1.2cm,anchor=base] (A0) at (4,-0.3) {Universal};", file=outFile)
   print("\\node[rectangle,text width=0.9cm,anchor=base] (B0) at (1,-0.3) {Optimized};", file=outFile)
   for i in range(len(universal)):
       print("\\node[rectangle,text width=1.2cm,anchor=base] (A"+str(i+1)+") at (4,"+str(-i/2.0-1)+") {"+universal[i]+"};", file=outFile)
   for i in range(len(optimized)):
       print("\\node[rectangle,text width=1.2cm,anchor=base] (B"+str(i+1)+") at (1,"+str(-i/2.0-1)+") {"+optimized[i]+"};", file=outFile)
   for i in range(len(optimized)):
       aligned = alignment[optimized[i]]
       print(aligned)
       if aligned == "NA":
           pass
       else:
           for target in aligned.split(","):
               print("\\draw[-] (A"+str(iuniv[target]+1)+".west) to (B"+str(i+1)+".east);", file=outFile)
   print("\end{tikzpicture}", file=outFile)
