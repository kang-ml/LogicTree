#######################################
rules_1 = '''If there is at least one people who is neither long nor bad, then Wiley is alert.
Someone is alert and not long if and only if he is cultural and not sore.
Someone being both cultural and not alert is equivalent to being average and bad.
Someone who is bad is always both sore and not alert.
If someone who is not long is also not alert, then he is sore.
If all people are not long, then Wiley is average.'''

fact_1 = "Ronald is not long."

explain_1 = '''Information extracted from the given fact:
**Ronald**: *not long*.

Information extracted from the given rules:
If there is at least one people who is neither long nor bad, then Wiley is alert. -- The conditions equal to *not long* and *not bad*. The given fact matches partial condition.
Someone is alert and not long if and only if he is cultural and not sore. -- 'if and only if' is biconditional. The conditions are (1) *alert* and *not long*. The given fact matches partial condition in this case. Or (2) *cultural* and *not sore*. The given fact does not match any conditions in this case.
Someone being both cultural and not alert is equivalent to being average and bad. -- 'equivalent to' is biconditional. The conditions are (1) *cultural* and *not alert*. The given fact does not match any conditions in this case. Or (2) *average* and *bad*. The given fact does not match any conditions in this case.
Someone who is bad is always both sore and not alert. -- The condition is *bad*. The given fact does not match any conditions.
If someone who is not long is also not alert, then he is sore. -- The conditions are *not long* and *not alert*. The given fact matches partial condition.
If all people are not long, then Wiley is average. -- The condition has *all people*, which is considered as a universal quantifier. The given fact does not match any conditions.
'''

output_1 = '''If there is at least one people who is neither long nor bad, then Wiley is alert.
Someone is alert and not long if and only if he is cultural and not sore.
If someone who is not long is also not alert, then he is sore.'''
#######################################


#######################################
rules_2 = '''Someone being both fearless and reasonable is equivalent to being not sparkling.
Tyra is not fearless and Cara is bewildered if and only if Tyra is not sparkling and Lewis is reasonable.
If all people are fearless, then Tyra is reasonable.
If Tyra is either fearless or faithful, then Tyra is not bewildered and Nigel is reasonable.
If someone is not sparkling, then he is both average and faithful.'''

fact_2 = "Wade is faithful."

explain_2 = '''Information extracted from the given fact:
**Wade**: *faithful*.

Information extracted from the given rules:
Someone being both fearless and reasonable is equivalent to being not sparkling. -- 'equivalent to' is biconditional. The conditions are (1) *fearless* and *reasonable*. The given fact does not match any conditions in this case. Or (2) *not sparkling*. The given fact does not match any conditions in this case.
Tyra is not fearless and Cara is bewildered if and only if Tyra is not sparkling and Lewis is reasonable. -- 'if and only if' is biconditional. The conditions are (1) *Tyra not fearless* and *Cara bewildered*. The given fact does not match any conditions in this case. Or (2) *Tyra not sparkling* and *Lewis reasonable*. The given fact does not match any conditions in this case.
If all people are fearless, then Tyra is reasonable. -- The condition has *all people*, which is considered as a universal quantifier. The given fact does not match any conditions.
If Tyra is either fearless or faithful, then Tyra is not bewildered and Nigel is reasonable. -- The condition is *Tyra fearless* or *Tyra faithful*. The given fact does not match any conditions.
If someone is not sparkling, then he is both average and faithful. -- The condition is *not sparkling*. The given fact does not match any conditions.
'''

output_2 = "None"

#######################################


#######################################
rules_3 = '''If there is at least one people who is different or short, then Wiley is talkative.
If everyone is talkative or not poised, then Rosa is not angry.
If someone is short and not shiny, then he is not angry, and vice versa.
If Dan is shiny or Adler is different, then Wiley is short.'''

fact_3 = "Rosa is short."

explain_3 = '''Information extracted from the given fact:
**Rosa**: *short*.

Information extracted from the given rules:
If there is at least one people who is different or short, then Wiley is talkative. -- The condition equals to *different* or *short*. The given fact matches full condition.
If everyone is talkative or not poised, then Rosa is not angry. -- The condition is *talkative* or *not poised*. The given fact does not match any conditions.
If someone is short and not shiny, then he is not angry, and vice versa. -- 'vice versa' is biconditional. The conditions are (1) *short* and *not shiny*. The given fact matches partial condition in this case. Or (2) *not angry*. The given fact does not match any conditions in this case.
If Dan is shiny or Adler is different, then Wiley is short. -- The condition is *Dan shiny* or *Adler different*. The given fact does not match any conditions.
'''

output_3 = '''If there is at least one people who is different or short, then Wiley is talkative.
If someone is short and not shiny, then he is not angry, and vice versa.'''
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

forward_selection_system_prompt ='''Imagine you are one of the greatest AI scientists. You are given **a fact** and **a list of rules** (each rule being a premise with condition(s)). Your task is to evaluate each rule in the list and select those that meet *any* of the following requirements:
- Full Condition Match: The fact fully and directly satisfies all condition(s) of the rule, allowing a valid derivation to obtain a new proposition.
- Partial Condition Match: The fact directly satisfies some, but not all, conditions of the rule. This means that additional fact(s) would be required to make a full derivation and obtain a new proposition.

If no rule is selected, return **None**.'''