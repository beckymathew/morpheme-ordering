def get_abstract_morphemes(labels):
    """
    Takes the string of UD labels for a Turkish verb and returns a list of abstract morphemes.
    Parameters:
     - labels: A string of UD labels for a Turkish verb, such as 'Aspect=Perf|Mood=Ind|Number=Sing|Person=3|Polarity=Pos|Tense=Past'

    Returns:
     - A list of abstract morphemes in order. 
    """

    # creating dictionary from labels string
    label_pairs = labels.split("|")
    label_dict = {}
    for pair in label_pairs:
        k, v = pair.split("=")
        label_dict[k] = v

    morphs = ["ROOT"]

    # (1) Voice and maybe other derivational suffixes, which may have some order among themselves (?)
    # https://www.turkishexplained.com/passivemood.htm
    # although the link includes reflexive and ability, the corpus only has causative, passive, and causative-passive
    voice = label_dict.get("Voice")
    if voice == "CauPass":
        morphs.append("VAL_Cau_tir")
        morphs.append("VOICE_Pass_il")
    elif voice == "Cau":
        morphs.append("VAL_Cau_tir")
    elif voice == "Pass":
        morphs.append("VOICE_Pass_il")
    elif voice:
        morphs.append(voice)

    # potential mood comes before negative marker
    polarity = label_dict.get("Polarity")
    mood = label_dict.get("Mood")
    if mood == "Pot" and polarity == "Pos": # https://www.turkishexplained.com/negpot.htm, https://www.turkishexplained.com/cancant.htm   
        morphs.append("MOOD_Pot_ebil")






    # TAM suffixes are in different slots if 3rd person plural
    # Note: Nonpast tense is not labeled bc it's void
    person = label_dict.get("Person")
    number = label_dict.get("Number")
    aspect = label_dict.get("Aspect")
    evidential = "Indir" if label_dict.get("Evident") else "Dir"
    tense = label_dict.get("Tense")
    verbform = label_dict.get("VerbForm")
    polite = label_dict.get("Polite")
    #print(person, number, aspect, evidential, tense, verbform)
#    return morphs

    # (2) Tense/Aspect/Mood/Polarity/... Maybe this can be split into multiple slots, I've written more on this in turkish-olmak.tsv.csv.
    # negative comes before indirect
    if label_dict.get("Polarity") == "Neg": # skip positive bc it's void
     if aspect=="Perf" and mood in ["Ind", "Gen"] and polarity=="Neg" and tense=="Pres":
         pass # zero polarity and TAM marking in this case
     else:
        morphs.append("POLAR_Neg_ma")


    if aspect=="Hab" and mood == "Pot" and number=="Sing" and person=="3" and polarity=="Neg" and tense=="Past" and voice=="Pass":
        morphs.append("MOOD_TODO_zdI")


    if mood == "Pot" and polarity == "Pos" and aspect=="Hab" and tense == "Past":
      morphs.append("MOOD_TODO_lerdi")
      pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
      pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_IZ", "Agr_SINIZ", None][pn-1]
      if pn_ending is not None:
         morphs.append(pn_ending)



    if mood == "Imp": # zero marking
        # -in, -iniz, -sin, -sinler
     if label_dict.get("Polarity") == "Neg":
        if person == "2" and aspect == "Perf" and number == "Plur" and tense == "Pres":
           morphs.append("MOOD_TODO_yIn")
        elif person == "3" and aspect == "Perf" and number == "Sing" and tense == "Pres":
           morphs.append("MOOD_TODO_sIn")
     else:
        if person == "2" and number == "Plur":
           morphs.append("MOOD_TODO_In")
        elif person == "2":
           pass
        elif person == "3":
           morphs.append("Agr_SIN")           
    elif verbform is None and polite == "Form":
        morphs.append("POLITE_MAKTA")
    elif verbform is None and mood == "Opt":
        if person == "1" and number == "Plur":
            morphs.append("Agr_OPT_1Pl_ELIM")
        elif person == "1" and number == "Sing":
            morphs.append("Agr_OPT_1Pl_EYIM")
        elif person == "3" and number == "Sing":
            morphs.append("Agr_OPT_2Sg_a")
    elif aspect=="Perf" and mood in ["Ind", "Gen"] and polarity=="Neg" and tense=="Pres":
       if person is not None:
         pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
         pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_IZ", "Agr_SINIZ", None][pn-1]
         if pn_ending is not None:
            morphs.append(pn_ending)
         if person == "3" and number == "Plur":
             morphs.append("3PL_LAR")
    elif verbform is None: # finite
      if evidential == "Dir":
          if tense == "Pres" or tense=="Fut":
              pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
              pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_IZ", "Agr_SINIZ", None][pn-1]
              if mood == "Nec":
                  morphs.append("TAM1_MALI_Nec")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")

              elif mood == "Cnd" and aspect == "Perf":
                  pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_K", "Agr_SINIZ", None][pn-1]
                  morphs.append("TAM1_SA_Cnd")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
              elif mood == "Cnd" and aspect == "Hab":
                  pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_K", "Agr_SINIZ", None][pn-1]
                  morphs.append("TAM1_AR")
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
                  morphs.append("TAM2_SA_Cnd")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
              elif aspect == "Hab" and tense == "Pres" and polarity == "Neg":
                 morphs.append("TAM1_TODO_Az") # This suffix always directly follows the negative -mA-
                 if person == "3" and number == "Plur":
                     morphs.append("3PL_LAR")
                 if pn_ending is not None:
                    morphs.append(pn_ending)

