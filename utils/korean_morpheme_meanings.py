# based on matchedAllomorphs.tsv
morpheme_slots = {
    "jp_이": "DERIVATION", # predicative maker
    "ep_으시": "HONORIFIC",
    "ef_십시오": "HONORIFIC", # honorific formal polite imperative https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_세요": "HONORIFIC", # honorific informal polite imperative
    "ef_세": "HONORIFIC",
    "ef_으리오": "VALENCY", # passative / causative https://en.wiktionary.org/wiki/%EB%A6%AC
    "ef_리오": "VALENCY", # passative / causastive https://en.wiktionary.org/wiki/%EB%A6%AC
    "ef_ㄹ세": "TENSE/ASPECT", # not certain about this, but -l usually means future tense and -se usually involves an honorific
    "ef_ㄹ걸": "TENSE/ASPECT", # future tense -l
    "ef_ㄹ지어다": "TENSE/ASPECT", # future tense -l
    "ef_지어다": "PRAGMATICMOOD", # https://www.reddit.com/r/Korean/comments/di3d8z/help_me_understand_the_ending_%EC%9D%84%EC%A7%80%EC%96%B4%EB%8B%A4_please/
    "ef_ㄹ지": "TENSE/ASPECT", # future tense -l
    "ef_ㄹ지라": "TENSE/ASPECT", # future tense -l
    "ef_ㄹ쏘냐": "TENSE/ASPECT", # future tense -l
    "ef_쏘냐": "PRAGMATICMOOD", # interrogative https://www.reddit.com/r/Korean/comments/aqytjr/what_does_%EB%91%90%EB%A0%A4%EC%9A%B8%EC%86%8C%EB%83%90_consist_of/
    "ef_ㄹ지어라": "TENSE/ASPECT", # future tense -l
    "ef_ㄹ텐데": "TENSE/ASPECT", # future tense -l
    "ef_텐데": "PRAGMATICMOOD", # expresses uncertainty and regret https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-92-100/lesson-100/
    "ef_읍시다": "FORMALITY", # -eub is formal
    "ef_ㅂ디다": "FORMALITY", # -b is formal
    "ef_ㅂ시다": "FORMALITY", # -b is formal
    "ef_ㅂ니까": "FORMALITY", # -b is formal, -kka is interrogative
    "ef_ㅂ니다": "FORMALITY", # -b is formal
    "ef_습니다": "FORMALITY", # -seub is formal
    "ef_ㅂ시요": "FORMALITY", # -b is formal
    "ef_ㅂ시오": "FORMALITY", # -b is formal
    "ef_습니까": "FORMALITY", # -seub is formal, -kka is interrogative
    "ef_입니다": "FORMALITY", # formal "to be"
    "ep_시": "SYNTACTICMOOD", # usually subjunctive, but sometimes is HONORIFIC
    "ep_더": "SYNTACTICMOOD",
    "ef_리": "SYNTACTICMOOD", # "I guess..." https://en.wiktionary.org/wiki/%EB%A6%AC
    "ef_으리": "SYNTACTICMOOD", # "I guess..." https://en.wiktionary.org/wiki/%EB%A6%AC 
    "ef_으리라": "SYNTACTICMOOD", # ^
    "ef_리라": "SYNTACTICMOOD", # ^
    "ef_니": "SYNTACTICMOOD", # allomorph of indicative
    "ef_시오": "SYNTACTICMOOD", # subjunctive formal polite -si + imperative -o
    "ef_더군": "SYNTACTICMOOD", # allomorph of imperfective -deon, mirative -gun
    "ef_는군": "SYNTACTICMOOD", # indicative -neun, mirative -gun
    "ef_는가": "SYNTACTICMOOD", # indicative -neun
    "ef_ㄴ가": "SYNTACTICMOOD", # indicative -n
    "ef_ㄴ다": "SYNTACTICMOOD", # indicative -n, declarative -da
    "ef_는다": "SYNTACTICMOOD", # indicative -neun, declarative -da
    "ef_ㄴ지": "SYNTACTICMOOD", # indicative -n, of course / biased questions -ji
    "ef_는지": "SYNTACTICMOOD", # indicative -neun, of course / biased questions -ji
    "ef_던가": "SYNTACTICMOOD", # retrospective / imperfective -deon with interrogative https://www.howtostudykorean.com/unit-5/unit-5-lessons-117-125/lesson-117/#1171
    "ef_는구나": "SYNTACTICMOOD", # indicative -neun
    "ef_ㄴ걸": "SYNTACTICMOOD", # indicative -n
    "ef_ㄴ데": "SYNTACTICMOOD", # indicative -n, contrast connector -de
    "ef_는지요": "SYNTACTICMOOD", # indicative -neun, of course / biased question -ji, polite -yo
    "ef_ㄴ데요": "SYNTACTICMOOD", # indicative -n, contrast connector -de, polite -yo
    "ef_는단다": "SYNTACTICMOOD", # indicative -neun
    "ef_ㄴ지라": "SYNTACTICMOOD", # indicative -n
    "ef_ㄴ거지": "SYNTACTICMOOD", # indicative -n
    "ef_오": "PRAGMATICMOOD", # imperative
    "ef_아라": "PRAGMATICMOOD",	# allomorph of 어라
    "ef_어라": "PRAGMATICMOOD",
    "ef_라": "PRAGMATICMOOD", # imperative
    "ef_으라": "PRAGMATICMOOD", # imperative
    "ef_을까": "PRAGMATICMOOD", # interrogative, https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635 
    "ef_느냐": "PRAGMATICMOOD", # interrogative formal non-polite (table in https://en.wiktionary.org/wiki/%EC%9E%88%EB%8B%A4)
    "ef_어": "PRAGMATICMOOD", # indicative informal non-polite
    "ef_어요": "PRAGMATICMOOD", # indicative informal polite
    "ef_다": "PRAGMATICMOOD", # declarative -da
    "ef_다.": "PRAGMATICMOOD", # a typo, declarative -da
    "ef_에": "PRAGMATICMOOD",
    "ef_에요": "PRAGMATICMOOD", # polite -yo
    "ef_구나": "PRAGMATICMOOD", # something like a mirative, "Oh I just realized that..." https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-76-83/lesson-82-2/#921
    "ef_군": "PRAGMATICMOOD", # ^ same mirative
    "ef_군요": "PRAGMATICMOOD", # ^ same mirative with polite -yo
    "ef_라고": "PRAGMATICMOOD", # quotative
    "ef_라구": "PRAGMATICMOOD", # quotative
    "ef_라니": "PRAGMATICMOOD", # contraction of quotative
    "ef_자": "PRAGMATICMOOD",
    "ef_냐": "PRAGMATICMOOD", # interrogative
    "ef_소": "PRAGMATICMOOD", # declarative from outdated haoche style https://blog.lingodeer.com/the-definitive-guide-to-korean-speech-levels/
    "ef_ㄹ까": "PRAGMATICMOOD", # interrogative "Should I do this for you?" https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635
    "ef_ㄹ까요": "PRAGMATICMOOD", # interrogative -lkka, polite -yo
    "ef_지": "PRAGMATICMOOD", # something like "of course" or a biased question
    "ef_죠": "PRAGMATICMOOD", # same as -ji with -yo polite
    "ef_지요": "PRAGMATICMOOD", # same as ^ -jyo
    "ef_나": "PRAGMATICMOOD", # casual interrogative https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjT1NPEj9DqAhXEGc0KHVZaDbsQFjAAegQIBhAB&url=https%3A%2F%2Fgobillykorean.com%2Fshop%2FFile%2Fget%2F%3Ffile%3DGo_Billy_Korean_Episode_28.pdf&usg=AOvVaw1Q1-UDawtJGqrhJ62jjstX
    "ef_어야지": "PRAGMATICMOOD", # one should do something
    "ef_지마라": "PRAGMATICMOOD", # negative imperative
    "ef_리요": "PRAGMATICMOOD", # imperative (but an older style)
    "ef_답니다": "PRAGMATICMOOD", # something like a quotative? https://forum.wordreference.com/threads/%EB%8B%B5%EB%8B%88%EB%8B%A4.2253519/
    "jxf_요": "POLITE",
    "ef_요": "POLITE",
    "ef_니까": "CONNECTOR", # formal polite cause/reason -nikka https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_으니까": "CONNECTOR", # formal polite cause/reason -eunikka
    "ef_니까요": "CONNECTOR", # formal polite cause/reason -nikka, polite -yo
    "ef_으니까요": "CONNECTOR", # formal polite cause/reason -eunikka, polite -yo
    "ef_고": "CONNECTOR", 
    "ef_구": "CONNECTOR", # can't tell what this is, some people say it's a different way to write -go
    "ef_야": "CONNECTOR", # condition connective form, https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_데": "CONNECTOR", # contrast connective form https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_랴": "CONNECTOR", # https://krdict.korean.go.kr/eng/dicSearch/SearchView?divSearch=defViewGlobal&ParaWordNo=80306&nationCode=6&ParaNationCode=6&nation=eng&captchaNumber=&comment_user_name=&commentTitle=&wordComment=&viewTypes=on 
    "ef_으랴": "CONNECTOR", # https://krdict.korean.go.kr/eng/dicSearch/SearchView?divSearch=defViewGlobal&ParaWordNo=80306&nationCode=6&ParaNationCode=6&nation=eng&captchaNumber=&comment_user_name=&commentTitle=&wordComment=&viewTypes=on 
    "ef_옵니다": "AUXILIARY", # formal indicative "to come" (not a suffix, it's a new verb)
    "ef_걸": "DERIVATION" # contraction of gos-eul which turns a verb into a noun, https://forum.wordreference.com/threads/%EB%8A%94-%EA%B1%B8.1999585/
}

