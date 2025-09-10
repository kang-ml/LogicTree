from guidance import gen, system, user, assistant
import guidance

@guidance
def missing_fact_searcher(lm, system_prompt, demos, aug_facts, pseudo_deadends_path, temp=0.1):
    with system():
        lm += system_prompt

    #################################################
    for demo in demos:
        facts = demo['facts']
        curr_path = demo['curr_path'].split("\n")
        fact_to_derive = demo['fact_to_derive']
        fact_to_search = demo['fact_to_search']
        ans = demo['ans']

        with user():
            lm += f"The given one specific fact:\n{curr_path[-2]}"

        with user():
            lm += f"The given rule:\n{curr_path[-1]}"

        with user():
            lm += f"Let's go through each condition of the given rule and identify the missing condition needed to deduce the rule."

        with user():
            lm += "The missing condition needed to deduce the rule is:"

        with assistant():
            lm += fact_to_search

        with user():
            lm += f"Check if the missing condition is present in the fact repository:\n{facts}"
        
        with assistant():
            lm += ans

        with user():
            lm += f"The deduction result is:"

        with assistant():
            lm += fact_to_derive
   
    #################################################

    with user():
        lm += f"The given one specific fact:\n{pseudo_deadends_path[-2]}"

    with user():
        lm += f"The given rule:\n{pseudo_deadends_path[-1]}"

    with user():
        lm += f"Let's go through each condition of the given rule and identify the missing condition needed to deduce the rule."

    with user():
        lm += "The missing condition needed to deduce the rule is:"

    with assistant():
        lm += gen('fact_to_search', temperature=temp)

    with user():
        lm += f"Check if the missing condition is present in the fact repository:\n{aug_facts}"

    with assistant():
        lm += gen('ans', temperature=temp)

    with user():
        lm += f"The deduction result is:"

    with assistant():
        lm += gen('fact_to_derive', temperature=temp)

    return lm