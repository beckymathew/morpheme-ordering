def get_abstract_morphemes(labels):
    """
    Takes the string of UD labels for a Hungarian noun and returns a list of abstract morphemes.
    Parameters:
     - labels: A string of UD labels for a Hungarian noun, such as 'Definite=Def|Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act'

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
        morphs.append("Number")

    psor_person = label_dict.get("Person[psor]")
    psor_number = label_dict.get("Number[psor]")
    if psor_person and not psor_person == "None" and psor_number and not psor_number =="None":
        morphs.append("Possessor")

    if label_dict.get("Number[psed]") and label_dict.get("Number[psed]") != "None":
        morphs.append("Possessed")

    case = label_dict.get("Case")

    if case and not case == "Nom":
        morphs.append("Case")

    return morphs
    # plural, possessor person, possessor number, case (other than nominative)
    # TODO: possessed number is almost always None
