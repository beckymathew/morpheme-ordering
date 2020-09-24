def get_abstract_morphemes(lemma):
   if lemma == "させる" or lemma == "せる":
     lemma = "VAL_CAUSATIVE"
   elif lemma == "れる" or lemma == "られる" or lemma == "える" or lemma == "得る" or lemma == "ける":
     lemma = "VOICE/MOOD_PASSIVE_POTENTIAL"
   elif lemma == "て":
     lemma = "FIN_TE"
   elif lemma == "する":
     lemma = "DERIV_SURU"
   elif lemma == "ます":
       lemma = "POLITENESS_masu"
   elif lemma == "たい":
       lemma = "MOOD_tai"
   elif lemma == "ない":
       lemma = "POLARITY_nai"
   elif lemma == "た":
       lemma = "TAM_ta"
   elif lemma == "う":
       lemma = "TAM_yoo"
   else:
       lemma = lemma
   return lemma.split("_")[0]