# TODO the following forms match this description but don't have the Az suffix:
#POLAR_Neg_ma+TAM1_TODO_Az+Agr_IM        &       !!! bilmeezim   &       bilmem  &       bil     &       Aspect=Hab|Mood=Ind|Number=Sing|Person=1|Polarity=Neg|Tense=Pres        &       4  \\
#POLAR_Neg_ma+TAM1_TODO_Az+Agr_IM        &       !!! içmeezim    &       içmem   &       iç      &       Aspect=Hab|Mood=Ind|Number=Sing|Person=1|Polarity=Neg|Tense=Pres        &       3  \\
#POLAR_Neg_ma+TAM1_TODO_Az+Agr_IM        &       !!! anlamayazım &       anlamam &       anla    &       Aspect=Hab|Mood=Ind|Number=Sing|Person=1|Polarity=Neg|Tense=Pres        &       2  \\

# TODO Az vs Ar suffix
#POLAR_Neg_ma+TAM1_AR+TAM2_SA_Cnd        &       !!! olmaırsa    &       olmazsa &       ol      &       Aspect=Hab|Mood=Cnd|Number=Sing|Person=3|Polarity=Neg|Tense=Pres        &       2  \\
#POLAR_Neg_ma+TAM1_AR+TAM2_SA_Cnd        &       !!! gelmeirse   &       gelmezse        &       gel     &       Aspect=Hab|Mood=Cnd|Number=Sing|Person=3|Polarity=Neg|Tense=Pres        &       1  \\


