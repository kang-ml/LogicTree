none_type = {'A': 'A. **Partial Information Met**: The subject meets some but not all conditions of the one additional premise.',
             'B': 'B. **No Information Met**: The subject does not meet any conditions of the one additional premise.'}

derivation_demos = [{"premise_list": "Bob is round.",
                    "one_premise": "Round people are young.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*round*.\n\nFacts from the given **Set of Premises**:\n1. **Bob**: *round*.",
                    "ans": "Bob is young."},

                    {"premise_list": "The tiger likes the cow.",
                    "one_premise": "If the tiger likes the cow, then the tiger is hungry.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*the tiger likes the cow*.\n\nFacts from the given **Set of Premises**:\n1. **The tiger**: *likes the cow*.",
                    "ans": "The tiger is hungry."},
                    
                    ####
                    {"premise_list": "The rabbit is smart.",
                    "one_premise": "All smart people are cold.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*smart*.\n\nFacts from the given **Set of Premises**:\n1. **The rabbit**: *smart*.",
                    "ans": "The rabbit is cold."},
                    ####

                    {"premise_list": "The tiger likes the cow. The tiger likes the squirrel.",
                    "one_premise": "If something likes both the squirrel and the cow, then it visits the tiger.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*likes the squirrel* and *likes the cow*.\n\nFacts from the given **Set of Premises**:\n1. **The tiger**: *likes the cow*, *likes the squirrel*.",
                    "ans": "The tiger visits the tiger."},
                    
                    ####
                    {"premise_list": "Tom is blue. Tom is round.",
                    "one_premise": "If someone is round and not red then they are smart.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*round* and *not red*.\n\nFacts from the given **Set of Premises**:\n1. **Tom**: *blue*, *round*.",
                    "ans": f"None\nThe condition(s) in the one additional premise: **round**, **not red** (**not red** is not equivalent to **blue**).\nReason: {none_type['A']}"},
                    ####

                    {"premise_list": "Bob is round.",
                    "one_premise": "If someone is round and smart then they are not red.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*round* and *smart*.\n\nFacts from the given **Set of Premises**:\n1. **Bob**: *round*.",
                    "ans": f"None\nThe condition(s) in the one additional premise: **round**, **smart**.\nReason: {none_type['A']}"},
                    
                    ####
                    {"premise_list": "The dog sees the rabbit.",
                    "one_premise": "If something (someone) sees the rabbit then the rabbit is cold.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*sees the rabbit*.\n\nFacts from the given **Set of Premises**:\n1. **The dog**: *sees the rabbit*.",
                    "ans": "The rabbit is cold."},
                    ####

                    {"premise_list": "Bob is round.",
                    "one_premise": "If someone is tall, they are round.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*tall*.\n\nFacts from the given **Set of Premises**:\n1. **Bob**: *round*.",
                    "ans": f"None\nThe condition(s) in the one additional premise: **tall**.\nReason: {none_type['B']}"},

                    {"premise_list": "Dave is kind. Dave is red. Red, kind people are big. Big people are smart.",
                    "one_premise": "Smart, kind people are young",
                    "info_extract": "Conditions from **One Additional Premise**:\n*smart* and *kind*.\n\nFacts from the given **Set of Premises**:\n1. **Dave**: *kind*, *red*, *big*, *smart*.",
                    "ans": "Dave is young."},

                    {"premise_list": "Alice is happy.",
                    "one_premise": "If Alice is sad and red, she is quiet.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*sad* and *red*.\n\nFacts from the given **Set of Premises**:\n1. **Alice**: *happy*.",
                    "ans": f"None\nThe condition(s) in the one additional premise: **sad**, **red**.\nReason: {none_type['B']}"},

                    {"premise_list": "Erin is tall. Tall people are cold. Erin is cold.",
                    "one_premise": "Cold, young people are not furry.",
                    "info_extract": "Conditions from **One Additional Premise**:\n*cold* and *young*.\n\nFacts from the given **Set of Premises**:\n1. **Erin**: *tall*, *cold*.",
                    "ans": f"None\nThe condition(s) in the one additional premise: **cold**, **young**.\nReason: {none_type['A']}"},]

derivation_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to derive a new **Proposition** based on a given **Set of Premises** and **One Additional Premise**.
Follow these instructions carefully:
1. **Derive a Proposition** that logically follows from both the **Set of Premises** and the **One Additional Premise**.
2. Ensure that the **Proposition**:
- Must be a valid logical deduction from the provided **Set of Premises** and the **One Additional Premise**.
- Must not duplicate any of the provided **Set of Premises**.
- Must not include any information not directly deduced from the provided premises.
- Automatically adapt pronouns (e.g., 'they', 'something', 'someone') to the correct subject based on the context.
3. **Do not apply a rule or condition unless all conditions of the rule are met by the subject.** For example, if a condition states "If someone is round and smart," and the subject is not round or smart, this condition should not be applied.
4. If no new **Proposition** can be derived, return **None**, and classifiy the reason into one of the following categories:
- A. **Partial Information Met**: The subject meets some but not all conditions of the one additional premise.
- B. **No Information Met**: The subject does not meet any conditions of the one additional premise.'''