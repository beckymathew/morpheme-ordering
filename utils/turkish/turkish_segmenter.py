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
    voice = label_dict.get("Voice")
    if voice:
        morphs.append(voice)

    
    # TAM suffixes are in different slots if 3rd person plural
    # Note: Nonpast tense is not labeled bc it's void
    person = label_dict.get("Person")
    number = label_dict.get("Number")

    # (2) Tense/Aspect/Mood/Polarity/... Maybe this can be split into multiple slots, I've written more on this in turkish-olmak.tsv.csv.
    # negative comes before indirect
    if label_dict.get("Polarity") == "Neg": # skip positive bc it's void
        morphs.append("Neg")

    # In the UD corpus, Prog is Wikipedia's imperfective and Hab is Wikipedia's aorist
    aspect = label_dict.get("Aspect")
    if aspect == "Prog": # should look like -yor-
        morphs.append("IMPERFECTIVE")
    elif aspect == "Prosp":
        morphs.append("PROSPECTIVE")
    elif aspect == "Hab": # can't tell if aorist or perfective is the default
        morphs.append("AORIST")
    elif aspect == "Perf":
        morphs.append("PERFECTIVE")

    if person == "3" and number == "Plur": 
        if aspect == "Perf":
            # (4) A second Tense/Aspect/Mood/... suffix slot
            if label_dict.get("Evident"):
                morphs.append("Indirect")
            else:
                if label_dict.get("Tense") == "Past":
                    morphs.append("Past")
            
            # (3) A special suffix -lar- for 3rd person plural
            morphs.append("3Plur")
        else:
            # (3) A special suffix -lar- for 3rd person plural
            morphs.append("3Plur")

            # (4) A second Tense/Aspect/Mood/... suffix slot
            if label_dict.get("Evident"):
                morphs.append("Indirect")
            else:
                if label_dict.get("Tense") == "Past":
                    morphs.append("Past")
    else:
        if label_dict.get("Evident"):
            morphs.append("Indirect")
        else:
            if label_dict.get("Tense") == "Past":
                morphs.append("Past")
   
    # (5) Person/Number agreement (might be split into Person+Number in the 2nd person, I've written more in turkish-olmak.tsv.csv)
    # Person and Number are not systematically separate morphemes, so I have them labeled in a single morpheme here
    if person in ["1","2"]: # skip 3SG because it's void
        morphs.append(person + number)
    
    return morphs

    # TODO: interrogative
    # TODO: voice morphemes (caus, pass, causpass) https://www.turkishexplained.com/passivemood.htm
    # TODO: Tense=Pqp? Seems to be indirect. Also, any Evident other than Nfh?
    # TODO: Mood
    # TODO: Polite