def get_abstract_morphemes(labels):
    """
    Takes the string of UD labels for a Hungarian verb and returns a list of abstract morphemes.
    Parameters:
     - labels: A string of UD labels for a Hungarian verb, such as 'Definite=Def|Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act'

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

    if label_dict.get("Voice") == "Cau":
        morphs.append("Cau_AT")




    tense = label_dict.get("Tense")
    definite = label_dict.get("Definite")
    person = label_dict.get("Person")
    number = label_dict.get("Number")
    mood = label_dict.get("Mood")
    if mood is not None and "Pot" in mood:
        morphs.append("Pot_HET")

    if label_dict.get("VerbForm") == "Inf":
        morphs.append("Inf_NI")


    if label_dict.get("VerbForm") == "Inf" and person is not None:
      personNumber = int(person) + {"Sing" : 0, "Plur" : 3}[number]
      byPerson = [["1sg_EM"], ["2sg_ED"], [], ["1pl_ENK"], ["2pl_TEK"], ["3pl_EK"]]
      morphs += byPerson[personNumber-1]
    if mood == "Cnd,Pot":
        mood = "Cnd"
    if mood == "Pot":
        mood = "Ind"
    if mood == "Imp":
        mood = "Subj"
    if mood == "Imp,Pot":
        mood = "Subj"
    if definite == "2":
        definite = "Def"
    if label_dict.get("VerbForm") != "Inf":
      personNumber = int(person) + {"Sing" : 0, "Plur" : 3}[number]
      if mood=='Ind' and tense == "Pres" and definite == "Ind":
          byPerson = [["1sg_EK"], ["2sg_EL"], [], ["1pl_ENK"], ["2pl_TEK"], ["3pl_NEK"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Ind' and tense == "Pres" and definite == "Def":
          byPerson = [["1sg_EM"], ["2sg_ED"], ["Def_I"], ["Def_I", "1pl_UK"], ["Def_I", "2pl_TEK"], ["Def_I", "3pl_EK"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Ind' and tense == "Past" and definite == "Ind":
          byPerson = [["Past_T", "1sg_EM"], ["Past_T", "2sg_EL"], ["Past_T"], ["Past_T",  "1pl_ENK"], ["Past_T",  "2pl_TEK"], ["Past_T",  "3pl_EK"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Ind' and tense == "Past" and definite == "Def":
          byPerson = [["Past_T", "1sg_EM"], ["Past_T", "2sg_ED"], ["Past_T", "Def_I"], ["Past_T",  "1pl_UK"], ["Past_T","Def_I",  "2pl_TEK"], ["Past_T", "Def_I", "3pl_EK"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Cnd' and definite == "Ind":
          byPerson = [["Cnd_N", "1sg_EK"], ["Cnd_N", "2sg_EL"], ["Cnd_N"], ["Cnd_N",  "1pl_ENK"], ["Cnd_N", "2pl_TEK"], ["Cnd_N", "3pl_NEK"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Cnd' and definite == "Def":
          byPerson = [["Cnd_N", "1sg_EM"], ["Cnd_N", "2sg_ED"], ["Cnd_N", "Def_I"], ["Cnd_N",  "1pl_ENK"], ["Cnd_N", "2pl_TEK"], ["Cnd_N", "3pl_EK"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Subj' and definite == "Ind":
          byPerson = [["Pot_J", "1sg_EK"], ["Pot_J", "2sg_EL"], ["Pot_J", "3sg_EN"], ["Pot_J",  "1pl_ENK"], ["Pot_J", "2pl_TEK"], ["Pot_J", "3pl_NEK"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Subj' and definite == "Def":
          byPerson = [["Pot_J", "1sg_EM"], ["Pot_J", "2sg_ED"], ["Pot_J", "3sg_E"], ["Pot_J",  "1pl_UK"], ["Pot_J", "Def_I","2pl_TEK"], ["Pot_J", "Def_I","3pl_EK"]]
          morphs += byPerson[personNumber-1]
      else:
          assert False, label_dict
  
    
    return morphs
    # TODO: 2po in Wikipedia doesn't show up in corpus
    # http://www.hungarianreference.com/Verbs/Causative-at-tat.aspx says causative + potential + conditional = could make do something
    # but mood that is both potential and conditional isn't attested in corpus
