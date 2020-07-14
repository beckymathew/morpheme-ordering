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
    "ef_읍시다": "FORMALITY", # -eub is formal
    "ef_ㅂ디다": "FORMALITY", # -b is formal
    "ef_ㅂ시다": "FORMALITY", # -b is formal
    "ef_ㅂ니까": "FORMALITY", # -b is formal, -kka is interrogative
    "ef_ㅂ니다": "FORMALITY", # -b is formal
    "ef_습니다": "FORMALITY", # -seub is formal
    "ef_ㅂ시요": "FORMALITY", # -b is formal
    "ef_ㅂ시오": "FORMALITY", # -b is formal
    "ef_습니까": "FORMALITY", # -seub is formal, -kka is interrogative
    "ep_시": "SYNTACTICMOOD", # usually subjunctive, but sometimes is HONORIFIC
    "ep_더": "SYNTACTICMOOD",
    "ef_오": "PRAGMATICMOOD", # imperative
    "ef_아라": "PRAGMATICMOOD",	# allomorph of 어라
    "ef_어라": "PRAGMATICMOOD",
    "ef_라": "PRAGMATICMOOD", # imperative
    "ef_으라": "PRAGMATICMOOD", # imperative
    "ef_을까": "PRAGMATICMOOD", # interrogative, https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635 
    "ef_느냐": "PRAGMATICMOOD", # interrogative formal non-polite (table in https://en.wiktionary.org/wiki/%EC%9E%88%EB%8B%A4)
    "ef_어": "PRAGMATICMOOD", # indicative informal non-polite
    "ef_어요": "PRAGMATICMOOD", # indicative informal polite
    "ef_다": "PRAGMATICMOOD",
    "ef_에요", "PRAGMATICMOOD", # polite -yo
    "jxf_요": "POLITE",
    "ef_요": "POLITE",
    "ef_니까": "CONNECTOR", # connector -(eu)ni, interrogative -kka
    "ef_으니까": "CONNECTOR"
}

# ef: Final ending marker. SLOTS: V, VI, VII
더군	ef	1	[('더군', 'ef')]
리	ef	2	[('리', 'ef'), ('으리', 'ef')]
리오	ef	1	[('으리오', 'ef')]
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
시오	ef	1	[('시오', 'ef')]
는구나	ef	1	[('는구나', 'ef')]
대서야	ef	1	[('대서야', 'ef')]
옵니다	ef	1	[('옵니다', 'ef')]
는군	ef	2	[('는군', 'ef')]
ㄹ지어라	ef	1	[('ㄹ지어라', 'ef')]
ㄹ걸	ef	2	[('ㄹ걸', 'ef')]
옵소서	ef	2	[('옵소서', 'ef')]
어야지	ef	4	[('어야지', 'ef')]
노라	ef	3	[('노라', 'ef')]
구려	ef	1	[('구려', 'ef')]
데	ef	1	[('데', 'ef')]
라고	ef	2	[('라고', 'ef')]
구	ef	1	[('구', 'ef')]
ㄹ세	ef	4	[('ㄹ세', 'ef')]
랍니다	ef	2	[('랍니다', 'ef')]
니	ef	3	[('니', 'ef')]	Allomorph of Indicative (SLOT V)
야	ef	15	[('야', 'ef')]
라나	ef	1	[('라나', 'ef')]
고	ef	1	[('고', 'ef')]
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
니까요	ef	4	[('니까요', 'ef'), ('으니까요', 'ef')]
이요	ef	1	[('이요', 'ef')]
에요	ef	8	[('에요', 'ef')]
ㄹ까요	ef	2	[('ㄹ까요', 'ef')]
이랴	ef	1	[('이랴', 'ef')]
입니다	ef	1	[('입니다', 'ef')]
든가	ef	1	[('든가', 'ef')]
지예	ef	1	[('지예', 'ef')]
라구	ef	1	[('라구', 'ef')]
에	ef	1	[('에', 'ef')]	SLOT VI
다.	ef	1	[('다.', 'ef')]
다면	ef	1	[('다면', 'ef')]
ㄴ데요	ef	1	[('ㄴ데요', 'ef')]
거든	ef	4	[('거든', 'ef')]
ㄹ지	ef	2	[('ㄹ지', 'ef')]
랴	ef	9	[('으랴', 'ef'), ('랴', 'ef')]
ㄴ지라	ef	2	[('ㄴ지라', 'ef')]
는지	ef	12	[('는지', 'ef')]
세요	ef	8	[('세요', 'ef')]
냐	ef	17	[('냐', 'ef')]
라네	ef	3	[('라네', 'ef')]
인가	ef	1	[('인가', 'ef')]
는지요	ef	3	[('는지요', 'ef')]
ㄹ지라	ef	1	[('ㄹ지라', 'ef')]
긴	ef	1	[('긴', 'ef')]
는다	ef	318	[('는다', 'ef')]
다네	ef	4	[('다네', 'ef')]
ㄴ가	ef	214	[('ㄴ가', 'ef')]
리라	ef	42	[('리라', 'ef'), ('으리라', 'ef')]
ㄴ지	ef	23	[('ㄴ지', 'ef')]
십시오	ef	5	[('십시오', 'ef')]
네	ef	3	[('네', 'ef')]
는가	ef	128	[('는가', 'ef')]
소	ef	153	[('소', 'ef')]
나	ef	10	[('나', 'ef')]
단다	ef	1	[('단다', 'ef')]
라니	ef	2	[('라니', 'ef')]
던가	ef	11	[('던가', 'ef')]
구나	ef	7	[('구나', 'ef')]
죠	ef	28	[('죠', 'ef')]
지요	ef	11	[('지요', 'ef')]
ㄴ거지	ef	1	[('ㄴ거지', 'ef')]
군	ef	12	[('군', 'ef')]
ㄹ까	ef	145	[('ㄹ까', 'ef')]
지	ef	68	[('지', 'ef')]	https://en.wiktionary.org/wiki/%EC%A7%80#Suffix
답니다	ef	6	[('답니다', 'ef')]
ㄴ다	ef	3328	[('ㄴ다', 'ef')]
자	ef	122	[('자', 'ef')]	SLOT VI

def morpheme_meaning(grapheme, label):
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

### Notes ###
# - The corpus doesn't fully separate morphemes. In cases where a single morpheme from the corpus actually corresponds to multiple morphemes (like HONORIFIC + PAST), I've labeled it with the left-most morpheme's slot (HONORIFIC).

### Issues ###
# - doesn't make sense to me that case particles (usually for nouns) should indicate pragmatic mood
# - doesn't make sense that adnominalizers / nominalizers indicate syntactic mood -- they're changing a verb into a different category