warningCache = set()


features = {}
features["Voice"] = "Voice"		
features["Gender"] = "Agr"		
features["Number"] = "Agr"		
features["Animacy"] = "Other"		
features["Clitic"] = "Emb"		
features["VerbForm"] = "Emb"		
features["InfForm"] = "Emb"		
features["PartForm"] = "Emb"		
features["Number[psor]"] = "Possessive"	
features["Person[psor]"] = "Possessive"	
features["Evident"] = "Evidential"	
features["Tense"] = "TAM"	
features["Mood"] = "TAM"	
features["VerbType"] = "TAM"	
features["Aspect"] = "TAM"	
features["Polite"] = "Politeness"
features["Polarity"] = "Polarity"	
features["Case"] = "Case"
features["Person"] = "Agr"
features["Degree"] = "Degree"
features["Connegative"] = "Connegative"
features["Style"] = "Style"
features["Abbr"] = "Abbr"
features["Typo"] = "Typo"
features["Derivation"] = "Other"
features["Definite"] = "Other"

from collections import defaultdict

def get_abstract_morphemes(labels, only=None):
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
        if pair == "_":
           continue
        try:
            k, v = pair.split("=")
        except ValueError:
           print("MORPH", pair, labels)
           assert False
        label_dict[k] = v

    morphs = ["ROOT"]

    perFeature = defaultdict(list)
    for key, val in label_dict.items():
        if key not in features and key not in warningCache:
           print(key)
           warningCache.add(key)
        perFeature[features.get(key, "Other")].append(key+"_"+val)
    for feat in sorted(list(perFeature)):
        if only is not None and feat != only:
          continue
        form = "|".join(sorted(perFeature[feat]))
        if form == "Polarity_Pos":
            continue
        if feat not in ["Voice", "Agr", "TAM"]:
            continue
        morphs.append(form)
#    print(morphs)
    return morphs

    # TODO: interrogative
    # Tense=Pqp? Seems to be indirect? Usually looks like mıştı but I don't know if it's mış+tı
    #   Pqp tense is miş-ti, which maybe could be broken down into Pqp+Past
    # Mood: Ind, Cnd, Imp, Pot, Gen, Opt, Des, DesPot, Nec
    #   Gen comes after TAM suffix ?
    #   Indicative is default?
    # Polite
    #   It looks informal is default, although I don't know why only some of the verbs have Polite labeled
