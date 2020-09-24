#!/bin/bash
for i in {1..50}
do
    python3 forWords_Hungarian_RandomOrder_Fine.py --language Hungarian --model RANDOM
    python3 forWords_Hungarian_RandomOrder_Coarse.py --language Hungarian --model RANDOM
done

python3 forWords_Hungarian_RandomOrder_Fine.py --language Hungarian --model REAL
python3 forWords_Hungarian_RandomOrder_Coarse.py --language Hungarian --model REAL

python3 forWords_Hungarian_RandomOrder_Fine.py --language Hungarian --model REVERSE
python3 forWords_Hungarian_RandomOrder_Coarse.py --language Hungarian --model REVERSE