def get_abstract_morphemes(labels):
    """
    Takes a list of UD labels for a Finnish verb and returns a list of abstract morphemes.
    Parameters:
     - labels: A list of UD labels for a Finnish verb, such as 'Definite=Def|Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act'

    Returns:
     - A list of abstract morphemes in order. 
    """

    morphs = ["ROOT"]

    if len(labels) < 3:
        return morphs

    # creating dictionary from labels string
    label_pairs = labels.split("|")
    label_dict = {}
    for pair in label_pairs:
        k, v = pair.split("=")
        label_dict[k] = v

    # derivation, plural, case, possessor person + number 
    derivation = label_dict.get("Derivation")
    number = label_dict.get("Number")
    case = label_dict.get("Case")
    person_psor = label_dict.get("Person[psor]")
    number_psor = label_dict.get("Number[psor]")

    if derivation: morphs.append("Derivation")
    if number == "Plur": morphs.append("Number") # only plural is marked
    if case not in [None, "Nom"]: morphs.append("Case") # nominative is unmarked
    if person_psor:
        morphs.append("Possessor")
            
    return morphs

# Derivation: https://universaldependencies.org/fi/feat/Derivation.html. Even though it's labeled, it's part of the lemma form. 
# I think it would be accurate to either include the derivation (so it's like verb + derivation = noun) or not include the derivation (just deal with root noun).
# I'm including derivation here, but it would make sense to not have it also. 