# ef: Final ending marker. SLOTS: V, VI, VII
"""
아	ef	4	[('아', 'ef')]
아야지	ef	2	[('아야지', 'ef')]
다니	ef	1	[('다니', 'ef')]
지라	ef	2	[('지라', 'ef'), ('으지라', 'ef')]
다더라	ef	1	[('다더라', 'ef')]
냐고	ef	2	[('으냐고', 'ef'), ('냐고', 'ef')]
너라	ef	1	[('너라', 'ef')]
나다	ef	1	[('나다', 'ef')]
대서야	ef	1	[('대서야', 'ef')]
옵소서	ef	2	[('옵소서', 'ef')]
노라	ef	3	[('노라', 'ef')]
구려	ef	1	[('구려', 'ef')]
랍니다	ef	2	[('랍니다', 'ef')]
라나	ef	1	[('라나', 'ef')]
로다	ef	2	[('로다', 'ef')]
란다	ef	2	[('란다', 'ef')]
여	ef	2	[('여', 'ef')]
외다	ef	2	[('외다', 'ef')]
예요	ef	2	[('예요', 'ef')]
이요	ef	1	[('이요', 'ef')]
이랴	ef	1	[('이랴', 'ef')]
든가	ef	1	[('든가', 'ef')]
지예	ef	1	[('지예', 'ef')]
다면	ef	1	[('다면', 'ef')]
거든	ef	4	[('거든', 'ef')]
라네	ef	3	[('라네', 'ef')]
인가	ef	1	[('인가', 'ef')]
긴	ef	1	[('긴', 'ef')]
다네	ef	4	[('다네', 'ef')]
네	ef	3	[('네', 'ef')]
단다	ef	1	[('단다', 'ef')]
"""

