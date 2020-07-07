# Determine if morpheme is an allomorph 

# Allomorphs come from https://repository.upenn.edu/pwpl/vol22/iss1/10/
# and http://cms.bufs.ac.kr/yslee/research/papers/53AllomorhyinKORnounParticles.pdf 
# and http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.119.7942&rep=rep1&type=pdf 

# accusative 은 / 는 -- jxt
# nominative 이 / 가 -- usually jcs, but sometimes jcc
# topic 을 / 를 -- jco 
# conjunctive, comitative 과 / 와 -- jcj, jct
# instrumental (으)로 -- jca
# conditional (으)면 -- ecs
# effective (으)니 -- ecs
# effective (으)니까, (으)니까요 -- ecs or ef, but doesn't show up that much 
# purposive (으)러 -- ecs, very infrequent
# past ㅆ / 었 -- ep
# perfective 은 / ㄴ -- etm, but is already represented in underlying form
# intentional (으)려 -- ecs or ecx, but usually appears with go, neun, or myeon following
# nominalizer 음 / ㅁ -- etn
# conjunctive (으)면서 -- ecs
# Looks like most allomorphs with 으 at the beginning have a base form without 으

def get_underlying_morph_no_epenthesis(morph, fine_label):
    """
    Determines the underlying form of an allomorph. Does not automatically remove 으 vowel. 
    
    Params:
     - morph: a string of a Korean allomorph
     - fine_label: a string of the allomorph's fine label from the KAIST corpus
    
    Returns: 
     A tuple of the underlying morph and its fine label. 
    """
    allomorph_to_underlying = {
        ("는", "jxt"): ("은", "jxt"),
        ("가", "jcs"): ("이", "jcs"), 
        ("가", "jcc"): ("이", "jcc"), 
        ("를", "jco"): ("을", "jco"),
        ("과", "jcj"): ("와", "jcj"),
        ("과", "jct"): ("와", "jct"),
        ("으로", "jca"): ("로", "jca"),
        ("으면", "ecs"): ("면", "ecs"),
        ("으니", "ecs"): ("니", "ecs"),  
        ("으니까", "ecs"): ("니까", "ecs"),
        ("으니까", "ecf"): ("니까", "ecf"),   
        ("으니까요", "ecs"): ("니까요", "ecs"),
        ("으니까요", "ef"): ("니까요", "ef"),
        ("으러", "ecs"): ("러", "ecs"),
        ("었", "ep"): ("ㅆ", "ep"),
        ("으려", "ecs"): ("려", "ecs"),
        ("으려", "ecx"): ("려", "ecx"),
        ("으려고", "ecs"): ("려고", "ecs"),
        ("으려고", "ecx"): ("려고", "ecx"),
        ("으려는", "ecs"): ("려는", "ecs"),
        ("으려는", "ecx"): ("려는", "ecx"),
        ("으려면", "ecs"): ("려면", "ecs"),
        ("으려면", "ecx"): ("려면", "ecx"),
        ("음", "etn"): ("ㅁ", "etn"),
        ("으면서", "ecs"): ("면서", "ecs")
    }

    if (morph, fine_label) in allomorph_to_underlying:
        return allomorph_to_underlying[(morph, fine_label)]
    else:
        return (morph, fine_label)

def get_underlying_morph(morph, fine_label):
    """
    Determines the underlying form of an allomorph. Automatically removes  으 vowel. 
    
    Params:
     - morph: a string of a Korean allomorph
     - fine_label: a string of the allomorph's fine label from the KAIST corpus
    
    Returns: 
     A tuple of the underlying morph and its fine label. 
    """
    allomorph_to_underlying = {
        ("는", "jxt"): ("은", "jxt"),
        ("가", "jcs"): ("이", "jcs"),
        ("가", "jcc"): ("이", "jcc"),
        ("를", "jco"): ("을", "jco"),
        ("과", "jcj"): ("와", "jcj"),
        ("과", "jct"): ("와", "jct"),
        ("었", "ep"): ("ㅆ", "ep"),
        ("음", "etn"): ("ㅁ", "etn"),
    }

    if morph[0] == "으":
        return (morph[1:], fine_label)
    elif (morph, fine_label) in allomorph_to_underlying:
        return allomorph_to_underlying[(morph, fine_label)]
    else:
        return (morph, fine_label)