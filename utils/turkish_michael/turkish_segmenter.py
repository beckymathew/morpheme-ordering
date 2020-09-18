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
        morphs.append("MOOD_Pot_bil")






    # (2) Tense/Aspect/Mood/Polarity/... Maybe this can be split into multiple slots, I've written more on this in turkish-olmak.tsv.csv.
    # negative comes before indirect
    if label_dict.get("Polarity") == "Neg": # skip positive bc it's void
        morphs.append("POLAR_Neg_ma")


    # TAM suffixes are in different slots if 3rd person plural
    # Note: Nonpast tense is not labeled bc it's void
    person = label_dict.get("Person")
    number = label_dict.get("Number")
    aspect = label_dict.get("Aspect")
    evidential = "Indir" if label_dict.get("Evident") else "Dir"
    tense = label_dict.get("Tense")
    verbform = label_dict.get("VerbForm")
    polite = label_dict.get("Polite")
    print(person, number, aspect, evidential, tense, verbform)
#    return morphs







    if mood == "Imp": # zero marking
        if person == "2":
           pass
        elif person == "3":
           morphs.append("Agr_SIN")           
    elif verbform is None and polite == "Form":
        morphs.append("POLITE_MAKTA")
    elif verbform is None and mood == "Opt":
        if person == "1" and number == "Plur":
            morphs.append("MOOD_OPT_1Pl_ELIM")
        elif person == "1" and number == "Sing":
            morphs.append("MOOD_OPT_1Pl_EYIM")
        elif person == "3" and number == "Sing":
            morphs.append("MOOD_OPT_2Sg_a")


# QUESTIOIN
#TAM1_IYOR+Form	&	ulaşmakta	&	ulaş	&	Aspect=Prog|Mood=Ind|Number=Sing|Person=3|Polarity=Pos|Polite=Form|Tense=Pres	&	1  \\	TODO
#TAM1_IYOR+Form	&	oturmakta	&	otur	&	Aspect=Prog|Mood=Ind|Number=Sing|Person=3|Polarity=Pos|Polite=Form|Tense=Pres	&	1  \\
#TAM1_IYOR+Form	&	soymakta	&	soy	&	Aspect=Prog|Mood=Ind|Number=Sing|Person=3|Polarity=Pos|Polite=Form|Tense=Pres	&	1  \\

#TAM1_ACAK+Agr_IM	&	gitmeliyim	&	git	&	Aspect=Perf|Mood=Nec|Number=Sing|Person=1|Polarity=Pos|Tense=Pres	&	3  \\	TODO
#TAM1_ACAK+Agr_IM	&	dönmeliyim	&	dön	&	Aspect=Perf|Mood=Nec|Number=Sing|Person=1|Polarity=Pos|Tense=Pres	&	2  \\
#TAM1_ACAK+Agr_IM	&	anlatmalıyım	&	anlat	&	Aspect=Perf|Mood=Nec|Number=Sing|Person=1|Polarity=Pos|Tense=Pres	&	1  \\
#POL_Neg_ma+TAM1_ACAK+Agr_IM	&	değilim	&	değil	&	Aspect=Perf|Mood=Ind|Number=Sing|Person=1|Polarity=Neg|Tense=Pres	&	14  \\	TODO

#TAM1_ACAK	&	olmalı	&	ol	&	Aspect=Perf|Mood=Nec|Number=Sing|Person=3|Polarity=Pos|Tense=Pres	&	4  \\	TODO
#TAM1_ACAK	&	olsa	&	ol	&	Aspect=Perf|Mood=Des|Number=Sing|Person=3|Polarity=Pos|Tense=Pres	&	3  \\

#TAM1_ACAK	&	konuşabilmeli	&	konuş	&	Aspect=Perf|Mood=NecPot|Number=Sing|Person=3|Polarity=Pos|Tense=Pres	&	1  \\
#POL_Neg_ma+TAM1_ACAK+Gen_dir	&	değildir	&	değil	&	Aspect=Perf|Mood=Gen|Number=Sing|Person=3|Polarity=Neg|Tense=Pres	&	15  \\	TODO
#Gen_dir	&	olacaktır	&	ol	&	Aspect=Perf|Mood=Gen|Number=Sing|Person=3|Polarity=Pos|Tense=Fut	&	5  \\	TODO
#Gen_dir	&	girecektir	&	gir	&	Aspect=Perf|Mood=Gen|Number=Sing|Person=3|Polarity=Pos|Tense=Fut	&	1  \\
#Gen_dir	&	çarpacaktır	&	çarp	&	Aspect=Perf|Mood=Gen|Number=Sing|Person=3|Polarity=Pos|Tense=Fut	&	1  \\


