# based on matchedAllomorphs.tsv
morpheme_slots = {
    "jp_이": "DERIVATION_predicative", # predicative maker
    "ep_으시": "HONORIFIC_???",
    "ef_십시오": "HONORIFIC_formal_polite+imperative_오", # honorific formal polite imperative https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation -si-psio where -si- is honorific, -psio is sentence-final imperative
    "ef_세요": "HONORIFIC_informal_polite_imperative/nonpast_seyo", # honorific informal polite imperative
    "ef_세": "HONORIFIC_???",
    "ef_으리오": "VALENCY_passive/causative_ri", # passative / causative https://en.wiktionary.org/wiki/%EB%A6%AC (barely occurs in the corpus)
    "ef_리오": "VALENCY_passive/causative_ri", # passative / causastive https://en.wiktionary.org/wiki/%EB%A6%AC (barely occurs in the corpus)
    "ef_ㄹ세": "TENSE/ASPECT_???", # not certain about this, but -l usually means future tense and -se usually involves an honorific
    "ef_ㄹ걸": "TENSE/ASPECT_l+?_???", # future tense -l
    "ef_ㄹ지어다": "TENSE/ASPECT_???", # future tense -l
    "ef_지어다": "PRAGMATICMOOD_지어다", # https://www.reddit.com/r/Korean/comments/di3d8z/help_me_understand_the_ending_%EC%9D%84%EC%A7%80%EC%96%B4%EB%8B%A4_please/
    "ef_ㄹ지": "TENSE/ASPECT_l+PRAGMATICMOOD_ji", # future tense -l
    "ef_ㄹ지라": "TENSE/ASPECT_l+?_???", # future tense -l
    "ef_ㄹ쏘냐": "TENSE/ASPECT_l+?_???", # future tense -l
    "ef_쏘냐": "PRAGMATICMOOD", # interrogative https://www.reddit.com/r/Korean/comments/aqytjr/what_does_%EB%91%90%EB%A0%A4%EC%9A%B8%EC%86%8C%EB%83%90_consist_of/
    "ef_ㄹ지어라": "TENSE/ASPECT_l+?_???", # future tense -l
    "ef_ㄹ텐데": "TENSE/ASPECT_l+?_???", # future tense -l
    "ef_텐데": "PRAGMATICMOOD_텐데", # expresses uncertainty and regret https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-92-100/lesson-100/
    "ef_읍시다": "FORMALITY_formal_p+?_???_hortative_formal_polite_sida", # -eub is formal
    "ef_ㅂ디다": "FORMALITY_p+?_???", # -b is formal
    "ef_ㅂ시다": "FORMALITY_formal_polite_p+?_???_hortative_formal_polite_sida", # -b is formal
    "ef_ㅂ니까": "FORMALITY_formal_polite_p+SYNTACTICMOOD_formal_polite_ni+PRAGMATICMOOD_interrogative_kka", # -b is formal, -kka is interrogative
    "ef_ㅂ니다": "FORMALITY_formal_polite_p+?_???_indicative_formal_polite_nida", # -b is formal
    "ef_습니다": "FORMALITY_formal_polite_past_p+?_???_indicative_formal_polite_nida", # -seub is formal
    "ef_ㅂ시요": "FORMALITY_p+?_???", # -b is formal
    "ef_ㅂ시오": "FORMALITY_p+?_???", # -b is formal
    "ef_습니까": "FORMALITY_formal_polite_p+SYNTACTICMOOD_formal_polite_ni+PRAGMATICMOOD_interrogative_kka", # -seub is formal, -kka is interrogative
    "ef_입니다": "FORMALITY_p+?_???", # formal "to be"
    "ep_시": "SYNTACTICMOOD_subjunctive_Or_honorific_시", # usually subjunctive, but sometimes is HONORIFIC
    "ep_더": "SYNTACTICMOOD_???",
    "ef_리": "SYNTACTICMOOD_I_guess_ri", # "I guess..." https://en.wiktionary.org/wiki/%EB%A6%AC
    "ef_으리": "SYNTACTICMOOD_I_guess_ri", # "I guess..." https://en.wiktionary.org/wiki/%EB%A6%AC 
    "ef_으리라": "SYNTACTICMOOD_I_guess_ri+PRAGMATICMOOD_ra", # https://en.wiktionary.org/wiki/%EB%9D%BC Etymology 6
    "ef_리라": "SYNTACTICMOOD_I_guess_ri+PRAGMATICMOOD_ra", # https://en.wiktionary.org/wiki/%EB%9D%BC
    "ef_니": "SYNTACTICMOOD_indicative_n", # allomorph of indicative
    "ef_시오": "SYNTACTICMOOD_subjunctive_formal_polite_si+PRAGMATICMOOD_imperative_오", # subjunctive formal polite -si + imperative -o
    "ef_더군": "SYNTACTICMOOD_imperfective_deon+PRAGMATICMOOD_mirative_gun", # allomorph of imperfective -deon, mirative -gun
    "ef_는군": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_mirative_gun", # indicative -neun, mirative -gun
    "ef_는가": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_interrogative_ga", # indicative -neun
    "ef_ㄴ가": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_interrogative_ga", # indicative -n
    "ef_ㄴ다": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_declarative_da", # indicative -n, declarative -da
    "ef_는다": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_declarative_da", # indicative -neun, declarative -da
#    "ef_ㄴ지": "SYNTACTICMOOD", # indicative -n, of course / biased questions -ji
#    "ef_는지": "SYNTACTICMOOD", # indicative -neun, of course / biased questions -ji
    "ef_던가": "SYNTACTICMOOD_imperative_deon+PRAGMATICMOOD_interrogative_ka", # retrospective / imperfective -deon with interrogative https://www.howtostudykorean.com/unit-5/unit-5-lessons-117-125/lesson-117/#1171
#    "ef_는구나": "SYNTACTICMOOD", # indicative -neun
#    "ef_ㄴ걸": "SYNTACTICMOOD", # indicative -n
    "ef_ㄴ데": "SYNTACTICMOOD_indicative_n+CONNECTOR_connector_de", # indicative -n, contrast connector -de
    "ef_는지요": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_ji+POLITE_polite_yo", # indicative -neun, of course / biased question -ji, polite -yo
    "ef_ㄴ데요": "SYNTACTICMOOD_indicative_n+CONNECTOR_contrast_connector_de+POLITE_polite_yo", # indicative -n, contrast connector -de, polite -yo
    "ef_는단다": "SYNTACTICMOOD_indicative_n+?_?", # indicative -neun
    "ef_ㄴ지라": "SYNTACTICMOOD_indicative_n+?_?", # indicative -n
    "ef_ㄴ거지": "SYNTACTICMOOD_indicative_n+?_?", # indicative -n
    "ef_오": "PRAGMATICMOOD_imperative_오", # imperative
    "ef_아라": "PRAGMATICMOOD_imperative_eora/ara",	# allomorph of 어라. https://en.wiktionary.org/wiki/%EC%95%84%EB%9D%BC https://en.wiktionary.org/wiki/%EC%96%B4%EB%9D%BC
    "ef_어라": "PRAGMATICMOOD_imperative_eora/ara",
    "ef_라": "PRAGMATICMOOD_plain-declarative/imperative_ra", # imperative
    "ef_으라": "PRAGMATICMOOD_plain-declarative/imperative_era", # imperative
    "ef_을까": "PRAGMATICMOOD_inquisitive_eulkka", # interrogative, https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635 https://en.wiktionary.org/wiki/%EC%9D%84%EA%B9%8C
    "ef_느냐": "PRAGMATICMOOD_formal_polite_interrogative_nopast_neunya", # interrogative formal non-polite (table in https://en.wiktionary.org/wiki/%EC%9E%88%EB%8B%A4)
    "ef_어": "PRAGMATICMOOD_indicative_informal_nonpolite", # indicative informal non-polite
    "ef_어요": "PRAGMATICMOOD_indicative_informal_polite", # indicative informal polite
    "ef_다": "PRAGMATICMOOD_declarative_da", # declarative -da
    "ef_다.": "PRAGMATICMOOD_declarative_da", # a typo, declarative -da
    "ef_에": "PRAGMATICMOOD_e",
#    "ef_에요": "PRAGMATICMOOD", # polite -yo
    "ef_구나": "PRAGMATICMOOD_mirative_gun", # something like a mirative, "Oh I just realized that..." https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-76-83/lesson-82-2/#921
    "ef_군": "PRAGMATICMOOD_mirative_gun", # ^ same mirative
#    "ef_군요": "mirative+polite_yo", # ^ same mirative with polite -yo
    "ef_라고": "PRAGMATICMOOD_quotative", # quotative
    "ef_라구": "PRAGMATICMOOD_quotative", # quotative
    "ef_라니": "PRAGMATICMOOD_quotative", # contraction of quotative
    "ef_자": "PRAGMATICMOOD_hortative_자", # # Slot VI
    "ef_냐": "PRAGMATICMOOD_formal_nonpolite_interrogative_nya", # interrogative
    "ef_소": "PRAGMATICMOOD_declarative_haoche_소", # declarative from outdated haoche style https://blog.lingodeer.com/the-definitive-guide-to-korean-speech-levels/
    "ef_ㄹ까": "PRAGMATICMOOD_interrogative_lkka", # interrogative "Should I do this for you?" https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635
    "ef_ㄹ까요": "PRAGMATICMOOD_interrogative_lkka+POLITE_polite_yo", # interrogative -lkka, polite -yo
    "ef_지": "PRAGMATICMOOD_ji", # something like "of course" or a biased question. Wikipedia: Casual
    "ef_죠": "PRAGMATICMOOD_ji+POLITE_polite_yo", # same as -ji with -yo polite
    "ef_지요": "PRAGMATICMOOD_of_course_ji+POLITE_polite_yo", # same as ^ -jyo
    "ef_나": "PRAGMATICMOOD_causal_interrogative_na", # casual interrogative https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjT1NPEj9DqAhXEGc0KHVZaDbsQFjAAegQIBhAB&url=https%3A%2F%2Fgobillykorean.com%2Fshop%2FFile%2Fget%2F%3Ffile%3DGo_Billy_Korean_Episode_28.pdf&usg=AOvVaw1Q1-UDawtJGqrhJ62jjstX
    "ef_어야지": "PRAGMATICMOOD_one_should_do_something", # one should do something
    "ef_지마라": "PRAGMATICMOOD_negative_imperative", # negative imperative
    "ef_리요": "PRAGMATICMOOD_imperative_old_style", # imperative (but an older style)
    "ef_답니다": "PRAGMATICMOOD_답니다", # something like a quotative? https://forum.wordreference.com/threads/%EB%8B%B5%EB%8B%88%EB%8B%A4.2253519/
    "jxf_요": "POLITE_yo",
    "ef_요": "POLITE_yo",
    "ef_니까": "CONNECTOR_nikka", # formal polite cause/reason -nikka https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_으니까": "CONNECTOR_eunikka", # formal polite cause/reason -eunikka
    "ef_니까요": "CONNECTOR_nikka+POLITE_polite_yo", # formal polite cause/reason -nikka, polite -yo
    "ef_으니까요": "CONNECTOR_eunikka+POLITE_polite_yo", # formal polite cause/reason -eunikka, polite -yo
    "ef_고": "CONNECTOR_go", # https://en.wiktionary.org/wiki/%EA%B3%A0 
    "ef_구": "CONNECTOR_구", # can't tell what this is, some people say it's a different way to write -go
    "ef_야": "CONNECTOR_connective_condition_ya", # condition connective form, https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_데": "CONNECTOR_de", # contrast connective form https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_랴": "CONNECTOR_rya", # https://krdict.korean.go.kr/eng/dicSearch/SearchView?divSearch=defViewGlobal&ParaWordNo=80306&nationCode=6&ParaNationCode=6&nation=eng&captchaNumber=&comment_user_name=&commentTitle=&wordComment=&viewTypes=on 
    "ef_으랴": "CONNECTOR_rya", # https://krdict.korean.go.kr/eng/dicSearch/SearchView?divSearch=defViewGlobal&ParaWordNo=80306&nationCode=6&ParaNationCode=6&nation=eng&captchaNumber=&comment_user_name=&commentTitle=&wordComment=&viewTypes=on 
    "ef_옵니다": "AUXILIARY_옵니다", # formal indicative "to come" (not a suffix, it's a new verb)
    "ef_걸": "DERIVATION_nominalization_gos-eul", # contraction of gos-eul which turns a verb into a noun, https://forum.wordreference.com/threads/%EB%8A%94-%EA%B1%B8.1999585/
    "etn_기" : "SYNTACTICMOOD_nominalizer_informal_nonpilote_gi",
    "etn_ㅁ" : "SYNTACTICMOOD_nominalizer_formal_nonpolite_m",
    "ep_었었" : "TENSE/ASPECT_remote_past_었었",
    "ep_았었" : "TENSE/ASPECT_remote_past_었었",
    "ep_ㅆ었" : "TENSE/ASPECT_remote_past_었었",
    "ecx_려고" : "CONNECTOR_speaker_intention",
    "ecc_면서" : "CONNECTOR_conjunctive_myeonseo",
    "ecs_면서" : "CONNECTOR_conjunctive_meyonseo",
    "ecs_서" : "CONNECTOR_conjunctive_seo",
    "ecs_아서" : "CONNECTOR_conjunctive_aseo",
    "ecs_아야" : "CONNECTOR_conjunctive_aya",
    "ecs_어서" : "CONNECTOR_conjunctive_aseo",
    "ecs_어야" : "CONNECTOR_conjunctive_aya",
    "ecs_이" : "CONNECTOR_connector_i",
    "ef_ㄹ까" : "TENSE/ASPECT_ri+PRAGMATICMOOD_interrogative_kka",
    "ep_셨" : "HONORIFIC_honorific_s+TENSE/ASPECT_honorific_past_yeot", # portmanteau honorific (SLOT II) + past  (https://en.wikipedia.org/wiki/Korean_verbs)
    "ep_었겠" : "TENSE/ASPECT_remote_past/future_eossget",
    "ep_았겠" : "TENSE/ASPECT_remote_past/future_eossget", # SLOT III
    "ep_겠" : "TENSE/ASPECT_assertive",   # assertive (table in https://en.wiktionary.org/wiki/%EC%9E%88%EB%8B%A4) (SLOT III)
    "ep_ㅆ" : "TENSE/ASPECT_past",
    "xsv_되" : "VALENCY_되",
    "xsv_하" : "VALENCY_하",
    "xsn_뿐" : "DERIVATION_뿐",
    "xsn_들" : "DERIVATION_들",
    "xsm_하" : "DERIVATION_하",
    "xsm_스럽" : "DERIVATION_스럽",
    "jxc_부터" : "PRAGMATICMOOD_buteo", #https://en.wiktionary.org/wiki/%EB%B6%80%ED%84%B0
    "jxc_라도" : "PRAGMATICMOOD_rado", #https://en.wiktionary.org/wiki/%EB%9D%BC%EB%8F%84
    "jxc_도" : "PRAGMATICMOOD_do", # https://en.wiktionary.org/wiki/%EB%8F%84#Particle
    "jxc_까지" : "PRAGMATICMOOD_까지",
    "jcr_라고" : "PRAGMATICMOOD_rago", # https://en.wiktionary.org/wiki/%EB%9D%BC%EA%B3%A0#Suffix
    "jcr_고" : "PRAGMATICMOOD_go",
    "jca_에서" : "PRAGMATICMOOD_eseo", # https://en.wiktionary.org/wiki/%EC%97%90%EC%84%9C
    "jca_에" : "PRAGMATICMOOD_e",
    "jca_로"  : "PRAGMATICMOOD_ro", # "by" https://en.wiktionary.org/wiki/%EB%A1%9C#Particle
    "jca_로서"   : "PRAGMATICMOOD_roseo", # "by" according to Wiktionary
    "jca_로써"   : "PRAGMATICMOOD_rosseo",   # "by" according to Wiktionary
    "jca_보다"   : "PRAGMATICMOOD_boda", #https://en.wiktionary.org/wiki/%EB%B3%B4%EB%8B%A4#Particle
    "ef_소" : "PRAGMATICMOOD_소",
    "ep_어야겠" : "TENSE/ASPECT_tense/aspect_have-to-do",
    "ep_었더" : "TENSE/ASPECT_a-type-of-past",
    "ep_았" : "TENSE/ASPECT_past_eoss",
    "ep_았더" : "TENSE/ASPECT_past_...",
    "ep_아야겠" : "TENSE/ASPECT_need-to",
    "jxc_만" : "PRAGMATICMOOD_only",
    "ep_더" : "SYNTACTICMOOD_imperfective_deon", # Allomorph of -deon (SLOT V)
    "ef_ㄹ세" : "TENSE/ASPECT_???",
    "ecs_ㄴ다면" : "CONNECTOR_conditional_ㄴ다면",
    "ecs_니" : "CONNECTOR_and-then_ni", # https://en.wiktionary.org/wiki/%EB%8B%88#Suffix
    "ecc_지만" : "CONNECTOR_but_jiman", #https://en.wiktionary.org/wiki/%EC%A7%80%EB%A7%8C
    "ecs_지만" : "CONNECTOR_but_jiman", #https://en.wiktionary.org/wiki/%EC%A7%80%EB%A7%8C
    "ecs_게" : "CONNECTOR_so-that_ge", # https://en.wiktionary.org/wiki/%EA%B2%8C#Suffix
    "ecx_게" : "CONNECTOR_so-that_ge",
    "ecs_고" : "CONNECTOR_and;that_go", # https://en.wiktionary.org/wiki/%EA%B3%A0#Suffix_2
    "ecs_나" : "CONNECTOR_but_na", # https://en.wiktionary.org/wiki/%EB%82%98#Suffix
    "ecs_듯이" : "CONNECTOR_deusi", # https://en.wiktionary.org/wiki/%EB%93%AF%EC%9D%B4#Suffix
    "ecs_라면" : "PRAGMATICMOOD_ra+CONNECTOR_conditional_myeon", # https://en.wiktionary.org/wiki/%EB%A9%B4
    "ecx_려" : "CONNECTOR_intention_려",
    "ecs_고자" : "CONNECTOR_intention_고자", # example in Wiktionary
    "ecs_도록" : "CONNECTOR_in-order-to_dorok", # https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-92-100/lesson-82/
    "ecs_러" : "CONNECTOR_in-order-to_reo", # https://en.wiktionary.org/wiki/%EB%9F%AC 
    "ecs_어" : "CONNECTOR_and-then_eo", # https://en.wiktionary.org/wiki/%EC%96%B4#Suffix
    "ecs_어도" : "CONNECTOR_even-if/although_eodo",
    "ecs_지" : "CONNECTOR_ji", # https://en.wiktionary.org/wiki/%EC%A7%80#Suffix     
    "ecs_자마자" : "CONNECTOR_as_soon_as",
    "ecs_자면" : "CONNECTOR_jamyeon", # https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002299413
    "ecs_면" : "CONNECTOR_conditional_myeon", # https://en.wiktionary.org/wiki/%EB%A9%B4
    "ecs_며" : "CONNECTOR_as/while_myeo", #https://en.wiktionary.org/wiki/%EB%A9%B0
    "ecs_려면" : "CONNECTOR_if-you-want-려면", # https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-92-100/lesson-96/
    "ecs_려고" : "CONNECTOR_intend-to", # https://www.howtostudykorean.com/unit-2-lower-intermediate-korean-grammar/unit-2-lessons-26-33/lesson-32/
    "ecs_려" : "CONNECTOR_ryeo_려",
    "ecc_고": "CONNECTOR_ecc_go", # https://en.wiktionary.org/wiki/%EA%B3%A0 
    "ecs_ㄹ수록" : "CONNECTOR_as-changes_ㄹ수록", #https://www.howtostudykorean.com/unit-6/lessons-126-133/lesson-132/
    "ecs_ㄹ수록" : "CONNECTOR_whether_ㄹ수록", # https://koreanwikiproject.com/wiki/(%EC%9C%BC)%E3%84%B9%EC%A7%80_%EB%AA%A8%EB%A5%B4%EA%B2%A0%EB%8B%A4
    "ecs_ㄹ지도" : "CONNECTOR_you-dont-know-if_ㄹ지도",
    "ecs_ㄹ지라도" : "CONNECTOR_even-if-it-were_ㄹ지라도", # koreangrammaticalforms.com/entry.php?eid=0000001066
    "ecc_거나" : "CONNECTOR_or_거나", # https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-51-58/lesson-58/
    "ecc_나" : "CONNECTOR_or_이나", # https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-51-58/lesson-58/
    "ecs_ㄴ다면서" : "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_declarative_da+CONNECTOR_conjunctive_meyonseo" # https://moen.tistory.com/898
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

    ret = morpheme_slots.get(label + "_" + grapheme)
    if ret:
        slots.append(ret) # label from dictionary morpheme_slots
        return slots




    if grapheme[-1] == "요": # This should always be last
        politeFlag = True
        grapheme = grapheme[:-1]


    ret = morpheme_slots.get(label + "_" + grapheme)
    if ret:
        slots.append(ret) # label from dictionary morpheme_slots
        return slots



    if grapheme:
        if grapheme[0] == "으": # allomorph, epenthetic vowel
            grapheme = grapheme[1:]

        if grapheme[0] == "ㅂ" or grapheme[0] == "습" or grapheme[0] == "읍":
            slots.append("FORMALITY_p")
            grapheme = grapheme[1:]

        if "FORMALITY_p" in slots and grapheme == "니까": # this is an interrogative after a formal, otherwise cause/reason
            slots.append("PRAGMATICMOOD_nikka")
            grapheme = ""

        if label in ["ef", "ecs"] and grapheme:
            if label == "ef" and grapheme[0] == "ㄹ": # future tense TODO: this looks like it's not always future
                slots.append("TENSE/ASPECT_ri")
                grapheme = grapheme[1:]
            if grapheme[0] == "ㄴ" or grapheme[0] == "는": # indicative
                slots.append("SYNTACTICMOOD_indicative_n")
                grapheme = grapheme[1:]
                if grapheme == "지": # indicative + ji turns a verb into a noun-like clause https://www.howtostudykorean.com/unit-2-lower-intermediate-korean-grammar/unit-2-lessons-26-33/lesson-30/
                    slots.append("DERIVATION_ji")
                    grapheme = ""

        if grapheme and label == "ecs" and grapheme[0] == "다":
            slots.append("PRAGMATICMOOD_declarative_da")
            grapheme = grapheme[1:]
        if grapheme and label == "ecs" and grapheme[0] == "라":
            slots.append("PRAGMATICMOOD_ra")
            grapheme = grapheme[1:]


        ret = morpheme_slots.get(label + "_" + grapheme)
        if ret == None and grapheme: 
            if label == "px": # auxiliary verb
                slots.append("AUXILIARY_"+grapheme)
            elif grapheme == "있" or grapheme == "없": # to have / not have, used to modify a main verb
                slots.append("AUXILIARY_"+grapheme)
            elif label == "pvg" or label == "paa": # general verb or attributive adjective
                slots.append("ROOT_") # TODO: why would a root appear later in an affix chain
            elif label ==  "xsn" or label == "xsm": # noun derivational suffix or adjective derivational suffix
                # not technically the root, but probably part of a noun / adj root that got turned into a verb
                slots.append("DERIVATION_"+grapheme)
            elif label == "xsv": # verb derivational suffix
                slots.append("VALENCY_"+grapheme)
            elif label == "etm" or label == "etn": # adnominalizer or nominalizer
                slots.append("SYNTACTICMOOD_"+grapheme)
            elif label == "ep": # pre-final ending marker, usually tense/aspect or honorific (in dictionary)
                slots.append("TENSE/ASPECT_"+grapheme)
            elif label == "jcr": # quotative case particle
                slots.append("PRAGMATICMOOD_"+grapheme)
            elif label == "jca": # adverbial case particle (looks like mostly locative or instrumental)
                slots.append("PRAGMATICMOOD_"+grapheme)
            elif label == "jxc": # common auxiliary (looks like "only", "until", "up to")
                slots.append("PRAGMATICMOOD_"+grapheme)
            elif label == "ecc" or label == "ecs" or label == "ecx": # coordinate conjunction, conjunctive ending, auxiliary conjunction
                slots.append("CONNECTOR_"+grapheme)
            else:
                slots.append("UNKNOWN_"+grapheme)
        elif grapheme:
            slots.append(ret) # label from dictionary morpheme_slots

        grapheme = ""
        if label + "_" + grapheme in morpheme_slots:
            slots.append(morpheme_slots[label + "_" + grapheme])
            grapheme = ""

    if politeFlag: # This should always be last
        slots.append("POLITE_yo")
    
    if len(slots) == 0:
        slots.append("UNKNOWN_"+grapheme)
    assert len(slots) > 0, grapheme
    return slots 

def morpheme_meaning(grapheme, label):
    ret = morpheme_slots.get(label + "_" + grapheme)
    if ret == None: 
        if label == "px": # auxiliary verb
            return "AUXILIARY_"+grapheme
        elif grapheme == "있" or grapheme == "없": # to have / not have, used to modify a main verb
            return "AUXILIARY_"+grapheme
        elif label == "pvg" or label == "paa": # general verb or attributive adjective
            return "ROOT"
        elif label ==  "xsn" or label == "xsm": # noun derivational suffix or adjective derivational suffix
            # not technically the root, but probably part of a noun / adj root that got turned into a verb
            return "ROOT"
        elif label == "xsv": # verb derivational suffix
            return "VALENCY_"+grapheme
        elif label == "etm" or label == "etn": # adnominalizer or nominalizer
            return "SYNTACTICMOOD_"+grapheme
        elif label == "ep": # pre-final ending marker, usually tense/aspect or honorific (in dictionary)
            return "TENSE/ASPECT"
        elif label == "jcr": # quotative case particle
            return "PRAGMATICMOOD_"+grapheme
        elif label == "jca": # adverbial case particle (looks like mostly locative or instrumental)
            return "PRAGMATICMOOD_"+grapheme
        elif label == "jxc": # common auxiliary (looks like "only", "until", "up to")
            return "PRAGMATICMOOD_"+grapheme
        elif label == "ecc" or label == "ecs" or label == "ecx": # coordinate conjunction, conjunctive ending, auxiliary conjunction
            return "CONNECTOR_"+grapheme
        else:
            return "UNKNOWN_"+grapheme
    else:
        return ret # label from dictionary morpheme_slots

### Notes ###
# - The corpus doesn't fully separate morphemes. In cases where a single morpheme from the corpus actually corresponds to multiple morphemes (like HONORIFIC + PAST), I've labeled it with the left-most morpheme's slot (HONORIFIC).

### Issues ###
# - doesn't make sense to me that case particles (usually for nouns) should indicate pragmatic mood
# - doesn't make sense that adnominalizers / nominalizers indicate syntactic mood -- they're changing a verb into a different category
#   - This doesn't matter if we're using verbsWithoutAdnominals
