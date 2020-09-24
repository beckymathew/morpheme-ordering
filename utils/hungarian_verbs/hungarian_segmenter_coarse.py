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
        morphs.append("Valence")




    tense = label_dict.get("Tense")
    definite = label_dict.get("Definite")
    person = label_dict.get("Person")
    number = label_dict.get("Number")
    mood = label_dict.get("Mood")
    if mood is not None and "Pot" in mood:
        morphs.append("Mood")

    if label_dict.get("VerbForm") == "Inf":
        morphs.append("Inf")


    if label_dict.get("VerbForm") == "Inf" and person is not None:
      personNumber = int(person) + {"Sing" : 0, "Plur" : 3}[number]
      byPerson = [["Agr"], ["Agr"], [], ["Agr"], ["Agr"], ["Agr"]]
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
          byPerson = [["Agr"], ["Agr"], [], ["Agr"], ["Agr"], ["Agr"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Ind' and tense == "Pres" and definite == "Def":
          byPerson = [["Agr"], ["Agr"], ["Agr"], ["Agr"], ["Agr"], ["Agr"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Ind' and tense == "Past" and definite == "Ind":
          byPerson = [["Tense", "Agr"], ["Tense", "Agr"], ["Tense"], ["Tense",  "Agr"], ["Tense",  "Agr"], ["Tense",  "Agr"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Ind' and tense == "Past" and definite == "Def":
          byPerson = [["Tense", "Agr"], ["Tense", "Agr"], ["Tense", "Agr"], ["Tense",  "Agr"], ["Tense","Agr"], ["Tense", "Agr"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Cnd' and definite == "Ind":
          byPerson = [["Mood", "Agr"], ["Mood", "Agr"], ["Mood"], ["Mood",  "Agr"], ["Mood", "Agr"], ["Mood", "Agr"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Cnd' and definite == "Def":
          byPerson = [["Mood", "Agr"], ["Mood", "Agr"], ["Mood", "Agr"], ["Mood",  "Agr"], ["Mood", "Agr"], ["Mood", "Agr"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Subj' and definite == "Ind":
          byPerson = [["Mood", "Agr"], ["Mood", "Agr"], ["Mood", "Agr"], ["Mood",  "Agr"], ["Mood", "Agr"], ["Mood", "Agr"]]
          morphs += byPerson[personNumber-1]
      elif mood == 'Subj' and definite == "Def":
          byPerson = [["Mood", "Agr"], ["Mood", "Agr"], ["Mood", "Agr"], ["Mood",  "Agr"], ["Mood", "Agr"], ["Mood", "Agr"]]
          morphs += byPerson[personNumber-1]
      else:
          assert False, (label_dict, mood, definite, tense)
  
    
    return morphs
    # TODO: 2po in Wikipedia doesn't show up in corpus
    # http://www.hungarianreference.com/Verbs/Causative-at-tat.aspx says causative + potential + conditional = could make do something
    # but mood that is both potential and conditional isn't attested in corpus