#

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

# TODO CndPot
#POL_Neg_ma+TAM1_ACAK	&	bilemese	&	bil	&	Aspect=Perf|Mood=CndPot|Number=Sing|Person=3|Polarity=Neg|Tense=Pres	&	1  \\
#POL_Neg_ma+TAM1_AR+Agr_SINIZ	&	keşfede=mez=seniz	&	keşfet	&	Aspect=Hab|Mood=CndPot|Number=Plur|Person=2|Polarity=Neg|Tense=Pres	&	1  \\




                  morphs.append("TAM1_SA_Cnd")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
              elif mood == "Cnd" and aspect == "Hab":
                  morphs.append("TAM1_AR")
                  if person == "3" and number == "Plur":
                      morphs.append("3PL_LAR")
                  morphs.append("TAM2_SA_Cnd")
                  if pn_ending is not None:
                     morphs.append(pn_ending)
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


#    if person == "3" and number == "Plur": 
#        if aspect == "Perf":
#            # (4) A second Tense/Aspect/Mood/... suffix slot
#            if label_dict.get("Evident"):
#                morphs.append("Indirect")
#            else:
#                if label_dict.get("Tense") == "Past":
#                    morphs.append("Past")
#                elif label_dict.get("Tense") == "Pqp":
#                    morphs.append("Pqp")
#            
#            if mood in ["Cnd", "Opt", "Imp", "Des", "Nec"]: # https://turkishexplained.com/conditional.htm, https://turkishteatime.com/turkish-grammar-guide/subjunctive/, https://www.turkishexplained.com/imperative.htm, https://fluentinturkish.com/grammar/turkish-verb-moods, https://turkishlesson.tr.gg/Necessitative.htm
#                morphs.append(mood) 
#            elif mood == "DesPot":
#                morphs.append("Des")
#                morphs.append("Pot")
#
#            # (3) A special suffix -lar- for 3rd person plural
#            morphs.append("3Plur")
#        else:
#            if mood in ["Cnd", "Opt", "Imp", "Des", "Nec"]: # https://turkishexplained.com/conditional.htm, https://turkishteatime.com/turkish-grammar-guide/subjunctive/, https://www.turkishexplained.com/imperative.htm, https://fluentinturkish.com/grammar/turkish-verb-moods, https://turkishlesson.tr.gg/Necessitative.htm
#                morphs.append(mood) 
#            elif mood == "DesPot":
#                morphs.append("Des")
#                morphs.append("Pot")
#
#            # (3) A special suffix -lar- for 3rd person plural
#            morphs.append("3Plur")
#
#            # (4) A second Tense/Aspect/Mood/... suffix slot
#            if label_dict.get("Evident"):
#                morphs.append("Indirect")
#            else:
#                if label_dict.get("Tense") == "Past":
#                    morphs.append("Past")
#                elif label_dict.get("Tense") == "Pqp":
#                    morphs.append("Pqp")
#    else:
#        if label_dict.get("Evident"):
#            morphs.append("Indirect")
#        else:
#            if label_dict.get("Tense") == "Past":
#                morphs.append("Past")
#            elif label_dict.get("Tense") == "Pqp":
#                    morphs.append("Pqp")
#
#        if mood in ["Cnd", "Opt", "Imp", "Des", "Nec"]: # https://turkishexplained.com/conditional.htm, https://turkishteatime.com/turkish-grammar-guide/subjunctive/, https://www.turkishexplained.com/imperative.htm, https://fluentinturkish.com/grammar/turkish-verb-moods, https://turkishlesson.tr.gg/Necessitative.htm
#            morphs.append(mood) 
#        elif mood == "DesPot":
#            morphs.append("Des")
#            morphs.append("Pot")
#
#    # (5) Person/Number agreement (might be split into Person+Number in the 2nd person, I've written more in turkish-olmak.tsv.csv)
#    # Person and Number are not systematically separate morphemes, so I have them labeled in a single morpheme here
#    if person in ["1","2"]: # skip 3SG because it's void
#        morphs.append(person + number)
    

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
