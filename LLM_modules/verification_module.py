from rank_premise import rank_rules
import guidance
from guidance import models, gen, system, user, assistant

def verify_true_and_false(fact_statements, target_statement):
    if target_statement in fact_statements:
        return 'True', target_statement

    # Check for the negated form in the premises
    negated_target_statement = None
    if 'not' in target_statement:
        if 'is not' in target_statement:
            negated_target_statement = target_statement.replace(" is not ", " is ")
        elif 'are not' in target_statement:
            negated_target_statement = target_statement.replace(" are not ", " are ")
    else:
        if 'is' in target_statement:
            negated_target_statement = target_statement.replace(" is ", " is not ")
        elif 'are' in target_statement:
            negated_target_statement = target_statement.replace(" are ", " are not ")
    

    if negated_target_statement and negated_target_statement in fact_statements:
        return 'False', negated_target_statement

    return 'Not found', None


def verify_unknown(nlp, rule_statements, target_statement):
    _, ranked_rules = rank_rules(nlp, rules=rule_statements.split('\n'), fact=target_statement, remove_rule_with_zero_score=True)
    if not ranked_rules:
        return 'Not found in rules'
    else:
        return 'Found in rules'
    
def verify_direct(gpt_model, nlp, prompts, fact_statements, rule_statements, target_statement, gpt_query_cnt):
    verification_system_prompt = prompts['verification_module']['system_prompt']
    verification_demos = prompts['verification_module']['demos']

    result, path = verify_true_and_false(fact_statements, target_statement)
    if result != 'Not found':
        return result, path, gpt_query_cnt

    result = verify_unknown(nlp, rule_statements, target_statement)
    if result == 'Not found in rules':
        fact_list = fact_statements.split('\n')
        _, ranked_fact_list = rank_rules(nlp, fact_list, target_statement, remove_rule_with_zero_score=True)
        for fact in ranked_fact_list:

            ###################
            val_gpt = models.OpenAI(gpt_model)
            val_gpt.echo = False
            val_gpt += verifier(system_prompt=verification_system_prompt, demos=verification_demos, final_node=fact, final_conclusion=target_statement)
            conclusion_val = val_gpt['ans']
            gpt_query_cnt += 1
            ###################

            # first check if it can direct to conclusion
            if conclusion_val == 'Same':
                return 'True', fact, gpt_query_cnt
            elif conclusion_val == 'Opposite':
                return 'False', fact, gpt_query_cnt
        return 'Unknown', None, gpt_query_cnt
    else:
        return 'Not found', None, gpt_query_cnt

@guidance
def verifier(lm, system_prompt, demos, final_node, final_conclusion, temp=0.1):
    with system():
        lm += system_prompt

    #################################################
    for demo in demos:
        proposition = demo['proposition']
        conclusion = demo['conclusion']
        explanation = demo['explanation']
        ans = demo['ans']

        with user():
            lm += f"Proposition:\n{proposition}"

        with user():
            lm += f"Conclusion:\n{conclusion}"

        with user():
            lm += "Validate the relationship between the given Proposition and the Conclusion, think about the reason:"

        with assistant():
            lm += explanation

        with assistant():
            lm += "So the relationship is:"

        with assistant():
            lm += ans
    #################################################

    with user():
        lm += f"Proposition:\n{final_node}"

    with user():
        lm += f"Conclusion:\n{final_conclusion}"

    with user():
        lm += "Validate the relationship between the given Proposition and the Conclusion, think about the reason:"

    with assistant():
        lm += gen('explain', temperature=temp)

    with assistant():
        lm += "So the relationship is:"

    with assistant():
        lm += gen('ans', temperature=temp)

    return lm