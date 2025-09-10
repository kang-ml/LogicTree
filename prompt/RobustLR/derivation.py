none_type = {'A': 'A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.',
             'B': 'B. **No Information Met**: The facts do not meet any conditions of the one additional premise.'}

derivation_demos = [{"premise_list": "Anne is quiet. If Anne is quiet then Dave is red. Dave is red. Fiona is the son of Dave.",
                    "one_premise": "If Dave is red and Dave's son is Fiona then Charlie is not young.",
                    "info_extract": "Conditions from **One Additional Premise**: *Dave red* and *Dave's son is Fiona*.\nResult from **One Additional Premise**: *Charlie is not young*.\n\nMatched Fact from **Set of Premises**: *Dave is red* and *Fiona is the son of Dave*.",
                    "ans": "Charlie is not young."},

                    {"premise_list": "Charlie is not blue.",
                    "one_premise": "Charlie is blue if Fiona is not rough.",
                    "info_extract": "Conditions from **One Additional Premise**: *Fiona not rough*.\nResult from **One Additional Premise**: *Charlie is blue*.\n\nMatched Fact from **Set of Premises**: *Charlie is not blue*.",
                    "ans": "Fiona is rough."},

                    {"premise_list": "Anne is the aunt of Charlie.",
                    "one_premise": "Bob is not kind if Erin is smart or Anne is the aunt of Charlie.",
                    "info_extract": "Conditions from **One Additional Premise**: *Erin smart* or *Anne is the aunt of Charlie*.\nResult from **One Additional Premise**: *Bob is not kind*.\n\nMatched Fact from **Set of Premises**: *Anne is the aunt of Charlie*.",
                    "ans": "Bob is not kind."},

                    {"premise_list": "Harry is not young.",
                    "one_premise": "Bob is not green if Charlie is blue and Harry is not young.",
                    "info_extract": "Conditions from **One Additional Premise**: *Charlie is blue* and *Harry is not young*.\nResult from **One Additional Premise**: *Bob is not green*.\n\nMatched Fact from **Set of Premises**: *Harry is not young*.",
                    "ans": f"None\nReason: {none_type['A']}"},

                    {"premise_list": "Charlie is not furry.",
                    "one_premise": "If Charlie is not furry and Dave is young then Gary is big.",
                    "info_extract": "Conditions from **One Additional Premise**: *Charlie is not furry* and *Dave is young*.\nResult from **One Additional Premise**: *Gary is big*.\n\nMatched Fact from **Set of Premises**: *Charlie is not furry*.",
                    "ans": f"None\nReason: {none_type['A']}"},

                    {"premise_list": "Charlie is kind.",
                    "one_premise": "Anne is nice if Charlie is not kind.",
                    "info_extract": "Conditions from **One Additional Premise**: *Charlie is not kind*.\nResult from **One Additional Premise**: *Anne is nice*.\n\nNo Matched Fact from **Set of Premises**.",
                    "ans": f"None\nReason: {none_type['B']}"},

                    {"premise_list": "Charlie is not blue.",
                    "one_premise": "Bob is green if Charlie is blue or Gary is Bob's aunt.",
                    "info_extract": "Conditions from **One Additional Premise**: *Charlie is blue* or *Gary is Bob's aunt*.\nResult from **One Additional Premise**: *Bob is green*.\n\nNo Matched Fact from **Set of Premises**.",
                    "ans": f"None\nReason: {none_type['B']}"},]

derivation_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to derive a new **Proposition** based on a given **Set of Premises** and **One Additional Premise**.
Follow these steps:
1. Extract Key Information:
- From the **One Additional Premise**
    - Identify the required condition(s).
    - Identify the result of the condition(s).
- From the **Set of Premises**
    - Identify the matched fact(s).

2. Derive a New Proposition:
- Deduce a valid **Proposition** if the fact(s) meet all conditions (or any branch of an "or" condition) as specified in the **One Additional Premise**.
- The match must be exact (subjects, objects, relations, attributes).
- Do not duplicate from the **Set of Premises** or invent information beyond the premises.
- Adjust pronouns (e.g., "they," "someone") to match the correct subject in context.

3. If no new **Proposition** can be derived:
- Return **None**, and classifiy the reason into one of the following categories:
    - A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.
    - B. **No Information Met**: The facts do not meet any conditions of the one additional premise.'''