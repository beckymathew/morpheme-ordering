from hangul_romanize import Transliter
from hangul_romanize.rule import academic 

transliter = Transliter(academic) # based on revised romanization

# each phoneme has a single character representation
our_romanization = {
    "eo": "O",
    "eu": "U",
    "ae": "E",
    "oe": "W", # originally the vowel /ø/ although sometimes (for younger speakers?) transcribed as /wɛ/ (according to Brown and Yoon "The Handbook of Korean Linguistics", 2015.)
    "ui": "i", # represents a dipthong of /ɨi/ at the beginnings of words, but /i/ elsewhere
    "yeo":"yO",
    "yae": "yE",
    "wae": "wE",
    "kk": "K",
    "tt": "T",
    "pp": "P",
    "jj": "J",
    "ch": "C",
    "ss": "S",
    "ng": "N",
    "r": "l" # allophones, although I think this transliter always uses "l"
}

# Common morphemes that are not full syllable blocks
letter_romanization = {
    "ㄹ": "l",
    "ㄴ": "n",
    "ㅆ": "S",
}

def romanize(word):
    """
    Phonemize a single (!) word in Hangul to a romanization where each phoneme corresponds to a single unique Latin alphabet letter. 
    
    Params:
     - word: a string representing a single word with no leading whitespace. May have unexpected results if the word string represents multiple words
    
    Returns:
     - string representing our romanization of the Hangul word. 

    Bugs:
     - The hangul_romanize Transliter only handles well-formed syllable blocks like 말, and cannot handle standalone letters like ㅁ ㅏ ㄹ
    """
    # separating each character, mostly to avoid potential romanization issues
    # such as 네옹 ne-ong and 넝 neong
    word = list(word)
    original_romanized = []
    for char in word:
        original_romanized.append(transliter.translit(char))
    
    our_romanized = ""
    for i, char in enumerate(original_romanized):
        for original, ours in our_romanization.items():
            if i == 0 and original == "ui": # see footnote, this only works if word is a single word and not a string of words
                char = char.replace(original, "Ui")
            else: 
                if len(char) == 1: # check if it's a single Hangul character
                    if char in letter_romanization:
                        char = letter_romanization[char]
                char = char.replace(original, ours) # normal syllable block
        our_romanized += char
    return our_romanized
        
# The vowel 의 is pronounced as /ɨi/ word-initially, as /ɛ/ when it is a possessive suffix, and as /i/ everywhere else.
# Just based on a word, it's not easy to tell whether it's a possessive suffix or not, so I only considered the /ɨi/ and /i/ cases. 
# This is according to Choo and Grady "The Sounds of Korean", 2003. 