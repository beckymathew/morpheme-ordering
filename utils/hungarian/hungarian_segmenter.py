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

    if label_dict.get("VerbForm") == "Inf":
        morphs.append("Inf")

    if label_dict.get("Voice") == "Cau":
        morphs.append("Cau")

    if label_dict.get("Tense") == "Past":
        morphs.append("Past")

    mood = label_dict.get("Mood")
    if mood in ["Cnd", "Pot"]: # conditional, subjunctive (only in present tense)
        morphs.append(mood)

    # As far as I can tell, there's no way to disentangle definiteness, person, and number
    definite = label_dict.get("Definite")
    person = label_dict.get("Person")
    number = label_dict.get("Number")
    if definite and person and number:
        morphs.append(definite + person + number)
    
    return morphs
    # TODO: 2po in Wikipedia doesn't show up in corpus
    # http://www.hungarianreference.com/Verbs/Causative-at-tat.aspx says causative + potential + conditional = could make do something
    # but mood that is both potential and conditional isn't attested in corpus