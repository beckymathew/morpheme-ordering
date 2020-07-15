{
    "ep_았": "",
    "jcr_고": "",
    "ecs_면": "",
    "px_지": "", # M2TA_064-s16, M2TA_064-s22, M2TA_064-s58 TODO: no idea...
    "ecx_게": "CAUSATIVE", # https://en.wiktionary.org/wiki/%EA%B2%8C etymology 6 -- causative / passive
    "paa_있": "", # TODO: can't find an example
    "etn_기": "DERIVATION", # nominalizer
    "ecx_지": "CONNECTOR", # used with ji + anhda / motha negation
    "nbn_수": "ABILITY", # exclusively used with verb + su + iss/eops-da pattern
    "ecx_고": "CONNECTOR", 
    "px_있"	"AUXILIARY", # sometimes used for progressive, ability/inability, etc
    "ef_ㄴ다": "DECLARATIVE", # plain present indicative for action verbs
    "ecs_어": "CONNECTOR", # https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/lessons-67-75/lesson-70/ TODO
    "ecx_어": "TENSE", # It's not exactly tense, but verbs must conjugate with -a or -o at the end in -a/-o/ya register TODO
    "etm_ㄹ": "DERIVATION", # adnominalizer (used with future tense? TODO)
    "jp_이": "VERB_DERIVATION", # predicative maker, appears earlier than other derivation slots
    "ep_ㅆ": "TENSE", # pre-final past tense marker
    "ef_다": "FINAL", # TODO
    "etm_ㄴ": "DERIVATION" # adnominalizer
}

# based on matchedAllomorphs.tsv
morpheme_slots = {
    "jp_이": "ROOT",
    "ep_으시": "HONORIFIC",
    "ef_십시오": "HONORIFIC", # honorific formal polite imperative https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_으리오": "VALENCY", # passative / causative https://en.wiktionary.org/wiki/%EB%A6%AC
    "ef_리오": "VALENCY", # passative / causastive https://en.wiktionary.org/wiki/%EB%A6%AC
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
    "ef_라고": "PRAGMATICMOOD", # quotative
    "ef_라구": "PRAGMATICMOOD", # quotative
    "ef_자": "PRAGMATICMOOD",
    "ef_냐": "PRAGMATICMOOD", # interrogative
    "ef_소": "PRAGMATICMOOD", # declarative from outdated haoche style https://blog.lingodeer.com/the-definitive-guide-to-korean-speech-levels/
    "ef_ㄹ까": "PRAGMATICMOOD", # interrogative "Should I do this for you?" https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635
    "ef_ㄹ까요": "PRAGMATICMOOD", # interrogative -lkka, polite -yo
    "ef_지": "PRAGMATICMOOD", # something like "of course" or a biased question
    "ef_죠": "PRAGMATICMOOD", # same as -ji with -yo polite
    "ef_지요": "PRAGMATICMOOD", # same as ^ -jyo
    "ef_나": "PRAGMATICMOOD", # casual interrogative https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjT1NPEj9DqAhXEGc0KHVZaDbsQFjAAegQIBhAB&url=https%3A%2F%2Fgobillykorean.com%2Fshop%2FFile%2Fget%2F%3Ffile%3DGo_Billy_Korean_Episode_28.pdf&usg=AOvVaw1Q1-UDawtJGqrhJ62jjstX
    "jxf_요": "POLITE",
    "ef_요": "POLITE",
    "ef_니까": "CONNECTOR", # formal polite cause/reason -nikka https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_으니까": "CONNECTOR", # formal polite cause/reason -eunikka
    "ef_니까요": "CONNECTOR", # formal polite cause/reason -nikka, polite -yo
    "ef_으니까요": "CONNECTOR", # formal polite cause/reason -eunikka, polite -yo
    "ef_고": "CONNECTOR", 
    "ef_구": "CONNECTOR", # can't tell what this is, some people say it's a different way to write -go
    "ef_야": "CONNECTOR", # condition connective form, https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_옵니다": "AUXILIARY" # formal indicative "to come" (not a suffix, it's a new verb)
}

# ef: Final ending marker. SLOTS: V, VI, VII
"""
아	ef	4	[('아', 'ef')]
아야지	ef	2	[('아야지', 'ef')]
는단다	ef	1	[('는단다', 'ef')]
다니	ef	1	[('다니', 'ef')]
ㄹ쏘냐	ef	1	[('ㄹ쏘냐', 'ef')]
지라	ef	2	[('지라', 'ef'), ('으지라', 'ef')]
다더라	ef	1	[('다더라', 'ef')]
냐고	ef	2	[('으냐고', 'ef'), ('냐고', 'ef')]
ㄹ지어다	ef	1	[('ㄹ지어다', 'ef')]
지마라	ef	1	[('지마라', 'ef')]
너라	ef	1	[('너라', 'ef')]
나다	ef	1	[('나다', 'ef')]
는구나	ef	1	[('는구나', 'ef')]
대서야	ef	1	[('대서야', 'ef')]
ㄹ지어라	ef	1	[('ㄹ지어라', 'ef')]
ㄹ걸	ef	2	[('ㄹ걸', 'ef')]
옵소서	ef	2	[('옵소서', 'ef')]
어야지	ef	4	[('어야지', 'ef')]
노라	ef	3	[('노라', 'ef')]
구려	ef	1	[('구려', 'ef')]
데	ef	1	[('데', 'ef')]
ㄹ세	ef	4	[('ㄹ세', 'ef')]
랍니다	ef	2	[('랍니다', 'ef')]
라나	ef	1	[('라나', 'ef')]
로다	ef	2	[('로다', 'ef')]
ㄴ데	ef	1	[('ㄴ데', 'ef')]
란다	ef	2	[('란다', 'ef')]
여	ef	2	[('여', 'ef')]
외다	ef	2	[('외다', 'ef')]
ㄹ텐데	ef	1	[('ㄹ텐데', 'ef')]
군요	ef	1	[('군요', 'ef')]
예요	ef	2	[('예요', 'ef')]
ㄴ걸	ef	1	[('ㄴ걸', 'ef')]
리요	ef	4	[('리요', 'ef')]
이요	ef	1	[('이요', 'ef')]
이랴	ef	1	[('이랴', 'ef')]
든가	ef	1	[('든가', 'ef')]
지예	ef	1	[('지예', 'ef')]
다면	ef	1	[('다면', 'ef')]
ㄴ데요	ef	1	[('ㄴ데요', 'ef')]
거든	ef	4	[('거든', 'ef')]
ㄹ지	ef	2	[('ㄹ지', 'ef')]
랴	ef	9	[('으랴', 'ef'), ('랴', 'ef')]
ㄴ지라	ef	2	[('ㄴ지라', 'ef')]
세요	ef	8	[('세요', 'ef')]
라네	ef	3	[('라네', 'ef')]
인가	ef	1	[('인가', 'ef')]
는지요	ef	3	[('는지요', 'ef')]
ㄹ지라	ef	1	[('ㄹ지라', 'ef')]
긴	ef	1	[('긴', 'ef')]
다네	ef	4	[('다네', 'ef')]
네	ef	3	[('네', 'ef')]
단다	ef	1	[('단다', 'ef')]
라니	ef	2	[('라니', 'ef')]
ㄴ거지	ef	1	[('ㄴ거지', 'ef')]
답니다	ef	6	[('답니다', 'ef')]
"""

def morpheme_meaning(grapheme, label):
    ret = morpheme_slots.get(label + "_" + grapheme)
    if ret == None: 
        if label == "px": # auxiliary verb
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