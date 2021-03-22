#!/bin/bash
for i in {1..50}
do
    python3 forWords_Sesotho_EvaluateWeights_Coarse.py --model UNIV
done

for i in {1..50}
do
    python3 forWords_Sesotho_EvaluateWeights_Coarse.py --model RANDOM
done


