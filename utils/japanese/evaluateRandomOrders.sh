#!/bin/bash
for i in {1..50}
do
    ~/python-py37-mhahn forWords_Celex_EvaluateWeights_MorphemeGrammar_FullData.py --model UNIV
done

for i in {1..50}
do
    ~/python-py37-mhahn forWords_Celex_EvaluateWeights_MorphemeGrammar_FullData.py --model RANDOM
done


