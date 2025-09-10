from guidance import gen, system, user, assistant
import guidance

@guidance
def derivation_maker(lm, system_prompt, demos, parent_node_path, node, temp=0.1):
    with system():
        lm += system_prompt

    #################################################
    for demo in demos:
        premise_list = demo['premise_list']
        one_premise = demo['one_premise']
        info_extract = demo['info_extract']
        ans = demo['ans']

        with user():
            lm += f"The given set of premises:\n{premise_list}"

        with user():
            lm += f"One additional premise:\n{one_premise}"

        with user():
            lm += "Key Information Extracted:"

        with assistant():
            lm += info_extract

        with user():
            lm += "The derived proposition is:"

        with assistant():
            lm += ans

    #################################################

    with user():
        lm += f"The given set of premises:\n{parent_node_path}"

    with user():
        lm += f"One additional premise:\n{node}"

    with user():
        lm += "Key Information Extracted:"

    with assistant():
        lm += gen('info_extract', temperature=temp)

    with user():
        lm += "The derived proposition is:"

    with assistant():
        lm += gen('ans', temperature=temp)

    return lm