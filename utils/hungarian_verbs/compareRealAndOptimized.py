import sys
import os

with open("output/"+os.listdir("output/")[0], "r") as inFile:
    real = [x.split("\t")[0] for x in inFile.read().strip().split("\n")]
with open("results/forWords_Hungarian_OptimizeOrder_Coarse_FineSurprisal/"+os.listdir("results/forWords_Hungarian_OptimizeOrder_Coarse_FineSurprisal/")[0], "r") as inFile:
    optimized = [x.split(" ")[0] for x in inFile.read().strip().split("\n")[1:]]
print(real)
print(optimized)
assert len(real) == len(optimized)
ioptim = dict(list(zip(optimized, range(len(optimized)))))

for i in range(len(real)):
    print("\\node[rectangle,text width=1.2cm,anchor=base] (A"+str(i+1)+") at (1,"+str(i/2.0-1)+") {"+real[i]+"};")
for i in range(len(optimized)):
    print("\\node[rectangle,text width=1.2cm,anchor=base] (B"+str(i+1)+") at (4,"+str(-i/2.0-1)+") {"+optimized[i]+"};")
for i in range(len(optimized)):
    print("\\draw[->] (A"+str(i+1)+".east) to (B"+str(ioptim[real[i]]+1)+".west);")

