#######################################
rules_1 = '''People who are round and red tend to be rough.
If you meet someone with rough skin who is cold from being outside, you'll notice they are nice.
Every time you meet someone kind and nice, they'll be green, too.
Big people with red hair are cold because they cannot find coats that fit.
It's a certainty that any green, big and kind individual is going to be nice.'''

fact_1 = "Bob is a cold and round man who has red and green skin."

explain_1 = '''Information extracted from the given fact, i.e., subject and the attributes (adjectives): **Bob**: *cold*, *round*, *red*, and *green*.

People who are round and red tend to be rough. -- The conditions (adjectives): *round*, *red*. The given fact matches full condition.
If you meet someone with rough skin who is cold from being outside, you'll notice they are nice. -- The conditions (adjectives): *rough*, *cold*. The given fact matches partial condition.
Every time you meet someone kind and nice, they'll be green, too. -- The conditions (adjectives): *kind*, *nice*. The given fact does not match any conditions.
Big people with red hair are cold because they cannot find coats that fit. -- The conditions (adjectives): *big*, *red*. The given fact matches partial condition.
It's a certainty that any green, big and kind individual is going to be nice. -- The conditions (adjectives): *green*, *big*, *kind*. The given fact matches partial condition.
'''

output_1 = '''People who are round and red tend to be rough.
If you meet someone with rough skin who is cold from being outside, you'll notice they are nice.
Big people with red hair are cold because they cannot find coats that fit.
It's a certainty that any green, big and kind individual is going to be nice.'''
#######################################


#######################################
rules_2 = '''Rough and big people are always also cold people.
A green, cold natured person will be rough textured.
Young people that are relatively nice to others, can also tend to be rough.'''

fact_2 = "Fred can be kind but he will talks so much his face turns blue; He is usually red and round other than that."

explain_2 = '''Information extracted from the given fact, i.e., subject and the attributes (adjectives): **Fred**: *kind*, *blue*, *red*, *round*.

Rough and big people are always also cold people. -- The conditions (adjectives): *rough*, *big*. The given fact does not match any conditions.
A green, cold natured person will be rough textured. -- The conditions (adjectives): *green*, *cold*. The given fact does not match any conditions.
Young people that are relatively nice to others, can also tend to be rough. -- The conditions (adjectives): *young*, *nice*. The given fact does not match any conditions.
'''

output_2 = "None"
#######################################


#######################################
rules_3 = '''Anybody young person covered in blue and green will be kind.
All young and kind people that feel blue are described as red.'''

fact_3 = "Young Eric has a round form, believes in green and is rough."

explain_3 = '''Information extracted from the given fact, i.e., subject and the attributes (adjectives): **Eric**: *young*, *round*, *green*, *rough*.

Anybody young person covered in blue and green will be kind. -- The conditions (adjectives): *young*, *blue*, *green*. The given fact matches partial condition.
All young and kind people that feel blue are described as red. -- The conditions (adjectives): *young*, *kind*, *blue*. The given fact matches partial condition.
'''

output_3 = '''Anybody young person covered in blue and green will be kind.
All young and kind people that feel blue are described as red.'''
#######################################

forward_selection_demos = [{"rules": rules_1,
                            "fact": fact_1,
                            "explain": explain_1,
                            "ans": output_1},
                    
                            {"rules": rules_2,
                            "fact": fact_2,
                            "explain": explain_2,
                            "ans": output_2},

                            {"rules": rules_3,
                            "fact": fact_3,
                            "explain": explain_3,
                            "ans": output_3}]

forward_selection_system_prompt = '''Imagine you are one of the greatest AI scientists. You are given **a fact** and **a list of rules** (each rule being a premise with condition(s)). Your task is to evaluate each rule in the list and select those that meet *any* of the following requirements:
- Full Condition Match: The fact fully and directly satisfies all condition(s) of the rule, allowing a valid derivation to obtain a new proposition.
- Partial Condition Match: The fact directly satisfies some, but not all, conditions of the rule. This means that additional fact(s) would be required to make a full derivation and obtain a new proposition.
If no rule is selected, return **None**.

Instructions:
- Only focus on the subject and attributes (adjectives) of the facts and rules. Ignore verbs (e.g., "looks...", "acts...") and modifying words (e.g., "very...", "is likely...") and nouns (e.g., "...age") and conditions (e.g., "...when...") of the attributes (adjectives).
- No synonyms or approximations are allowed (e.g., nice != kind).'''