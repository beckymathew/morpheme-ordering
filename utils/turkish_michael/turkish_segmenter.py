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
        morphs.append("Cau_t")
        morphs.append("Pass_il")
    elif voice == "Cau":
        morphs.append("Cau_t")
    elif voice == "Pass":
        morphs.append("Pass_il")
    elif voice:
        morphs.append(voice)

    # potential mood comes before negative marker
    mood = label_dict.get("Mood")
    if mood == "Pot": # https://www.turkishexplained.com/negpot.htm, https://www.turkishexplained.com/cancant.htm   
        morphs.append("Pot_bil")
    

    # (2) Tense/Aspect/Mood/Polarity/... Maybe this can be split into multiple slots, I've written more on this in turkish-olmak.tsv.csv.
    # negative comes before indirect
    if label_dict.get("Polarity") == "Neg": # skip positive bc it's void
        morphs.append("Neg_ma")


    # TAM suffixes are in different slots if 3rd person plural
    # Note: Nonpast tense is not labeled bc it's void
    person = label_dict.get("Person")
    number = label_dict.get("Number")
    aspect = label_dict.get("Aspect")
    evidential = "Indir" if label_dict.get("Evident") else "Dir"
    tense = label_dict.get("Tense")
    verbform = label_dict.get("VerbForm")
    print(person, number, aspect, evidential, tense, verbform)
#    return morphs
    if mood == "Imp": # zero marking
        pass
    elif verbform is None and mood == "Cnd":
        return ["POT_TODO"]
    elif verbform is None and mood == "Opt":
        return ["POT_TODO"]

#Cau_t+TAM1_ACAK+Agr_IZ	&	sürdürelim	&	sür	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Pos|Tense=Pres|Voice=Cau	&	1  \\
#Cau_t+TAM1_ACAK+Agr_IZ	&	saldıralım	&	sal	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Pos|Tense=Pres|Voice=Cau	&	1  \\
#Cau_t+TAM1_ACAK	&	patlata	&	patla	&	Aspect=Perf|Mood=Opt|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|Voice=Cau	&	2  \\
#Neg_ma+TAM1_ACAK+Agr_IZ	&	yemeyelim	&	ye	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Neg|Tense=Pres	&	2  \\
#Neg_ma+TAM1_ACAK+Agr_IZ	&	etmeyelim	&	et	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Neg|Tense=Pres	&	1  \\
#Neg_ma+TAM1_ACAK+Agr_IZ	&	olmayalım	&	ol	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Neg|Tense=Pres	&	1  \\
#Pass_il+TAM1_ACAK	&	bakıla	&	bak	&	Aspect=Perf|Mood=Opt|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|Voice=Pass	&	2  \\
#Pass_il+TAM1_ACAK	&	gömüle	&	göm	&	Aspect=Perf|Mood=Opt|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|Voice=Pass	&	2  \\
#Neg_ma+TAM1_ACAK+Agr_IM	&	doymayayım	&	doy	&	Aspect=Perf|Mood=Opt|Number=Sing|Person=1|Polarity=Neg|Tense=Pres	&	1  \\
#TAM1_ACAK+Agr_IM	&	yazayım	&	yaz	&	Aspect=Perf|Mood=Opt|Number=Sing|Person=1|Polarity=Pos|Tense=Pres	&	4  \\
#TAM1_ACAK+Agr_IZ	&	bakalım	&	bak	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Pos|Tense=Pres	&	9  \\
#TAM1_ACAK+Agr_IZ	&	gidelim	&	git	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Pos|Tense=Pres	&	7  \\
#TAM1_ACAK+Agr_IZ	&	alalım	&	al	&	Aspect=Perf|Mood=Opt|Number=Plur|Person=1|Polarity=Pos|Tense=Pres	&	2  \\
#Neg_ma+TAM1_ACAK	&	çalmaya	&	çal	&	Aspect=Perf|Mood=Opt|Number=Sing|Person=3|Polarity=Neg|Tense=Pres	&	1  \\
 

