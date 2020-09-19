# based on matchedAllomorphs.tsv
morpheme_slots = {
    "jp_이": "DERIVATION_predicative_i", # predicative maker
    "ep_으시": "HONORIFIC_honorific_s", # Kawasaki chapter 7.2
    "ef_십시오": "HONORIFIC_honorific_s+FORMALITY_formal_polite_p+PRAGMATICMOOD_formal_polite_imperative_시오", # honorific formal polite imperative https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation -si-psio where -si- is honorific, -psio is sentence-final imperative. The -si- doesn't really seem to be part of the affix: https://en.wiktionary.org/wiki/%ED%95%98%EB%8B%A4
    "ef_세요": "HONORIFIC_honorific_s+PRAGMATICMOOD_indicative_informal_어+POLITE_polite_요", # honorific informal polite imperative. E.g. https://en.wiktionary.org/wiki/%EC%98%A4%EB%8B%A4#Korean
    "ep_시": "HONORIFIC_honorific_s", # usually subjunctive, but sometimes is HONORIFIC. Kawasaki chapter 7.2
    "ef_세": "HONORIFIC_honorific_s+PRAGMATICMOOD_indicative_informal_어",
    "ef_시오" : "HONORIFIC_honorific_s+PRAGMATICMOOD_semiformal_오",
    "ef_으리오": "VALENCY_passive/causative_ri", # passative / causative https://en.wiktionary.org/wiki/%EB%A6%AC (barely occurs in the corpus)
    "ef_리오": "VALENCY_passive/causative_ri", # passative / causastive https://en.wiktionary.org/wiki/%EB%A6%AC (barely occurs in the corpus)
    "ef_ㄹ세": "UNKNOWN_ef_ㄹ세", # cf https://devr.tistory.com/318 for lsera
    "ef_ㄹ걸": "UNKNOWN_ef_ㄹ걸", # future tense -l
    "ef_ㄹ지어다": "UNKNOWN_ㄹ지어다", # future tense -l
    "ef_지어다": "PRAGMATICMOOD_지어다", # https://www.reddit.com/r/Korean/comments/di3d8z/help_me_understand_the_ending_%EC%9D%84%EC%A7%80%EC%96%B4%EB%8B%A4_please/
    "ef_ㄹ지": "TENSE/ASPECT_l+PRAGMATICMOOD_ji", # future tense -l   https://devr.tistory.com/320
    "ef_ㄹ지라": "UNKNOWN_ㄹ지라", # future tense -l
    "ef_ㄹ쏘냐": "UNKNOWN_ㄹ쏘냐", # future tense -l
    "ef_쏘냐": "PRAGMATICMOOD_interrogative_쏘냐", # interrogative https://www.reddit.com/r/Korean/comments/aqytjr/what_does_%EB%91%90%EB%A0%A4%EC%9A%B8%EC%86%8C%EB%83%90_consist_of/
    "ef_ㄹ지어라": "UNKNOWN_ㄹ지어라", # future tense -l
    "ef_ㄹ텐데": "UNKNOWN_ㄹ텐데", # future tense -l
    "ef_텐데": "PRAGMATICMOOD_텐데", # expresses uncertainty and regret https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-92-100/lesson-100/
    "ef_읍시다": "FORMALITY_formal_polite_p+PRAGMATICMOOD_hortative_formal_polite_sida", # -eub is formal
    "ef_ㅂ디다": "FORMALITY_formal_polite_p+UNKNOWN_디다", # -b is formal
    "ef_ㅂ시다": "FORMALITY_formal_polite_p+PRAGMATICMOOD_hortative_formal_polite_sida", # -b is formal
    "ef_ㅂ니까": "FORMALITY_formal_polite_p+SYNTACTICMOOD_formal_polite_ni+PRAGMATICMOOD_interrogative_ka", # -b is formal, -kka is interrogative
    "ef_ㅂ니다": "FORMALITY_formal_polite_p+SYNTACTICMOOD_formal_polite_ni+PRAGMATICMOOD_declarative_da", # -b is formal
    "ef_습니다": "FORMALITY_formal_polite_p+SYNTACTICMOOD_formal_polite_ni+PRAGMATICMOOD_declarative_da", # -seub is formal
    "ef_ㅂ시요": "FORMALITY_formal_polite_p+PRAGMATICMOOD_formal_polite_imperative_시오", # -b is formal
    "ef_ㅂ시오": "FORMALITY_formal_polite_p+PRAGMATICMOOD_formal_polite_imperative_시오", # -b is formal
    "ef_습니까": "FORMALITY_formal_polite_p+SYNTACTICMOOD_formal_polite_ni+PRAGMATICMOOD_interrogative_ka", # -seub is formal, -kka is interrogative
    "ef_입니다": "FORMALITY_formal_polite_p+SYNTACTICMOOD_formal_polite_ni+PRAGMATICMOOD_declarative_da", # formal "to be"
    "ef_ㄹ런지요" : "CONNECTOR_ㄹ런지+POLITE_polite_요",
    "ecs_ㄹ런지" : "CONNECTOR_ㄹ런지",
    "ep_더": "SYNTACTICMOOD_imperfective_deon", # Lee & Robert: -te- Retrospective https://en.wiktionary.org/wiki/%EB%8D%94 Follows past tense marker, thus not TENSE?ASPECT here https://en.wiktionary.org/wiki/%EB%8D%94
    "ef_리": "SYNTACTICMOOD_I_guess_ri", # "I guess..." https://en.wiktionary.org/wiki/%EB%A6%AC
    "ef_으리": "SYNTACTICMOOD_I_guess_ri", # "I guess..." https://en.wiktionary.org/wiki/%EB%A6%AC 
    "ef_으리라": "SYNTACTICMOOD_I_guess_ri+PRAGMATICMOOD_ra", # https://en.wiktionary.org/wiki/%EB%9D%BC Etymology 6
    "ef_리라": "SYNTACTICMOOD_I_guess_ri+PRAGMATICMOOD_ra", # https://en.wiktionary.org/wiki/%EB%9D%BC
    "ef_니": "SYNTACTICMOOD_indicative_n", # allomorph of indicative. TODO but also question marker: Yeon and Brown, p. 182 (section 4.3.6.2)
    "ef_시오": "PRAGMATICMOOD_formal_polite_imperative_시오", # subjunctive formal polite -si + imperative -o
    "ef_더군": "SYNTACTICMOOD_imperfective_deon+PRAGMATICMOOD_mirative_gun", # allomorph of imperfective -deon, mirative -gun
    "ef_는군": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_mirative_gun", # indicative -neun, mirative -gun
    "ef_는가": "PRAGMATICMOOD_interrogative_(neu)nka", # indicative -neun. Yeon and Brown, p. 183.
    "ef_ㄴ가": "PRAGMATICMOOD_interrogative_(neu)nka", # indicative -n. Yeon and Brown, p. 183.
    "ef_ㄴ다": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_declarative_da", # indicative -n, declarative -da
    "ef_는다": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_declarative_da", # indicative -neun, declarative -da
#    "ef_ㄴ지": "SYNTACTICMOOD", # indicative -n, of course / biased questions -ji
#    "ef_는지": "SYNTACTICMOOD", # indicative -neun, of course / biased questions -ji
    "ef_던가": "SYNTACTICMOOD_imperfective_deon+PRAGMATICMOOD_interrogative_ka", # retrospective / imperfective -deon with interrogative https://www.howtostudykorean.com/unit-5/unit-5-lessons-117-125/lesson-117/#1171
#    "ef_는구나": "SYNTACTICMOOD", # indicative -neun
#    "ef_ㄴ걸": "SYNTACTICMOOD", # indicative -n
    "ef_ㄴ데": "SYNTACTICMOOD_indicative_n+CONNECTOR_connector_de", # indicative -n, contrast connector -de
    "ef_는지요": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_ji+POLITE_polite_요", # indicative -neun, of course / biased question -ji, polite -yo
    "ef_ㄴ데요": "SYNTACTICMOOD_indicative_n+CONNECTOR_contrast_connector_de+POLITE_polite_요", # indicative -n, contrast connector -de, polite -yo
    "ef_는단다": "SYNTACTICMOOD_indicative_n+UNKNOWN_단다", # indicative -neun
    "ef_ㄴ지라": "SYNTACTICMOOD_indicative_n+UNKNOWN_지라", # indicative -n
    "ef_ㄴ거지": "SYNTACTICMOOD_indicative_n+UNKNOWN_거지", # indicative -n
    "ef_오": "PRAGMATICMOOD_semiformal_오", # imperative TODO
    "ef_아라": "PRAGMATICMOOD_imperative_ra/eora/ara",	# allomorph of 어라. https://en.wiktionary.org/wiki/%EC%95%84%EB%9D%BC https://en.wiktionary.org/wiki/%EC%96%B4%EB%9D%BC
    "ef_어라": "PRAGMATICMOOD_imperative_ra/eora/ara",
    "ef_라"  : "PRAGMATICMOOD_imperative_ra/eora/ara", # imperative https://en.wiktionary.org/wiki/%EB%9D%BC#Suffix_2
    "ef_으라": "PRAGMATICMOOD_imperative_ra/eora/ara", # imperative https://en.wiktionary.org/wiki/%EB%9D%BC#Suffix_2
    "ef_을까": "PRAGMATICMOOD_interrogative_lkka", # interrogative, https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635 https://en.wiktionary.org/wiki/%EC%9D%84%EA%B9%8C
    "ef_어요": "PRAGMATICMOOD_indicative_informal_어+POLITE_polite_요", # indicative informal polite
    "ef_다": "PRAGMATICMOOD_declarative_da", # declarative -da
    "ef_다.": "PRAGMATICMOOD_declarative_da", # a typo, declarative -da
    "ef_에": "PRAGMATICMOOD_e",
#    "ef_에요": "PRAGMATICMOOD", # polite -yo
    "ef_구나": "PRAGMATICMOOD_mirative_gun", # something like a mirative, "Oh I just realized that..." https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-76-83/lesson-82-2/#921
    "ef_군": "PRAGMATICMOOD_mirative_gun", # ^ same mirative
    "ef_군요" : "PRAGMATICMOOD_mirative_gun+POLITE_polite_요",
#    "ef_군요": "mirative+polite_요", # ^ same mirative with polite -yo
    #########################
    # RAGO ##################
    "ef_라고": "PRAGMATICMOOD_ef_quotative", # quotative
    "ef_라구": "PRAGMATICMOOD_ef_quotative", # quotative
    "ef_라니": "PRAGMATICMOOD_ef_quotative", # contraction of quotative
    "jcr_라고" : "PRAGMATICMOOD_jcr_rago", # https://en.wiktionary.org/wiki/%EB%9D%BC%EA%B3%A0#Suffix
    #########################
    "ef_자": "PRAGMATICMOOD_hortative_formal_nonpolite_자", # # Slot VI
    # NYA. Yeon and Brown, section 4.3.6.2
    "ef_냐": "PRAGMATICMOOD_formal_nonpolite_interrogative_nya", # interrogative. for adjectives https://en.wiktionary.org/wiki/%EA%B7%B8%EB%A5%B4%EB%8B%A4
    "ef_느냐": "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_formal_nonpolite_interrogative_nya", # interrogative formal non-polite (table in https://en.wiktionary.org/wiki/%EC%9E%88%EB%8B%A4)
    #
    "ef_소": "PRAGMATICMOOD_declarative_so", # declarative from outdated haoche style https://blog.lingodeer.com/the-definitive-guide-to-korean-speech-levels/
    "ef_ㄹ까": "PRAGMATICMOOD_interrogative_lkka", # interrogative "Should I do this for you?" https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-59-66/lesson-63/#635
    "ef_ㄹ까요": "PRAGMATICMOOD_interrogative_lkka+POLITE_polite_요", # interrogative -lkka, polite -yo
    "ef_지": "PRAGMATICMOOD_ji", # something like "of course" or a biased question. Wikipedia: Casual
    "ef_죠": "PRAGMATICMOOD_ji+POLITE_polite_요", # same as -ji with -yo polite. Kawasaki Chapter 6.15.
    "ef_지요": "PRAGMATICMOOD_ji+POLITE_polite_요", # same as ^ -jyo
    "ef_나": "PRAGMATICMOOD_causal_interrogative_na", # casual interrogative https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjT1NPEj9DqAhXEGc0KHVZaDbsQFjAAegQIBhAB&url=https%3A%2F%2Fgobillykorean.com%2Fshop%2FFile%2Fget%2F%3Ffile%3DGo_Billy_Korean_Episode_28.pdf&usg=AOvVaw1Q1-UDawtJGqrhJ62jjstX
    "ef_지마라": "PRAGMATICMOOD_negative_imperative_지마라", # negative imperative
    "ef_리요": "PRAGMATICMOOD_imperative_old_style", # imperative (but an older style)
    "ef_답니다": "PRAGMATICMOOD_답니다", # something like a quotative? https://forum.wordreference.com/threads/%EB%8B%B5%EB%8B%88%EB%8B%A4.2253519/
    "jxf_요": "POLITE_polite_요",
    "ef_요": "POLITE_polite_요",
    "ef_니까": "CONNECTOR_(eu)nikka", # formal polite cause/reason -nikka https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_으니까": "CONNECTOR_(eu)nikka", # formal polite cause/reason -eunikka
    "ef_니까요": "CONNECTOR_(eu)nikka+POLITE_polite_요", # formal polite cause/reason -nikka, polite -yo
    "ef_으니까요": "CONNECTOR_(eu)nikka+POLITE_polite_요", # formal polite cause/reason -eunikka, polite -yo
    "ef_구": "CONNECTOR_구", # can't tell what this is, some people say it's a different way to write -go
    "ef_야": "CONNECTOR_connective_condition_ya", # condition connective form, https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_데": "CONNECTOR_de", # contrast connective form https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_랴": "CONNECTOR_rya", # https://krdict.korean.go.kr/eng/dicSearch/SearchView?divSearch=defViewGlobal&ParaWordNo=80306&nationCode=6&ParaNationCode=6&nation=eng&captchaNumber=&comment_user_name=&commentTitle=&wordComment=&viewTypes=on 
    "ef_으랴": "CONNECTOR_rya", # https://krdict.korean.go.kr/eng/dicSearch/SearchView?divSearch=defViewGlobal&ParaWordNo=80306&nationCode=6&ParaNationCode=6&nation=eng&captchaNumber=&comment_user_name=&commentTitle=&wordComment=&viewTypes=on 
    "ef_옵니다": "AUXILIARY_옵니다", # formal indicative "to come" (not a suffix, it's a new verb)
    "ep_었었" : "TENSE/ASPECT_remote_past_었었",
    "ep_았었" : "TENSE/ASPECT_remote_past_었었",
    "ep_ㅆ었" : "TENSE/ASPECT_remote_past_었었",
    "ecx_려고" : "CONNECTOR_intention_려고", # https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ecc_면서" : "CONNECTOR_conjunctive_myeonseo",
    "ecs_면서" : "CONNECTOR_conjunctive_meyonseo",
    "ecs_서" : "CONNECTOR_conjunctive_seo", # Kawasaki chapter 8.3
    "ecs_아서" : "CONNECTOR_conjunctive_aseo",
    "ecs_아야" : "CONNECTOR_conjunctive_aya", # https://en.wiktionary.org/wiki/%EC%96%B4%EC%95%BC Alternatuve 아야 and 어야 according to https://en.wiktionary.org/wiki/%EC%96%B4%EC%95%BC
    "ecs_어서" : "CONNECTOR_conjunctive_aseo",
    "ecs_어야" : "CONNECTOR_conjunctive_aya", # https://en.wiktionary.org/wiki/%EC%96%B4%EC%95%BC
    "ecx_어야" : "CONNECTOR_conjunctive_aya", # in order to https://keytokorean.com/grammar/%ec%95%84%ec%96%b4%ec%95%bc-do-a-so-you-can-do-b/ https://www.koreanwikiproject.com/wiki/%EC%95%84/%EC%96%B4_%2B_%EC%95%BC
    "ecx_아야"  : "CONNECTOR_conjunctive_aya",
    "ef_어야지": "PRAGMATICMOOD_one_should_do_something_어야지", # one should do something. This is an alternative of aya according to https://en.wiktionary.org/wiki/%EC%96%B4%EC%95%BC
    "ef_아야지" : "PRAGMATICMOOD_one_should_do_something_어야지", # one should do something. This is an alternative of aya according to https://en.wiktionary.org/wiki/%EC%96%B4%EC%95%BC
    "ecs_이" : "CONNECTOR_connector_i",
    "ef_ㄹ까" : "PRAGMATICMOOD_interrogative_lkka",
    "ep_셨" : "HONORIFIC_honorific_s+TENSE/ASPECT_past", # portmanteau honorific (SLOT II) + past  (https://en.wikipedia.org/wiki/Korean_verbs)
    "ep_었겠" : "TENSE/ASPECT_remote_past/future_eossget",
    "ep_았겠" : "TENSE/ASPECT_remote_past/future_eossget", # SLOT III
    "ep_겠" : "TENSE/ASPECT_assertive/strong-will_get",   # assertive (table in https://en.wiktionary.org/wiki/%EC%9E%88%EB%8B%A4) (SLOT III). Kawasaki 8.10 states that 겠, ᄊ come in orsder determined by scope.
    "ep_ㅆ" : "TENSE/ASPECT_past", # 
    "xsv_되" : "DERIVATION_denominal_되", # as a verb, this means 'to become'
    "xsv_하" : "DERIVATION_verb_하",  # The verb hada 'to do' as in 해결하려고	해결+하+려고	VERB	ncpa+xsv+ecx: https://en.wiktionary.org/wiki/%ED%95%B4%EA%B2%B0%ED%95%98%EB%8B%A4
    "xsn_뿐" : "DERIVATION_뿐", # derives something meaning "only X" https://en.wiktionary.org/wiki/%EB%BF%90#Particle 도시귀족뿐이었다 도시+귀족+뿐+이+었+다	VERB	ncn+ncn+xsn+jp+ep+e 'it was only Urban aristocracy'
    "xsn_적" : "DERIVATION_적",
    "xsn_들" : "DERIVATION_뿐",
    "xsn_들" : "DERIVATION_들", # https://en.wiktionary.org/wiki/%EB%93%A4#Particle
    "xsm_하" : "DERIVATION_adj_하", # the adjective hada 'have a quality' as in 필요하다	필요+하+다	VERB	ncps+xsm+ef 필요하다 https://en.wiktionary.org/wiki/%ED%95%84%EC%9A%94%ED%95%98%EB%8B%A4 https://en.wiktionary.org/wiki/%EA%B0%80%EB%8A%A5%ED%95%98%EB%8B%A4 https://en.wiktionary.org/wiki/%EB%B6%88%EA%B0%80%EB%8A%A5%ED%95%98%EB%8B%A4
    "xsm_스럽" : "DERIVATION_스럽", # seureop https://en.wiktionary.org/wiki/%EC%8A%A4%EB%9F%BD%EB%8B%A4 forms adjectives
    "xsv_시키" : "DERIVATION_시키", # https://en.wiktionary.org/wiki/%EC%8B%9C%ED%82%A4%EB%8B%A4
    "xsv_받"   : "DERIVATION_받", # e.g. https://en.wiktionary.org/wiki/%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8B%A4
    "jxc_부터" : "PRAGMATICMOOD_buteo", #https://en.wiktionary.org/wiki/%EB%B6%80%ED%84%B0
    "jxc_라도" : "PRAGMATICMOOD_rado", #https://en.wiktionary.org/wiki/%EB%9D%BC%EB%8F%84
    "jxc_도" : "CONNECTOR_do", # https://en.wiktionary.org/wiki/%EB%8F%84#Particle
    "jxc_까지" : "PRAGMATICMOOD_까지",
    "jca_에서" : "PRAGMATICMOOD_eseo", # https://en.wiktionary.org/wiki/%EC%97%90%EC%84%9C
    "jca_에" : "CONNECTOR_e",
    "jca_로"  : "CONNECTOR_ro", # "by" https://en.wiktionary.org/wiki/%EB%A1%9C#Particle
    "jca_로서"   : "CONNECTOR_roseo", # "by" according to Wiktionary
    "jca_로써"   : "CONNECTOR_rosseo",   # "by" according to Wiktionary
    "jca_보다"   : "CONNECTOR_boda", #https://en.wiktionary.org/wiki/%EB%B3%B4%EB%8B%A4#Particle
#    "ef_소" : "PRAGMATICMOOD_소",
    "ep_어야겠" : "TENSE/ASPECT_tense/aspect_have-to-do",
    "ep_었더" : "TENSE/ASPECT_a-type-of-past",
    "ep_았" : "TENSE/ASPECT_past", # allmorph of ss. E.g. in this verb: https://en.wiktionary.org/wiki/%EB%B0%9B%EB%8B%A4#Korean
    "ep_았더" : "TENSE/ASPECT_past_...",
    "ep_아야겠" : "TENSE/ASPECT_need-to",
    "jxc_만" : "PRAGMATICMOOD_only",
    "ep_더" : "SYNTACTICMOOD_imperfective_deon", # Allomorph of -deon (SLOT V)
#    "ef_ㄹ세" : "TENSE/ASPECT_???",
    "ecs_ㄴ다면" : "CONNECTOR_conditional_ㄴ다면",
    "ecs_니" : "CONNECTOR_and-then_ni", # https://en.wiktionary.org/wiki/%EB%8B%88#Suffix
    "ecc_지만" : "CONNECTOR_but_jiman", #https://en.wiktionary.org/wiki/%EC%A7%80%EB%A7%8C
    "ecs_지만" : "CONNECTOR_but_jiman", #https://en.wiktionary.org/wiki/%EC%A7%80%EB%A7%8C
    "ecs_게" : "CONNECTOR_so-that_ge", # https://en.wiktionary.org/wiki/%EA%B2%8C#Suffix
    "ecx_게" : "CONNECTOR_so-that_ge",
    "ecs_나" : "CONNECTOR_but_na", # https://en.wiktionary.org/wiki/%EB%82%98#Suffix
    "ecs_듯이" : "CONNECTOR_deusi", # https://en.wiktionary.org/wiki/%EB%93%AF%EC%9D%B4#Suffix
    "ecs_라면" : "PRAGMATICMOOD_ra+CONNECTOR_conditional_myeon", # https://en.wiktionary.org/wiki/%EB%A9%B4 . ra also plain-declarative/ ???
    "ecx_려" : "CONNECTOR_intention_려",
    "ecs_고자" : "CONNECTOR_intention_고자", # example in Wiktionary
    "ecs_도록" : "CONNECTOR_in-order-to_dorok", # https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-92-100/lesson-82/
    "ecs_러" : "CONNECTOR_in-order-to_reo", # https://en.wiktionary.org/wiki/%EB%9F%AC 
    "ef_어": "PRAGMATICMOOD_indicative_informal_어", # indicative informal non-polite
    "ecs_어" : "CONNECTOR_infinitive_a/eo", # https://en.wiktionary.org/wiki/%EC%96%B4#Suffix   ecs is Etymology 4 (infinitive)
    "ecs_아" : "CONNECTOR_infinitive_a/eo", # https://en.wiktionary.org/wiki/%EC%96%B4#Suffix
    "ecx_어" : "CONNECTOR_infinitive_a/eo",# https://en.wiktionary.org/wiki/어
    "ecx_아" : "CONNECTOR_infinitive_a/eo", # https://en.wiktionary.org/wiki/어
    "ecs_어도" : "CONNECTOR_even-if/although_eodo",
    "ecs_지" : "CONNECTOR_ecs_ji", # https://en.wiktionary.org/wiki/%EC%A7%80#Suffix     
    "ecx_지" : "CONNECTOR_ecx_ji",
    "ecs_자마자" : "CONNECTOR_as_soon_as",
    "ecs_자면" : "CONNECTOR_jamyeon", # https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002299413
    "ecs_면" : "CONNECTOR_conditional_myeon", # https://en.wiktionary.org/wiki/%EB%A9%B4
    "ecs_며" : "CONNECTOR_as/while_myeo", #https://en.wiktionary.org/wiki/%EB%A9%B0
    "ecs_려면" : "CONNECTOR_if-you-want-려면", # https://www.howtostudykorean.com/upper-intermediate-korean-grammar/unit-4-lessons-92-100/lesson-96/
    "ecs_려고" : "CONNECTOR_intention_려고", # https://www.howtostudykorean.com/unit-2-lower-intermediate-korean-grammar/unit-2-lessons-26-33/lesson-32/
    "ecs_려" : "CONNECTOR_ryeo_려",
    # GO
    "ecc_고": "CONNECTOR_go", # https://en.wiktionary.org/wiki/%EA%B3%A0 
    "ecx_고" : "CONNECTOR_go", # I want to https://www.howtostudykorean.com/unit1/unit-1-lessons-17-25-2/lesson-17/ Conjunctive ending (https://en.wikipedia.org/wiki/Korean_verbs)
    "ef_고": "CONNECTOR_go", # https://en.wiktionary.org/wiki/%EA%B3%A0 Kawasaki chapter 8.2 (...), 11.2 (quotative).
    "jcr_고" : "CONNECTOR_go", # the jcr version appears in ra+go https://en.wiktionary.org/wiki/%EB%9D%BC%EA%B3%A0#Suffix
    "ecs_고" : "CONNECTOR_go", # https://en.wiktionary.org/wiki/%EA%B3%A0#Suffix_2
    #
    "ecs_ㄹ수록" : "CONNECTOR_as-changes_ㄹ수록", #https://www.howtostudykorean.com/unit-6/lessons-126-133/lesson-132/
    "ecs_ㄹ수록" : "CONNECTOR_whether_ㄹ수록", # https://koreanwikiproject.com/wiki/(%EC%9C%BC)%E3%84%B9%EC%A7%80_%EB%AA%A8%EB%A5%B4%EA%B2%A0%EB%8B%A4
    "ecs_ㄹ지도" : "CONNECTOR_you-dont-know-if_ㄹ지도",
    "ecs_ㄹ지라도" : "CONNECTOR_even-if-it-were_ㄹ지라도", # koreangrammaticalforms.com/entry.php?eid=0000001066
    "ecc_거나" : "CONNECTOR_or_거나", # https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-51-58/lesson-58/
    "ecc_나" : "CONNECTOR_or_이나", # https://www.howtostudykorean.com/unit-3-intermediate-korean-grammar/unit-3-lessons-51-58/lesson-58/
    "ecs_ㄴ다면서" : "SYNTACTICMOOD_indicative_n+PRAGMATICMOOD_declarative_da+CONNECTOR_conjunctive_meyonseo", # https://moen.tistory.com/898
    "ecc_ㄹ까" : "PRAGMATICMOOD_interrogative_lkka", # https://en.wiktionary.org/wiki/%E3%84%B9%EA%B9%8C Kawasaki Chapter 6.12
    "ecs_ㄹ까" : "PRAGMATICMOOD_interrogative_lkka", # https://en.wiktionary.org/wiki/%E3%84%B9%EA%B9%8C
    "ecx_ㄹ까" : "PRAGMATICMOOD_interrogative_lkka", # https://en.wiktionary.org/wiki/%E3%84%B9%EA%B9%8C
    "ef_ㄹ까" : "PRAGMATICMOOD_interrogative_lkka", # https://en.wiktionary.org/wiki/%E3%84%B9%EA%B9%8C
    "ecc_ㄹ까" : "CONNECTOR_weak-will_ㄹ까", # Kawasaki Chapter 6.13
    "ef_단다" : "PRAGMATICMOOD_tanta", # https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002391173
    "ef_아" : "PRAGMATICMOOD_아", # https://en.wiktionary.org/wiki/%EC%95%84#Suffix_2
    "ef_에요" : "PRAGMATICMOOD_e+POLITE_polite_요",
    "ef_걸": "NOMINALIZER_nominalization_gos-eul", # contraction of gos-eul which turns a verb into a noun, https://forum.wordreference.com/threads/%EB%8A%94-%EA%B1%B8.1999585/ https://en.wiktionary.org/wiki/%EA%B1%B8
    ###########################
    # Noun and Determiner Forms
    "etn_기" : "NOMINALIZER_nominalizer_informal_nonpolite_gi",
    "etn_ㅁ" : "NOMINALIZER_nominalizer_formal_nonpolite_m",
    # NEUN
    "etm_는" : "NOMINALIZER_present_determiner_는",
    "etm_ㄴ" : "NOMINALIZER_past_determiner_ㄴ",
    ###########################
    # EUL
    "jco_을" : "NOMINALIZER_future_determiner_을", # https://en.wiktionary.org/wiki/%EC%9D%84#Suffix
    "etm_을" : "NOMINALIZER_future_determiner_을",
    "etm_ㄹ" : "NOMINALIZER_future_determiner_을",
    # EUN
    "jxt_은" : "NOMINALIZER_past_determiner_ㄴ", # Also labeled etm. # https://en.wiktionary.org/wiki/%EC%9D%80#Particle
    "etm_은" : "NOMINALIZER_past_determiner_ㄴ", # https://en.wiktionary.org/wiki/%EC%9D%80#Particle. Also  https://en.wiktionary.org/wiki/%EB%82%B3%EB%8B%A4#Korean 낳은 past determiner is labeled pvg+etm
    "jcm_의" : "CASE_possessive_ui", # https://en.wiktionary.org/wiki/%EC%9D%98
    "jcs_이" : "CASE_i",
    "pad_어떻" : "CONNECTOR_어떻",
    "ecs_는데" : "CONNECTOR_informal_nonpolite_contrast_neunde", #https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ecs_더니" : "CONNECTOR_informal_polite_deoni", # https://en.wiktionary.org/wiki/%EA%B0%80%EB%8B%A4#Conjugation
    "ef_네" : "PRAGMATICMOOD_exclamatory_ne", # https://en.wiktionary.org/wiki/%EB%84%A4#Suffix
    "ef_다네" : "PRAGMATICMOOD_declarative_da+PRAGMATICMOOD_exclamatory_ne"
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
#    print(label + "_" + grapheme)
    ret = morpheme_slots.get(label + "_" + grapheme)
    if ret:
        slots.append(ret) # label from dictionary morpheme_slots
        return slots




#    if grapheme[-1] == "요": # This should always be last
 #       politeFlag = True
  #      grapheme = grapheme[:-1]


    ret = morpheme_slots.get(label + "_" + grapheme)
    if ret:
        slots.append(ret) # label from dictionary morpheme_slots
        return slots



    if grapheme:
        if grapheme[0] == "으": # allomorph, epenthetic vowel
            grapheme = grapheme[1:]

        if grapheme[0] == "ㅂ" or grapheme[0] == "습" or grapheme[0] == "읍":
            slots.append("FORMALITY_formal_polite_p")
            grapheme = grapheme[1:]

        if "FORMALITY_formal_polite_p" in slots and grapheme == "니까": # this is an interrogative after a formal, otherwise cause/reason
            slots.append("PRAGMATICMOOD_nikka")
            grapheme = ""

        if label in ["ef", "ecs"] and grapheme:
            if label == "ef" and grapheme[0] == "ㄹ": # future tense TODO: this looks like it's not always future
                assert False
                slots.append("TENSE/ASPECT_ri")
                grapheme = grapheme[1:]
            if grapheme[0] == "ㄴ" or grapheme[0] == "는": # indicative
                slots.append("SYNTACTICMOOD_indicative_n")
                grapheme = grapheme[1:]
                if grapheme == "지": # indicative + ji turns a verb into a noun-like clause https://www.howtostudykorean.com/unit-2-lower-intermediate-korean-grammar/unit-2-lessons-26-33/lesson-30/
                    slots.append("PRAGMATICMOOD_ji") # or maybe CONNECTOR
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
                slots.append("CONNECTOR_"+grapheme) # TODO: why would a root appear later in an affix chain
            elif label ==  "xsn" or label == "xsm": # noun derivational suffix or adjective derivational suffix
                # not technically the root, but probably part of a noun / adj root that got turned into a verb
                slots.append("DERIVATION_"+grapheme)
            elif label == "xsv": # verb derivational suffix
                slots.append("DERIVATION_"+grapheme)
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
        slots.append("POLITE_polite_요")
    
    if len(slots) == 0:
        slots.append("UNKNOWN_"+grapheme)
    assert len(slots) > 0, grapheme
    return slots 

#def morpheme_meaning(grapheme, label):
#    ret = morpheme_slots.get(label + "_" + grapheme)
#    if ret == None: 
#        if label == "px": # auxiliary verb
#            return "AUXILIARY_"+grapheme
#        elif grapheme == "있" or grapheme == "없": # to have / not have, used to modify a main verb
#            return "AUXILIARY_"+grapheme
#        elif label == "pvg" or label == "paa": # general verb or attributive adjective
#            return "ROOT"
#        elif label ==  "xsn" or label == "xsm": # noun derivational suffix or adjective derivational suffix
#            # not technically the root, but probably part of a noun / adj root that got turned into a verb
#            return "ROOT"
#        elif label == "xsv": # verb derivational suffix
#            return "VALENCY_"+grapheme
#        elif label == "etm" or label == "etn": # adnominalizer or nominalizer
#            return "SYNTACTICMOOD_"+grapheme
#        elif label == "ep": # pre-final ending marker, usually tense/aspect or honorific (in dictionary)
#            return "TENSE/ASPECT"
#        elif label == "jcr": # quotative case particle
#            return "PRAGMATICMOOD_"+grapheme
#        elif label == "jca": # adverbial case particle (looks like mostly locative or instrumental)
#            return "PRAGMATICMOOD_"+grapheme
#        elif label == "jxc": # common auxiliary (looks like "only", "until", "up to")
#            return "PRAGMATICMOOD_"+grapheme
#        elif label == "ecc" or label == "ecs" or label == "ecx": # coordinate conjunction, conjunctive ending, auxiliary conjunction
#            return "CONNECTOR_"+grapheme
#        else:
#            return "UNKNOWN_"+grapheme
#    else:
#        return ret # label from dictionary morpheme_slots
#
#### Notes ###
## - The corpus doesn't fully separate morphemes. In cases where a single morpheme from the corpus actually corresponds to multiple morphemes (like HONORIFIC + PAST), I've labeled it with the left-most morpheme's slot (HONORIFIC).
#
#### Issues ###
## - doesn't make sense to me that case particles (usually for nouns) should indicate pragmatic mood
## - doesn't make sense that adnominalizers / nominalizers indicate syntactic mood -- they're changing a verb into a different category
##   - This doesn't matter if we're using verbsWithoutAdnominals
