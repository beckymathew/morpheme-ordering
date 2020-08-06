def get_abstract_morphemes(labels_list):
    """
    Takes a string of UD labels for a Basque verb (with auxiliary) and returns a list of abstract morphemes.
    Parameters:
     - labels: A string of UD labels for a Basque verb, such as 'Definite=Def|Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act'

    Returns:
     - A list of abstract morphemes in order. 
    """

    label_pairs = labels.split("|")
    label_dict = {}
    for pair in label_pairs:
        k, v = pair.split("=")
        label_dict[k] = v\
    
    prefixes = []
    suffixes = ["ROOT"]

    verbform = label_dict.get("VerbForm")
    aspect = label_dict.get("Aspect")

    if verbform == "Part":
        if not aspect == "Perf": # perfective participle is exactly the root
            suffixes.append(aspect) 
    else:
        pass
    
    return prefixes, suffixes

    # TODO: why is there infm on non-2nd person?

    # TODO: Basque participle form uses a circumfix https://en.wikipedia.org/wiki/Basque_verbs
    # "The participle is generally obtained from the basic stem by prefixing e- or i- (there is no rule; if the stem begins with a vowel, j- is prefixed instead), and suffixing -i (to stems ending in a consonant) or -n (to stems ending in a vowel). Occasionally there is no suffix"