def automatic_morpheme_meaning(grapheme, label):
    slots = []
    politeFlag = False

    if grapheme[-1] == "요": # This should always be last
        politeFlag = True
        grapheme = grapheme[:-1]

    if grapheme:
        if grapheme[0] == "으": # allomorph, epenthetic vowel
            grapheme = grapheme[1:]

        if grapheme[0] == "ㅂ" or grapheme[0] == "습" or grapheme[0] == "읍":
            slots.append("FORMALITY")
            grapheme = grapheme[1:]

        if "FORMALITY" in slots and grapheme == "니까": # this is an interrogative after a formal, otherwise cause/reason
            slots.append("PRAGMATICMOOD")
            grapheme = ""

        if label == "ef" and grapheme:
            if grapheme[0] == "ㄹ": # future tense TODO: this looks like it's not always future
                slots.append("TENSE/ASPECT")
                grapheme = grapheme[1:]
            if grapheme[0] == "ㄴ" or grapheme[0] == "는": # indicative
                slots.append("SYNTACTICMOOD")
                grapheme = grapheme[1:]
                if grapheme == "지": # indicative + ji turns a verb into a noun-like clause https://www.howtostudykorean.com/unit-2-lower-intermediate-korean-grammar/unit-2-lessons-26-33/lesson-30/
                    slots.append("DERIVATION")
                    grapheme = ""
                    
        ret = morpheme_slots.get(label + "_" + grapheme)
        if ret == None: 
            if label == "px": # auxiliary verb
                slots.append("AUXILIARY")
            elif grapheme == "있" or grapheme == "없": # to have / not have, used to modify a main verb
                slots.append("AUXILIARY")
            elif label == "pvg" or label == "paa": # general verb or attributive adjective
                slots.append("ROOT") # TODO: why would a root appear later in an affix chain
            elif label ==  "xsn" or label == "xsm": # noun derivational suffix or adjective derivational suffix
                # not technically the root, but probably part of a noun / adj root that got turned into a verb
                slots.append("DERIVATION")
            elif label == "xsv": # verb derivational suffix
                slots.append("VALENCY")
            elif label == "etm" or label == "etn": # adnominalizer or nominalizer
                slots.append("SYNTACTICMOOD")
            elif label == "ep": # pre-final ending marker, usually tense/aspect or honorific (in dictionary)
                slots.append("TENSE/ASPECT")
            elif label == "jcr": # quotative case particle
                slots.append("PRAGMATICMOOD")
            elif label == "jca": # adverbial case particle (looks like mostly locative or instrumental)
                slots.append("PRAGMATICMOOD")
            elif label == "jxc": # common auxiliary (looks like "only", "until", "up to")
                slots.append("PRAGMATICMOOD")
            elif label == "ecc" or label == "ecs" or label == "ecx": # coordinate conjunction, conjunctive ending, auxiliary conjunction
                slots.append("CONNECTOR")
            else:
                slots.append("UNKNOWN")
        else:
            slots.append(ret) # label from dictionary morpheme_slots

        grapheme = ""
        if label + "_" + grapheme in morpheme_slots:
            slots.append(morpheme_slots[label + "_" + grapheme])
            grapheme = ""

        if politeFlag: # This should always be last
            slots.append("POLITE")
    
    return slots 

