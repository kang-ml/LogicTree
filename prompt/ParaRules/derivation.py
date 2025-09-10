none_type = {'A': 'A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.',
             'B': 'B. **No Information Met**: The facts do not meet any conditions of the one additional premise.'}

derivation_demos = [{"premise_list": "Thankfully Harry is nice; People have realized that he is big and rough; Since he is young he has tendency to become red when they mention it.",
                    "one_premise": "Big people with red hair are cold because they cannot find coats that fit.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*big*, *red*.\n\nFacts from the given **Set of Premises**:\n1. **Harry**: *nice*, *big*, *rough*, *young*, *red*.",
                    "ans": "Harry is cold."},

                    {"premise_list": "Eric is kind; He is also very cold and blue. A kind person who is down in the dumps and blue tends to have a rough side. Eric is rough.",
                    "one_premise": "Kind people with rough skin are usually red because it's wind burn.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*kind*, *rough*.\n\nFacts from the given **Set of Premises**:\n1. **Eric**: *kind*, *cold*, *blue*, *rough*.",
                    "ans": "Eric is red."},

                    {"premise_list": "As much as Harry is red, he is also nice and cold.",
                    "one_premise": "Someone that is cold, red and kind is also considered to be round.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*cold*, *red*, *kind*.\n\nFacts from the given **Set of Premises**:\n1. **Harry**: *red*, *nice*, *cold*.",
                    "ans": f"None\nReason: {none_type['A']}"},

                    {"premise_list": "That guy Bob sure is kind.",
                    "one_premise": "Young people who are both nice and cold also tend to be rough.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*young*, *nice*, *cold*.\n\nFacts from the given **Set of Premises**:\n1. **Bob**: *kind*.",
                    "ans": f"None\nReason: {none_type['B']}"},]

derivation_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to derive a new **Proposition** based on a given **Set of Premises** and **One Additional Premise**.
Follow these steps:
1. Extract Key Information:
- Identify the condition(s) required by the **One Additional Premise**.
- List facts, i.e., subject(s) and their attributes (adjectives), from the **Set of Premises**. Ignore verbs (e.g., "looks...", "acts...") and modifying words (e.g., "very...", "is likely...") and nouns (e.g., "...age") and conditions (e.g., "...when...") while focusing solely on the attributes (adjectives).

2. Derive a New Proposition:
- Deduce a valid **Proposition** if the fact(s) meet all conditions as specified in the **One Additional Premise**.
- No synonyms or approximations are allowed (e.g., nice != kind). The match must be exact.
- Do not duplicate from the **Set of Premises** or invent information beyond the premises.
- Adjust pronouns (e.g., "they," "someone") to match the correct subject in context.

3. If no new **Proposition** can be derived:
- Return **None**, and classifiy the reason into one of the following categories:
    - A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.
    - B. **No Information Met**: The facts do not meet any conditions of the one additional premise.'''