#Pass_il+TAM1_AR+Agr_IM	&	reddedilirsem	&	reddet	&	Aspect=Hab|Mood=Cnd|Number=Sing|Person=1|Polarity=Pos|Tense=Pres|Voice=Pass	&	1  \\
#Neg_ma+TAM1_ACAK+Agr_SIN	&	i̇stemesen	&	iste	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=2|Polarity=Neg|Tense=Pres	&	1  \\
#Neg_ma+TAM1_ACAK+Agr_SINIZ	&	olmasanız	&	ol	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=2|Polarity=Neg|Tense=Pres	&	1  \\
#Neg_ma+TAM1_ACAK+Agr_SINIZ	&	konuşmasanız	&	konuş	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=2|Polarity=Neg|Tense=Pres	&	1  \\
#Cau_t+TAM1_AR+3PL_LAR	&	sıkıştırırlarsa	&	sıkış	&	Aspect=Hab|Mood=Cnd|Number=Plur|Person=3|Polarity=Pos|Tense=Pres|Voice=Cau	&	1  \\
#TAM1_ACAK+3PL_LAR	&	isteseler	&	iste	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=3|Polarity=Pos|Tense=Pres	&	1  \\
#TAM1_ACAK+3PL_LAR	&	etseler	&	et	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=3|Polarity=Pos|Tense=Pres	&	1  \\
#Cau_t+TAM1_ACAK	&	uzatsa	&	uza	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|Voice=Cau	&	1  \\
#Cau_t+TAM1_ACAK	&	aksatsa	&	aksa	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|Voice=Cau	&	1  \\
#Neg_ma+TAM1_AR+Agr_SINIZ	&	şarlamazsanız	&	şarla	&	Aspect=Hab|Mood=Cnd|Number=Plur|Person=2|Polarity=Neg|Tense=Pres	&	1  \\
#Neg_ma+TAM1_AR+Agr_SINIZ	&	keşfedemezseniz	&	keşfet	&	Aspect=Hab|Mood=CndPot|Number=Plur|Person=2|Polarity=Neg|Tense=Pres	&	1  \\
#Neg_ma+TAM1_ACAK+3PL_LAR	&	anlamasalar	&	anla	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=3|Polarity=Neg|Tense=Pres	&	1  \\
#Neg_ma+TAM1_ACAK+3PL_LAR	&	bilmeseler	&	bil	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=3|Polarity=Neg|Tense=Pres	&	1  \\
#Neg_ma+TAM1_ACAK+3PL_LAR	&	ilgilenmeseler	&	ilgilen	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=3|Polarity=Neg|Tense=Pres	&	1  \\
#TAM1_ACAK+Agr_SINIZ	&	kursanız	&	kur	&	Aspect=Perf|Mood=Cnd|Number=Plur|Person=2|Polarity=Pos|Tense=Pres	&	1  \\
#Neg_ma+TAM1_IYOR+3PL_LAR	&	onamıyorlarsa	&	ona	&	Aspect=Prog|Mood=Cnd|Number=Plur|Person=3|Polarity=Neg|Polite=Infm|Tense=Pres	&	1  \\
#TAM1_ACAK+Agr_SIN	&	görsen	&	gör	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=2|Polarity=Pos|Tense=Pres	&	2  \\
#TAM1_ACAK+Agr_SIN	&	sorsan	&	sor	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=2|Polarity=Pos|Tense=Pres	&	1  \\
#Pass_il+TAM1_ACAK	&	bağlansa	&	bağla	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|Voice=Pass	&	2  \\
#Neg_ma+TAM1_ACAK+Agr_IM	&	olmasam	&	ol	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=1|Polarity=Neg|Tense=Pres	&	1  \\
#TAM1_AR+Agr_SIN	&	i̇stersen	&	iste	&	Aspect=Hab|Mood=Cnd|Number=Sing|Person=2|Polarity=Pos|Tense=Pres	&	2  \\
#TAM1_ACAK+Agr_IM	&	baksam	&	bak	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=1|Polarity=Pos|Tense=Pres	&	2  \\
#Neg_ma+TAM1_ACAK	&	değilse	&	değil	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=3|Polarity=Neg|Tense=Pres	&	5  \\
#TAM1_ACAK	&	olsa	&	ol	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=3|Polarity=Pos|Tense=Pres	&	17  \\
#TAM1_ACAK	&	varsa	&	var	&	Aspect=Perf|Mood=Cnd|Number=Sing|Person=3|Polarity=Pos|Tense=Pres	&	4  \\

    elif verbform is None: # finite
      if evidential == "Dir":
          if tense == "Pres":
              pn = int(person) + {"Sing" : 0, "Plur" : 3}[number]
              pn_ending = ["Agr_IM", "Agr_SIN", None, "Agr_IZ", "Agr_SINIZ", None][pn-1]
  
              if aspect == "Hab":
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
    
    if label_dict.get("Polite") == "Form": # https://elon.io/learn-turkish/lesson/the-suffix-dir-formal-usage
        morphs.append("Form")
        # can't tell if this is correct bc couldn't find good sources
        # there's only 7 verbs w this label in the notes, so here's my guess based on those 7

    if mood == "Gen": # copula
        morphs.append("Gen_dir")

    # Verbal nouns -- can't find a lot of examples of these that don't look exactly like the infinitive
    if label_dict.get("VerbForm") == "Vnoun":
        morphs.append("Vnoun_mak")
        if label_dict.get("Number[psor]") and label_dict.get("Person[psor]"):
            morphs.append(label_dict.get("Number[psor]") + label_dict.get("Person[psor]"))

    return morphs

    # TODO: interrogative
    # Tense=Pqp? Seems to be indirect? Usually looks like mıştı but I don't know if it's mış+tı
    #   Pqp tense is miş-ti, which maybe could be broken down into Pqp+Past
    # Mood: Ind, Cnd, Imp, Pot, Gen, Opt, Des, DesPot, Nec
    #   Gen comes after TAM suffix ?
    #   Indicative is default?
    # Polite
    #   It looks informal is default, although I don't know why only some of the verbs have Polite labeled
