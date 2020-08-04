def get_abstract_morphemes(labels):
    """
    Takes a string of UD labels for a Basque verb (with auxiliary) and returns a list of abstract morphemes.
    Parameters:
     - labels: A string of UD labels for a Basque verb, such as 'Definite=Def|Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act'

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

    # locative cases
    loc = ["Ine", "Ela", "All", "Ter", "Lat", "Loc"] # TODO: What's the terminal and elative cases?

    definite = label_dict.get("Definite")
    number = label_dict.get("Number")
    case = label_dict.get("Case")
    anim = label_dict.get("Animacy")

    # inanimate locative declension
    if anim == "Inan" and case in loc:
        if definite == "Ind":
            morphs.append(definite)
        elif definite == "Def" and number == "Plur":
            morphs.append(definite + "." + number)
        morphs.append(case)
    else:
        if definite == "Def":
            morphs.append(definite + "." + number)

        if case in loc: # animate locative declension
            morphs.append("Gen")
            morphs.append("GAN")
        morphs.append(case)
    
    return morphs

    # TODO: Case endings in corpus don't match http://www.languagesgulper.com/eng/Basque_language.html well
    # TODO: -ko / -go suffix is frequently in corpus but not labelled

