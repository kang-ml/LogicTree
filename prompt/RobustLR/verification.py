verification_demos = [
         {'proposition': "Fiona is not Bob's brother.",
          'conclusion': "Fiona is Bob's son.",
          'explanation': '*brother* and *son* are unrelated relations.',
          'ans': "Indeterminate"},

         {'proposition': "Charlie is Fiona's son.",
          'conclusion': "Gary is Fiona's son.",
          'explanation': '*Charlie* and *Gary* are different subjects.',
          'ans': "Indeterminate"},

         {'proposition': "Rosa is short.",
          'conclusion': "Rosa is short.",
          'explanation': 'Both subject *Rosa* and attribute *short* are the same.',
          'ans': "Same"},

         {'proposition': "The mother of Gary is not Charlie.",
          'conclusion': "Charlie is not the mother of Gary.",
          'explanation': 'The relation *not mother* between two people *Gary* and *Charlie* is the same',
          'ans': "Same"},

         {'proposition': "The mother of Anne is not Charlie.",
          'conclusion': "Charlie is the mother of Anne.",
          'explanation': 'The relations *not mother* and *mother* between two people *Anne* and *Charlie* directly contradict each other.',
          'ans': "Opposite"},

         {'proposition': "Paul not scared.",
          'conclusion': "Paul is scared.",
          'explanation': 'The subject *Paul* is the same, and the attributes *not scared* and *scared* directly contradict each other.',
          'ans': "Opposite"},          
          ]

verification_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to validate the relationship between a given **Proposition** and a **Conclusion**. There are three possibilities:
1. **Same**: The **Conclusion** has direct same subject and object and attributes (no synonym) as the **Proposition**. This includes cases where the Conclusion is a subset of the predicates (attributes) in the Proposition.
2. **Opposite**: The **Proposition** directly contradicts the **Conclusion**. The subjects (objects) are the same, but the predicates (attributes) are in direct opposition, i.e., 'predicate' versus 'not predicate'.
3. **Indeterminate**: Neither **Same** or **Opposite**. The **Proposition** and the **Conclusion** either have different subjects/predicates (attributes) or there is no clear relationship between them.

For your validation:
- Compare the subject and predicates (attributes) carefully.
- If the subjects are the same but the predicates (attributes) are different, and neither contradiction nor equivalence can be determined, classify the relationship as **Indeterminate**.
- Ensure that unrelated attributes/relations are NOT classified as **Same** or **Opposite**.'''