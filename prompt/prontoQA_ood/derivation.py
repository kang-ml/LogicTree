none_type = {'A': 'A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.',
             'B': 'B. **No Information Met**: The facts do not meet any conditions of the one additional premise.'}

derivation_demos = [{"premise_list": "Alex is an impus.",
                    "one_premise": "Impuses are gorpuses.",
                    "info_extract": "The condition: *impuses*. The fact matches the condition.",
                    "ans": "Alex is a gorpus."},

                    {"premise_list": "Alex is an impus. Each impus is a wumpus. Alex is a wumpus. Each wumpus is a brimpus. Alex is a brimpus.",
                    "one_premise": "Everything that is a impus and a brimpus is a zumpus.",
                    "info_extract": "The conditions: *impus* and *brimpus*. The facts match the conditions.",
                    "ans": "Alex is a zumpus."},

                    {"premise_list": "Stella is not a lempus.",
                    "one_premise": "Every yumpus is a zumpus, lempus and gorpus.",
                    "info_extract": "The condition: *yumpus*. The fact does not match the condition. The results: *zumpus* and *lempus* and *gorpus*. The fact matches the negation of the results.",
                    "ans": "Stella is not a yumpus."},

                    {"premise_list": "Rex is not a lorpus.",
                    "one_premise": "Everything that is a vumpus, a brimpus, or a tumpus is a lorpus.",
                    "info_extract": "The condition: *vumpus* or *brimpus* or *tumpus*. The fact does not match the condition. The result: *lorpus*. The fact matches the negation of the result.",
                    "ans": "Rex is not a vumpus. And Rex is not a brimpus. And Rex is not a tumpus."},

                    {"premise_list": "Rex is a lorpus.",
                    "one_premise": "Everything that is a lorpus, a lempus, and a dumpus is a sterpus, a numpus, and a brimpus.",
                    "info_extract": "The conditions: *lorpus* and *lempus* and *dumpus*. The given fact matches partial condition. The results: *sterpus* and *numpus* and *brimpus*. The fact does not match the negation of the results.",
                    "ans": f"None\nReason: {none_type['A']}"},

                    {"premise_list": "Charlie is a yumpus.",
                    "one_premise": "Everything that is a lorpus and a yumpus and a gorpus is a shumpus.",
                    "info_extract": "The conditions: *lorpus* and *yumpus* and *gorpus* The given fact matches partial condition. The result: *shumpus*. The fact does not match the negation of the result.",
                    "ans": f"None\nReason: {none_type['A']}"},

                    {"premise_list": "Charlie is a impus.",
                    "one_premise": "Everything that is a brimpus or a sterpus or a yumpus is a zumpus.",
                    "info_extract": "The condition: *brimpus* or *sterpus* or *yumpus*. The fact does not match the condition. The result: *zumpus*. The fact does not match the negation of the result.",
                    "ans": f"None\nReason: {none_type['B']}"},

                    {"premise_list": "Alex is not a wumpus.",
                    "one_premise": "Each wumpus is a brimpus.",
                    "info_extract": "The condition: *wumpus*. The fact does not match the condition. The result: *brimpus*. The fact does not match the negation of the result.",
                    "ans": f"None\nReason: {none_type['B']}"},
                    
                    {"premise_list": "Alex is a brimpus.",
                    "one_premise": "Each wumpus is a brimpus.",
                    "info_extract": "The condition: *wumpus*. The fact does not match the condition. The result: *brimpus*. The fact does not match the negation of the result.",
                    "ans": f"None\nReason: {none_type['B']}"},]

derivation_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to derive a new **Proposition** based on a given **Set of Premises** and **One Additional Premise**.
Follow these steps:
1. Extract condition(s) and result(s) from the **One Additional Premise**, then compare them with the facts in the **Set of Premises** to check for a match.

2. Derive a New Proposition:
- Deduce a valid **Proposition** if the fact(s) meet all conditions (or any branch of an "or" condition) as specified in the **One Additional Premise**.
- The match must be exact (subjects, negation or non-negation, attributes/adjectives).
- Do not duplicate from the **Set of Premises** or invent information beyond the premises.
- Adjust pronouns (e.g., "each," "everything") to match the correct subject in context.

3. If no new **Proposition** can be derived:
- Return **None**, and classifiy the reason into one of the following categories:
    - A. **Partial Information Met**: The facts meet some but not all conditions of the one additional premise.
    - B. **No Information Met**: The facts do not meet any conditions of the one additional premise.
    
Note: Do not be distracted by plural forms (e.g., *numpus* and *numpuses* are considered the same).'''