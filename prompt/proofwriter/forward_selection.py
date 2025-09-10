#######################################
rules_1 = '''All red, round people are quiet.
Red people are young.
If someone is round and smart then they are not red.
All white people are red.
Quiet people are green.
If someone is red and not white then they are not green.
If someone likes the dog and they are red then they are blue.'''

fact_1 = "Bob is red."

explain_1 = '''All red, round people are quiet. -- The conditions are *red* and *round*. The given fact matches partial conditions.
Red people are young. -- The condition is *red*. The given fact matches full condition.
If someone is round and smart then they are not red. -- The conditions are *round* and *smart*. The given fact does not match any conditions.
All white people are red. -- The condition is *white*. The given fact does not match any conditions.
Quiet people are green. -- The condition is *quiet*. The given fact does not match any conditions.
If someone is red and not white then they are not green. -- The conditions are *red* and *not white*. The given fact matches partial condition.
If someone likes the dog and they are red then they are blue. -- The conditions are *likes the dog* and *red*. The given fact matches partial condition.
'''

output_1 = '''All red, round people are quiet.
Red people are young.
If someone is red and not white then they are not green.
If someone likes the dog and they are red then they are blue.'''
#######################################


#######################################
rules_2 = '''If something is furry and not blue then it is nice.
If Anne is furry then Anne is nice.
Smart, furry things are round.'''

fact_2 = "Anne is quiet."

explain_2 = '''If something is furry and not blue then it is nice. -- The conditions are *furry* and *not blue*. The given fact does not match any conditions.
If Anne is furry then Anne is nice. -- The condition is *furry*. The given fact does not match any conditions.
Smart, furry things are round. -- The conditions are *smart* and *furry*. The given fact does not match any conditions.
'''

output_2 = "None"

#######################################


#######################################
rules_3 = '''If something visits the tiger and the tiger is green then it is green.
If something likes the cat and the cat visits the cow then the cow is red.
If something is rough and it likes the mouse then the mouse visits the cow.
If something needs the cat then it likes the cat.'''

fact_3 = "The cow needs the cat."

explain_3 = '''If something visits the tiger and the tiger is green then it is green. -- The conditions are *visits the tiger* and *the tiger is green*. The given fact does not match any conditions.
If something likes the cat and the cat visits the cow then the cow is red. -- The conditions are *likes the cat* and *the cat visits the cow*. The given fact does not match any conditions.
If something is rough and it likes the mouse then the mouse visits the cow. -- The conditions are *rough* and *likes the mouse*. The given fact does not match any conditions.
If something needs the cat then it likes the cat. -- The condition is *needs the cat*. The given fact matches full condition.
'''

output_3 = '''If something needs the cat then it likes the cat.'''
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
If no rule is selected, return **None**.'''