# Also consider Az suffix here
#POLAR_Neg_ma+TAM1_TODO_Az+Agr_IM        &       !!! bilmeezim   &       bilmem  &       bil     &       Aspect=Hab|Mood=Ind|Number=Sing|Person=1|Polarity=Neg|Tense=Pres        &       4  \\
#POLAR_Neg_ma+TAM1_TODO_Az+Agr_IM        &       !!! içmeezim    &       içmem   &       iç      &       Aspect=Hab|Mood=Ind|Number=Sing|Person=1|Polarity=Neg|Tense=Pres        &       3  \\
#POLAR_Neg_ma+TAM1_TODO_Az+Agr_IM        &       !!! yapmayazım  &       yapamam &       yap     &       Aspect=Hab|Mood=Pot|Number=Sing|Person=1|Polarity=Neg|Tense=Pres        &       2  \\
#POLAR_Neg_ma+TAM1_TODO_Az+Agr_IM        &       !!! anlamayazım &       anlamam &       anla    &       Aspect=Hab|Mood=Ind|Number=Sing|Person=1|Polarity=Neg|Tense=Pres        &       2  \\


              elif aspect == "Hab":
                  morphs.append("TAM1_AR")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
              elif aspect == "Prog":
                  morphs.append("TAM1_IYOR")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
              elif aspect == "Perf":
                  morphs.append("TAM1_ACAK")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
          elif tense == "Past":
              pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
              pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_K", "Agr_SINIZ", None][pn-1]
              if aspect == "Perf":
                  morphs.append("TAM1_TI")
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
                  if pn_ending is not None:
                      morphs.append(pn_ending)
              elif aspect == "Prog":
                  morphs.append("TAM1_IYOR")
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
                  morphs.append("TAM2_DU")
                  if pn_ending is not None:
                      morphs.append(pn_ending)
              elif aspect == "Hab" and tense == "Pres" and polarity == "Neg":
                 morphs.append("TAM1_TODO_Az") # This suffix always directly follows the negative -mA-
                 if person == "3" and number == "Plur":
                     morphs.append("3PL_LAR")
                 morphs.append("TAM2_TODO_dI")
                 if pn_ending is not None:
                    morphs.append(pn_ending)
              elif aspect == "Hab" and tense == "Past" and polarity == "Neg":
                 morphs.append("TAM1_TODO_Az") # This suffix always directly follows the negative -mA-
                 if person == "3" and number == "Plur":
                     morphs.append("3PL_LAR")
                 morphs.append("TAM2_TODO_dI")
                 if pn_ending is not None:
                    morphs.append(pn_ending)
                     
      elif evidential == "Indir":
          pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
          pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_IZ", "Agr_SINIZ", None][pn-1]
  
          if aspect == "Perf":
              morphs.append("TAM1_MIS1")
              if person == "3" and number == "Plur":
                  morphs.append("3PL_LAR")
              if pn_ending is not None:
                 morphs.append(pn_ending)
          elif aspect == "Hab":
              morphs.append("TAM1_AR")
              if person == "3" and number == "Plur":
                  morphs.append("3PL_LAR")
              morphs.append("TAM2_MIS2")
              if pn_ending is not None:
                 morphs.append(pn_ending)
          elif aspect == "Prog":
              morphs.append("TAM1_IYOR")
              if person == "3" and number == "Plur":
                  morphs.append("3PL_LAR")
              morphs.append("TAM2_MIS2")
              if pn_ending is not None:
                 morphs.append(pn_ending)
    if tense == "Pqp":
        morphs.append("TAM1_TODO_mIş")
        if person == "3" and number == "Plur":
            morphs.append("3PL_LAR")
        morphs.append("TAM2_TODO_tI")
        pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
        pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_K", "Agr_SINIZ", None][pn-1]
        if pn_ending is not None:
           morphs.append(pn_ending)
    elif tense == "Fut,Past" and label_dict.get("Evident", None) == "Nfh":
        morphs.append("TAM1_ACAK")
        if person == "3" and number == "Plur":
            morphs.append("3PL_LAR")
        morphs.append("TAM2_TODO_mIş")
        pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
        pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_K", "Agr_SINIZ", None][pn-1]
        if pn_ending is not None:
           morphs.append(pn_ending)
    elif tense == "Fut,Past":
        morphs.append("TAM1_ACAK")
        if person == "3" and number == "Plur":
            morphs.append("3PL_LAR")
        morphs.append("TAM2_TODO_tI")
        pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
        pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_K", "Agr_SINIZ", None][pn-1]
        if pn_ending is not None:
           morphs.append(pn_ending)



    if mood == "Gen": # copula
        morphs.append("Gen_dir") # TODO lar can go after dir

    # Verbal nouns -- can't find a lot of examples of these that don't look exactly like the infinitive
    if label_dict.get("VerbForm") == "Vnoun":
        morphs.append("Vnoun_mak")
        if label_dict.get("Number[psor]") and label_dict.get("Person[psor]"):
            morphs.append("NUMPERS_"+label_dict.get("Number[psor]") + label_dict.get("Person[psor]"))

    return morphs

    # TODO: interrogative
    # Tense=Pqp? Seems to be indirect? Usually looks like mıştı but I don't know if it's mış+tı
    #   Pqp tense is miş-ti, which maybe could be broken down into Pqp+Past
    # Mood: Ind, Cnd, Imp, Pot, Gen, Opt, Des, DesPot, Nec
    #   Gen comes after TAM suffix ?
    #   Indicative is default?
    # Polite
    #   It looks informal is default, although I don't know why only some of the verbs have Polite labeled
