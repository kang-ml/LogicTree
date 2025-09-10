from guidance import gen, system, user, assistant
import guidance

@guidance
def related_rule_searcher(lm, system_prompt, demos, query_rules, query_fact, temp=0.1):
    with system():
        lm += system_prompt

    #################################################
    for demo in demos:
        rules = demo['rules']
        fact = demo['fact']
        explain = demo['explain']
        ans = demo['ans']

        with user():
            lm += f"The given fact:\n{fact}"

        with user():
            lm += f"The given list of rules:\n{rules}"

        with user():
            lm += f"Let's go through each rule from the given list of rules and think step by step."

        with assistant():
            lm += explain

        with user():
            lm += f"The selected rules (partial or full condition directly matched) are:"

        with assistant():
            lm += ans
    #################################################

    with user():
        lm += f"The given fact:\n{query_fact}"

    with user():
        lm += f"The given list of rules:\n{query_rules}"

    with user():
        lm += f"Let's go through each rule from the given list of rules and think step by step."
    
    with assistant():
        lm += gen('explain', temperature=temp)

    with user():
        lm += f"The selected rules (partial or full condition directly matched) are:"

    with assistant():
        lm += gen('ans', temperature=temp)

    return lm