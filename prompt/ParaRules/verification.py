verification_demos = [
         {'proposition': "Erin is not round.",
          'conclusion': "Erin is not green.",
          'explanation': '*round* and *green* are unrelated attributes.',
          'ans': "Indeterminate"},

         {'proposition': "Anne is blue.",
          'conclusion': "Anne is green.",
          'explanation': '*blue* and *green* are considered as unrelated attributes. Only *blue* and *not blue* (*green* and *not green*) are considered as opposite attributes.',
          'ans': "Indeterminate"},

         {'proposition': "Tom is cold.",
          'conclusion': "Tom is cold.",
          'explanation': 'Both subject *Tom* and attribute *cold* are the same.',
          'ans': "Same"},

         ###
         {'proposition': "Tom feels cold.",
          'conclusion': "Tom is cold.",
          'explanation': 'Both subject *Tom* and attribute *cold* are the same.',
          'ans': "Same"},
         ###

         {'proposition': "Tom is cold and rough.",
          'conclusion': "Tom is cold.",
          'explanation': 'The subject *Tom* is the same. The attribute in the Conclusion *cold* is a subset of the attributes *cold* *rough* in the Proposition',
          'ans': "Same"},

         ###
         {'proposition': "Tom feels cold.",
          'conclusion': "Tom is not cold.",
          'explanation': 'The subject *Tom* is the same, and the attributes *cold* and *not cold* directly contradict each other.',
          'ans': "Opposite"},
         ###

         {'proposition': "Tim is not young.",
          'conclusion': "Tim is young.",
          'explanation': 'The subject *Tim* is the same, and the attributes *not young* and *young* directly contradict each other.',
          'ans': "Opposite"},
        
         {'proposition': "Tim is red and not young.",
          'conclusion': "Tim is young.",
          'explanation': 'The subject *Tim* is the same, and the attributes *not young* and *young* directly contradict each other.',
          'ans': "Opposite"}]

verification_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to validate the relationship between a given **Proposition** and a **Conclusion**. 
Only extract the subject and attributes (adjectives) from each statement to determine the relationship. Ignore verbs (e.g., "looks...", "acts...") and modifying words (e.g., "very...", "is likely...") and nouns (e.g., "...age") and conditions (e.g., "...when...") while focusing solely on the attributes (adjectives).
There are three possibilities:
1. **Same**: The **Conclusion** has direct same subject and attributes (no synonym) as the **Proposition**. This includes cases where the Conclusion is a subset of the attributes (adjectives) in the Proposition (e.g., "Tom is green and rough" → "Tom is green").
2. **Opposite**: The **Proposition** directly contradicts the **Conclusion**. The subjects are the same, but the attributes (adjectives) are in direct opposition, i.e., *adjective* versus *not adjective*.
3. **Indeterminate**: Neither **Same** nor **Opposite**. The **Proposition** and the **Conclusion** either have different attributes (adjectives) or there is no clear relationship between them.

For your validation:
- Compare the subject and attributes (adjectives) carefully.
- If the subjects are the same but the attributes (adjectives) are different, and neither contradiction nor equivalence can be determined, classify the relationship as **Indeterminate**.
- Ensure that unrelated attributes (e.g., *kind* and *nice*, *green* and *red*) are NOT classified as **Same** or **Opposite**.'''