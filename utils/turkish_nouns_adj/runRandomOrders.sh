#!/bin/bash
for i in {1..50}
do
    python3 forWords_Turkish_RandomOrder_Nouns_Coarse_FineSurprisal.py --model UNIV
done

for i in {1..50}
do
    python3 forWords_Turkish_RandomOrder_Nouns_Coarse_FineSurprisal.py --model RANDOM
done


