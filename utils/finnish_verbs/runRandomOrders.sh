#!/bin/bash
for i in {1..50}
do
    python3 forWords_Finnish_RandomOrder_Fine.py --language Finnish --model RANDOM
    python3 forWords_Finnish_RandomOrder_Coarse.py --language Finnish --model RANDOM
    python3 forWords_Finnish_RandomOrder_Coarse_FineSurprisal.py --language Finnish --model RANDOM
done

python3 forWords_Finnish_RandomOrder_Fine.py --language Finnish --model REAL
python3 forWords_Finnish_RandomOrder_Coarse.py --language Finnish --model REAL
python3 forWords_Finnish_RandomOrder_Coarse_FineSurprisal.py --language Finnish --model REAL

python3 forWords_Finnish_RandomOrder_Fine.py --language Finnish --model REVERSE
python3 forWords_Finnish_RandomOrder_Coarse.py --language Finnish --model REVERSE
python3 forWords_Finnish_RandomOrder_Coarse_FineSurprisal.py --language Finnish --model REVERSE