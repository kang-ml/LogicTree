verification_demos = [
         {'proposition': "Paul is civil.",
          'conclusion': "Paul is not scared.",
          'explanation': '"civil" and "not scared" are unrelated attributes.',
          'ans': "Indeterminate"},

         {'proposition': "Broderick is not scared.",
          'conclusion': "Paul is not scared.",
          'explanation': '"Broderick" and "Paul" are different subjects.',
          'ans': "Indeterminate"},

         {'proposition': "Rosa is short.",
          'conclusion': "Rosa is short.",
          'explanation': 'Both subject *Rosa* and attribute *short* are the same.',
          'ans': "Same"},

         {'proposition': "Blaine is angry and not different.",
          'conclusion': "Blaine is angry.",
          'explanation': 'The subject *Blaine* is the same. The attribute in the Conclusion *angry* is a subset of the attributes *angry* and *not different* in the Proposition',
          'ans': "Same"},

         {'proposition': "Broderick is not scared.",
          'conclusion': "Broderick is scared.",
          'explanation': 'The subject *Broderick* is the same, and the attributes *not scared* and *scared* directly contradict each other.',
          'ans': "Opposite"},

         {'proposition': "Paul is civil and not scared.",
          'conclusion': "Paul is scared.",
          'explanation': 'The subject *Paul* is the same, and the attributes *not scared* and *scared* directly contradict each other.',
          'ans': "Opposite"},          
          ]

verification_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to validate the relationship between a given **Proposition** and a **Conclusion**. There are three possibilities:
1. **Same**: The **Conclusion** has direct same subject and attributes (no synonym) as the **Proposition**. This includes cases where the Conclusion is a subset of the predicates (attributes) in the Proposition.
2. **Opposite**: The **Proposition** directly contradicts the **Conclusion**. The subjects are the same, but the predicates (attributes) are in direct opposition, i.e., 'predicate' versus 'not predicate'.
3. **Indeterminate**: Neither **Same** or **Opposite**. The **Proposition** and the **Conclusion** either have different subjects/predicates (attributes) or there is no clear relationship between them.

For your validation:
- Compare the subject and predicates (attributes) carefully.
- If the subjects are the same but the predicates (attributes) are different, and neither contradiction nor equivalence can be determined, classify the relationship as **Indeterminate**.
- Ensure that unrelated attributes are NOT classified as **Same** or **Opposite**.'''