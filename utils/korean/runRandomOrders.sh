#!/bin/bash
for i in {1..50}
do
    ~/python-py37-mhahn forWords_Korean_RandomOrder_MorphemeMeanings_WithoutAdnominals_DoubleSplit_Repeats_Seg1.py --model UNIV
done

for i in {1..50}
do
    ~/python-py37-mhahn forWords_Korean_RandomOrder_MorphemeMeanings_WithoutAdnominals_DoubleSplit_Repeats_Seg1.py --model RANDOM
done


