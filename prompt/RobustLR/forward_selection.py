#######################################
rules_1 = '''Bob is not cold if Harry is the aunt of Charlie.
Charlie is not cold if Gary is not big.
Erin is not Dave's uncle if Gary is big.
If Dave is big and The uncle of Harry is Gary then The aunt of Charlie is Harry.
Gary is big if Erin is not the uncle of Dave.'''

fact_1 = "Gary is not big."

explain_1 = '''Bob is not cold if Harry is the aunt of Charlie. -- The condition is *Harry is the aunt of Charlie*. The given fact does not match any condition. The result is *Bob is not cold*. The given fact does not match the negation of the result.
Charlie is not cold if Gary is not big. -- The condition is *Gary is not big*. The given fact matches full condition.
Erin is not Dave's uncle if Gary is big. -- The condition is *Gary is big*. The given fact does not match any condition. The result is *Erin is not Dave's uncle*. The given fact does not match the negation of the result.
If Dave is big and The uncle of Harry is Gary then The aunt of Charlie is Harry. -- The condition is *Dave is big* and *The uncle of Harry is Gary*. The given fact does not match any conditions. The result is *The aunt of Charlie is Harry*. The given fact does not match the negation of the result.
Gary is big if Erin is not the uncle of Dave. -- The condition is *Erin is not the uncle of Dave*. The given fact does not match any condition. The result is *Gary is big*. The given fact matches the negation of the result.
'''

output_1 = '''Charlie is not cold if Gary is not big.
Gary is big if Erin is not the uncle of Dave.'''
#######################################


#######################################
rules_2 = '''The aunt of Anne is not Bob if Anne is not the mother of Harry.
Anne is not Harry's mother if Gary is the grandfather of Harry.
Erin is smart if Erin is not Dave's grandmother.
If Bob is not the aunt of Anne then Erin is not the grandmother of Dave.'''

fact_2 = "Anne is the aunt of Charlie."

explain_2 = '''The aunt of Anne is not Bob if Anne is not the mother of Harry. -- The condition is *Anne is not the mother of Harry*. The given fact does not match any condition. The result is *The aunt of Anne is not Bob*. The given fact does not match the negation of the result.
Anne is not Harry's mother if Gary is the grandfather of Harry. -- The condition is *Gary is the grandfather of Harry*. The given fact does not match any condition. The result is *Anne is not Harry's mother*. The given fact does not match the negation of the result.
Erin is smart if Erin is not Dave's grandmother. -- The condition is *Erin is not Dave's grandmother*. The given fact does not match any condition. The result is *Erin is smart*. The given fact does not match the negation of the result.
If Bob is not the aunt of Anne then Erin is not the grandmother of Dave. -- The condition is *Bob is not the aunt of Anne*. The given fact does not match any condition. The result is *Erin is not the grandmother of Dave*. The given fact does not match the negation of the result.
'''

output_2 = "None"
#######################################


#######################################
rules_3 = '''Erin is not Anne's aunt if Harry is not quiet.
If Anne's grandfather is Erin and Erin is smart then Erin is not Dave's grandmother.
If Anne is not smart then Harry is not quiet.
If Erin is red or Erin is Anne's grandfather then Anne is not smart.'''

fact_3 = "Erin is the grandfather of Anne."

explain_3 = '''Erin is not Anne's aunt if Harry is not quiet. -- The condition is *Harry is not quiet*. The given fact does not match any condition. The result is *Erin is not Anne's aunt*. The given fact does not match the negation of the result.
if Anne's grandfather is Erin and Erin is smart then Erin is not Dave's grandmother. -- The conditions are *Anne's grandfather is Erin* and *Erin is smart*. The given fact matches partial condition.
If Anne is not smart then Harry is not quiet. -- The condition is *Anne is not smart*. The given fact does not match any condition. The result is *Harry is not quiet*. The given fact does not match the negation of the result.
If Erin is red or Erin is Anne's grandfather then Anne is not smart. -- The condition is *Erin is red* or *Erin is Anne's grandfather*. The given fact matches full condition.
'''

output_3 = '''if Anne's grandfather is Erin and Erin is smart then Erin is not Dave's grandmother.
If Erin is red or Erin is Anne's grandfather then Anne is not smart.'''
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

If no rule is selected, return **None**.'''