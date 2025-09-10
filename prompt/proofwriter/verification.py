verification_demos = [{'proposition': "Erin is not round.",
                       'conclusion': "Erin is not green.",
                       'explanation': '"Round" and "Green" are unrelated attributes.',
                       'ans': "Indeterminate"},

                      {'proposition': "Anne is blue.",
                       'conclusion': "Anne is green.",
                       'explanation': '"Blue" and "Green" are considered as unrelated attributes. Only "Blue" and "Not blue" ("Green" and "Not green") are considered as opposite attributes.',
                       'ans': "Indeterminate"},

                      {'proposition': "The rabbit is cold.",
                       'conclusion': "The rabbit is cold.",
                       'explanation': 'Both subject and predicate are the same.',
                       'ans': "Same"},

                      {'proposition': "The tiger is not young.",
                       'conclusion': "The tiger is young.",
                       'explanation': 'The subject is the same, but the predicates "not young" and "young" directly contradict each other.',
                       'ans': "Opposite"}]

verification_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to validate the relationship between a given **Proposition** and a **Conclusion**. There are three possibilities:
1. **Same:** The **Proposition** is directly equivalent to the **Conclusion**, meaning both the subject and the predicate (attributes) are the same.
2. **Opposite:** The **Proposition** directly contradicts the **Conclusion**. The subjects are the same, but the predicates (attributes) are in direct opposition, such as 'predicate' versus 'not predicate'.
3. **Indeterminate:** Neither **Same** or **Opposite**. The **Proposition** and the **Conclusion** either have different predicates (attributes) or there is no clear relationship between them.

For your validation:
- Carefully compare both the subject and predicate in each statement.
- If the subjects are the same but the predicates (attributes) are different, and neither contradiction nor equivalence can be determined, classify the relationship as **Indeterminate**.
- Ensure that unrelated attributes (e.g., "green" and "round", "green" and "blue") are not classified as **Same** or **Opposite**.'''