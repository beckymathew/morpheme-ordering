#!/bin/bash
for i in {1..50}
do
    python3 forWords_Hungarian_RandomOrder_Coarse_FineSurprisal.py --model RANDOM
done

python3 forWords_Hungarian_RandomOrder_Coarse_FineSurprisal.py --model REAL

python3 forWords_Hungarian_RandomOrder_Coarse_FineSurprisal.py --model REVERSE
