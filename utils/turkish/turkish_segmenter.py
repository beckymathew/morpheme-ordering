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
        morphs.append("Cau")
        morphs.append("Pass")
    elif voice:
        morphs.append(voice)

    # potential mood comes before negative marker
    mood = label_dict.get("Mood")
    if mood == "Pot": # https://www.turkishexplained.com/negpot.htm, https://www.turkishexplained.com/cancant.htm   
        morphs.append(mood)
    
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
                elif label_dict.get("Tense") == "Pqp":
                    morphs.append("Pqp")
            
            if mood in ["Cnd", "Opt", "Imp", "Des", "Nec"]: # https://turkishexplained.com/conditional.htm, https://turkishteatime.com/turkish-grammar-guide/subjunctive/, https://www.turkishexplained.com/imperative.htm, https://fluentinturkish.com/grammar/turkish-verb-moods, https://turkishlesson.tr.gg/Necessitative.htm
                morphs.append(mood) 
            elif mood == "DesPot":
                morphs.append("Des")
                morphs.append("Pot")

            # (3) A special suffix -lar- for 3rd person plural
            morphs.append("3Plur")
        else:
            if mood in ["Cnd", "Opt", "Imp", "Des", "Nec"]: # https://turkishexplained.com/conditional.htm, https://turkishteatime.com/turkish-grammar-guide/subjunctive/, https://www.turkishexplained.com/imperative.htm, https://fluentinturkish.com/grammar/turkish-verb-moods, https://turkishlesson.tr.gg/Necessitative.htm
                morphs.append(mood) 
            elif mood == "DesPot":
                morphs.append("Des")
                morphs.append("Pot")

            # (3) A special suffix -lar- for 3rd person plural
            morphs.append("3Plur")

            # (4) A second Tense/Aspect/Mood/... suffix slot
            if label_dict.get("Evident"):
                morphs.append("Indirect")
            else:
                if label_dict.get("Tense") == "Past":
                    morphs.append("Past")
                elif label_dict.get("Tense") == "Pqp":
                    morphs.append("Pqp")
    else:
        if label_dict.get("Evident"):
            morphs.append("Indirect")
        else:
            if label_dict.get("Tense") == "Past":
                morphs.append("Past")
            elif label_dict.get("Tense") == "Pqp":
                    morphs.append("Pqp")

        if mood in ["Cnd", "Opt", "Imp", "Des", "Nec"]: # https://turkishexplained.com/conditional.htm, https://turkishteatime.com/turkish-grammar-guide/subjunctive/, https://www.turkishexplained.com/imperative.htm, https://fluentinturkish.com/grammar/turkish-verb-moods, https://turkishlesson.tr.gg/Necessitative.htm
            morphs.append(mood) 
        elif mood == "DesPot":
            morphs.append("Des")
            morphs.append("Pot")

    # (5) Person/Number agreement (might be split into Person+Number in the 2nd person, I've written more in turkish-olmak.tsv.csv)
    # Person and Number are not systematically separate morphemes, so I have them labeled in a single morpheme here
    if person in ["1","2"]: # skip 3SG because it's void
        morphs.append(person + number)
    
    if label_dict.get("Polite") == "Form": # https://elon.io/learn-turkish/lesson/the-suffix-dir-formal-usage
        morphs.append("Form")
        # can't tell if this is correct bc couldn't find good sources
        # there's only 7 verbs w this label in the notes, so here's my guess based on those 7

    if mood == "Gen": # copula
        morphs.append(mood)

    return morphs

    # TODO: interrogative
    # Tense=Pqp? Seems to be indirect? Usually looks like mıştı but I don't know if it's mış+tı
    #   Pqp tense is miş-ti, which maybe could be broken down into Pqp+Past
    # Mood: Ind, Cnd, Imp, Pot, Gen, Opt, Des, DesPot, Nec
    #   Gen comes after TAM suffix ?
    #   Indicative is default?
    # Polite
    #   It looks informal is default, although I don't know why only some of the verbs have Polite labeled