def morpheme_meaning(grapheme, label):
    ret = morpheme_slots.get(label + "_" + grapheme)
    if ret == None: 
        if label == "px": # auxiliary verb
            return "AUXILIARY"
        elif grapheme == "있" or grapheme == "없": # to have / not have, used to modify a main verb
            return "AUXILIARY"
        elif label == "pvg" or label == "paa": # general verb or attributive adjective
            return "ROOT"
        elif label ==  "xsn" or label == "xsm": # noun derivational suffix or adjective derivational suffix
            # not technically the root, but probably part of a noun / adj root that got turned into a verb
            return "ROOT"
        elif label == "xsv": # verb derivational suffix
            return "VALENCY"
        elif label == "etm" or label == "etn": # adnominalizer or nominalizer
            return "SYNTACTICMOOD"
        elif label == "ep": # pre-final ending marker, usually tense/aspect or honorific (in dictionary)
            return "TENSE/ASPECT"
        elif label == "jcr": # quotative case particle
            return "PRAGMATICMOOD"
        elif label == "jca": # adverbial case particle (looks like mostly locative or instrumental)
            return "PRAGMATICMOOD"
        elif label == "jxc": # common auxiliary (looks like "only", "until", "up to")
            return "PRAGMATICMOOD"
        elif label == "ecc" or label == "ecs" or label == "ecx": # coordinate conjunction, conjunctive ending, auxiliary conjunction
            return "CONNECTOR"
        else:
            return "UNKNOWN"
    else:
        return ret # label from dictionary morpheme_slots

### Notes ###
# - The corpus doesn't fully separate morphemes. In cases where a single morpheme from the corpus actually corresponds to multiple morphemes (like HONORIFIC + PAST), I've labeled it with the left-most morpheme's slot (HONORIFIC).

### Issues ###
# - doesn't make sense to me that case particles (usually for nouns) should indicate pragmatic mood
# - doesn't make sense that adnominalizers / nominalizers indicate syntactic mood -- they're changing a verb into a different category
#   - This doesn't matter if we're using verbsWithoutAdnominals