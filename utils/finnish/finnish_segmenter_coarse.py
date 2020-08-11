def get_abstract_morphemes(labels):
    """
    Takes a list of UD labels for a Finnish verb and returns a list of abstract morphemes.
    Parameters:
     - labels: A list of UD labels for a Finnish verb, such as 'Definite=Def|Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act'

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

    verbform = label_dict.get("VerbForm")
    mood = label_dict.get("Mood")
    tense = label_dict.get("Tense")
    person = label_dict.get("Person")
    number = label_dict.get("Number")
    voice = label_dict.get("Voice")
    clitic = label_dict.get("Clitic")

    if voice not in ["Act", None]:
        morphs.append("Voice")

    if tense:
        morphs.append("Tense")

    if mood not in ["Ind", None]: 
        morphs.append("Mood")

    if person and number:
        morphs.append("Person.Number")
    
    if verbform not in ["Inf", None]: # TODO: not certain where to put this
        morphs.append("VerbForm")

    if clitic:
        morphs.append("Clitic")

    return morphs

# TODO: Is the Coll style different enough to affect the ordering?