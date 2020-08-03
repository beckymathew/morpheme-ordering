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

    if label_dict.get("Number") == "Plur":
        morphs.append("Plur") # -lar-
        # Singular is void

    if label_dict.get("Number[psor]") and label_dict.get("Person[psor]"):
        morphs.append(label_dict.get("Person[psor]") + label_dict.get("Number[psor]") + "[psor]")
        # Theoretically, you could separate person and number except the 3pl doesn't match the pattern
        # Also, Plur + 3Plur[psor] seems to look the same as Sing + 3Plur[psor]

    case = label_dict.get("Case")
    if not case == "Nom": # absolute (nominative) case is void
        morphs.append(case)

    # Wikipedia says predicative suffixes may show up with person and number (https://en.wikipedia.org/wiki/Turkish_grammar#Nouns)
    # But the corpus only has Person=3 for all nouns

    return morphs