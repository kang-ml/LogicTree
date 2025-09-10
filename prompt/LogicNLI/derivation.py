none_type = {'A': 'A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.',
             'B': 'B. **No Information Met**: The facts do not meet any conditions of the one additional premise.'}

derivation_demos = [{"premise_list": "Adler is angry.",
                    "one_premise": "If someone is short and not shiny, then he is angry, and vice versa.",
                    "info_extract": "Facts from the given **Set of Premises**:\n*Adler angry*.\n\nConditions from **One Additional Premise**:\n'vice versa' is biconditional. (1) *short* and *not shiny*. Or (2) *angry*.",
                    "ans": "Adler is short and not shiny."},

                    {"premise_list": "Adler is angry. If there is at least one people who is angry, then Dan is poised and not talkative. Dan is poised and not talkative.",
                    "one_premise": "If someone is poised and not talkative, then he is different and short.",
                    "info_extract": "Facts from the given **Set of Premises**:\n*Adler angry* and *Dan poised* and *Dan not talkative*.\n\nConditions from **One Additional Premise**:\n*poised* and *not talkative*.",
                    "ans": "Dan is different and short."},

                    {"premise_list": "Dan is poised.",
                    "one_premise": "If there is at least one people who is different or poised, then Wiley is talkative.",
                    "info_extract": "Facts from the given **Set of Premises**:\n*Dan poised*.\n\nConditions from **One Additional Premise**:\n*different* or *poised*.",
                    "ans": "Wiley is talkative."},

                    {"premise_list": "Rosa is short.",
                    "one_premise": "If someone is short and not shiny, then he is not angry, and vice versa.",
                    "info_extract": "Facts from the given **Set of Premises**:\n*Rosa short*.\n\nConditions from **One Additional Premise**:\n'vice versa' is biconditional. (1) *short* and *not shiny*. Or (2) *not angry*.",
                    "ans": f"None\nReason: {none_type['A']}"},

                    {"premise_list": "Dan is poised.",
                    "one_premise": "If Blaine is poised and Blaine is not angry, then Rosa is different and Rosa is shiny.",
                    "info_extract": "Facts from the given **Set of Premises**:\n*Dan poised*.\n\nConditions from **One Additional Premise**:\n*Blaine poised* and *Blaine not angry*.",
                    "ans": f"None\nReason: {none_type['B']}"},]

derivation_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to derive a new **Proposition** based on a given **Set of Premises** and **One Additional Premise**.
Follow these steps:
1. Extract Key Information:
- List facts, i.e., subject(s) and their attributes (adjectives), from the **Set of Premises**.
- Identify the condition(s) required by the **One Additional Premise**.

2. Derive a New Proposition:
- Deduce a valid **Proposition** if the fact(s) meet all conditions as specified in the **One Additional Premise**.
- No synonyms or approximations are allowed. The match must be exact.
- Do not duplicate from the **Set of Premises** or invent information beyond the premises.
- Adjust pronouns (e.g., "they," "someone") to match the correct subject in context.

3. If no new **Proposition** can be derived:
- Return **None**, and classifiy the reason into one of the following categories:
    - A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.
    - B. **No Information Met**: The facts do not meet any conditions of the one additional premise.'''