#######################################
rules_1 = '''Everything that is a numpus or an impus or a lempus is a jompus and a dumpus and a brimpus.
Everything that is a yumpus and a numpus is a rompus.
Each brimpus is a gorpus.
Numpuses are numpuses.'''

fact_1 = "Alex is a numpus."

explain_1 = '''Everything that is a numpus or an impus or a lempus is a jompus and a dumpus and a brimpus. -- The condition: *numpus* or *impus* or *lempus*. The given fact matches full condition.
Everything that is a yumpus and a numpus is a rompus. -- The conditions: *yumpus* and *numpus*. The given fact matches partial condition.
Each brimpus is a gorpus. -- The condition: *brimpus*. The given fact does not match any conditions. The result is *gorpus*. The given fact does not match the negation of the result.
Numpuses are numpuses. -- The condition: *numpuses*. The given fact matches full condition.
'''

output_1 = '''Everything that is a numpus or an impus or a lempus is a jompus and a dumpus and a brimpus.
Everything that is a yumpus and a numpus is a rompus.
Numpuses are numpuses.'''
#######################################


#######################################
rules_2 = '''Gorpuses are rompuses.
Everything that is a brimpus or a sterpus is a jompus.
Lorpuses are zumpuses, gorpuses, and sterpuses.'''

fact_2 = "Sam is a zumpus."

explain_2 = '''Gorpuses are rompuses. -- The condition: *gorpuses*. The given fact does not match any conditions. The result is *rompuses*. The given fact does not match the negation of the result.
Everything that is a brimpus or a sterpus is a jompus. -- The condition: *brimpus* or *sterpus*. The given fact does not match any conditions. The result is *jompus*. The given fact does not match the negation of the result.
Lorpuses are zumpuses, gorpuses, and sterpuses. -- The condition: *lorpuses*. The given fact does not match any conditions. The result is *zumpuses* *gorpuses* *sterpuses*. The given fact does not match the negation of the result.
'''

output_2 = "None"
#######################################


#######################################
rules_3 = '''Each sterpus is a lorpus.
Jompuses are dumpuses.
Numpuses are lempuses.
Lorpuses are sterpuses, yumpuses, and gorpuses.
Sterpuses are impuses and lempuses.'''

fact_3 = "Stella is not a lempus."

explain_3 = '''Each sterpus is a lorpus. -- The condition: *sterpus*. The given fact does not match any conditions. The result is *lorpus*. The given fact does not match the negation of the result.
Jompuses are dumpuses. -- The condition: *jompuses*. The given fact does not match any conditions. The result is *dumpuses*. The given fact does not match the negation of the result.
Numpuses are lempuses. -- The condition: *numpuses*. The given fact does not match any conditions. The result is *lempuses*. The given fact matches the negation of the result.
Lorpuses are sterpuses, yumpuses, and gorpuses. -- The condition: *lorpuses*. The given fact does not match any conditions. The result is *sterpuses* *yumpuses* *gorpuses*. The given fact does not match the negation of the result.
Sterpuses are impuses and lempuses. -- The condition: *sterpuses*. The given fact does not match any conditions. The result is *impuses* *lempuses*. The given fact matches the negation of the result.
'''

output_3 = '''Numpuses are lempuses.
Sterpuses are impuses and lempuses.'''
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
- Negation Result Match: The fact directly satisfies the negation result of the rule, allowing a contrapositive derivation to obtain the negation of the condition(s).

If no rule is selected, return **None**.

Note: Do not be distracted by plural forms (e.g., *numpus* and *numpuses* are considered the same).'''