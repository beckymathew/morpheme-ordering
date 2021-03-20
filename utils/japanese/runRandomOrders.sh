#!/bin/bash
for i in {1..50}
do
    python3 forWords_Japanese_RandomOrder_FormsPhonemesFull_FullData_Heldout.py --model UNIV
done
for i in {1..50}
do
    python3 forWords_Japanese_RandomOrder_FormsPhonemesFull_FullData_Heldout.py --model RANDOM
done

python3 forWords_Japanese_RandomOrder_FormsPhonemesFull_FullData_Heldout.py --model REAL

python3 forWords_Japanese_RandomOrder_FormsPhonemesFull_FullData_Heldout.py --model REVERSE
