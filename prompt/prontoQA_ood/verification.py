verification_demos = [
         {'proposition': "Wren is a tumpus.",
          'conclusion': "Wren is a tumpus.",
          'explanation': 'Both subject *Wren* and attribute *tumpus* are the same.',
          'ans': "Same"},

         {'proposition': "Max is a sterpus.",
          'conclusion': "Max is a lorpus or a sterpus or a tumpus.",
          'explanation': 'The subject *Max* is the same. The attribute in the Conclusion *lorpus* or *sterpus* or *tumpus* matches the attribute *sterpus* in the Proposition.',
          'ans': "Same"},

         {'proposition': "Fae is a brimpus, a zumpus, and a shumpus.",
          'conclusion': "Fae is a shumpus.",
          'explanation': 'The subject *Fae* is the same. The attribute in the Conclusion *shumpus* is a subset of the attributes *brimpus* and *zumpus* and *shumpus* in the Proposition',
          'ans': "Same"},

         {'proposition': "Wren is not mean.",
          'conclusion': "Wren is mean.",
          'explanation': 'The subject *Wren* is the same, and the attributes *not mean* and *mean* directly contradict each other.',
          'ans': "Opposite"},

         {'proposition': "Tim is not young.",
          'conclusion': "Tim is young.",
          'explanation': 'The subject *Tim* is the same, and the attributes *not young* and *young* directly contradict each other.',
          'ans': "Opposite"},
          
         {'proposition': "Fae is a vumpus.",
          'conclusion': "Fae is a yumpus.",
          'explanation': '*vumpus* and *yumpus* are unrelated attributes.',
          'ans': "Indeterminate"},

         {'proposition': "Fae is a brimpus, a zumpus, and a shumpus.",
          'conclusion': "Fae is a jompus.",
          'explanation': 'The attribute in the Conclusion *jompus* does not match any attribute *brimpus* *zumpus* *shumpus* in the Proposition.',
          'ans': "Indeterminate"},
        ]

verification_system_prompt = '''Suppose you are one of the greatest AI scientists, logicians. Your task is to classify the relationship between a given **Proposition** and a **Conclusion**. 
There are three possibilities:
1. **Same**: The **Proposition** can validate the **Conclusion**. This includes cases where:
    - The **Conclusion** has direct same subject and attributes (adjectives) as the **Proposition**. 
    - The subject is the same and the **Conclusion** attribute (adjective) is a subset of the attributes (adjectives) in the **Proposition**.
    - The subject is the same and one branch of the "or" statement in **Conclusion** attributes matches the attribute in the **Proposition**.
2. **Opposite**: The **Proposition** directly contradicts the **Conclusion**. The subjects are the same, but the attributes (adjectives) are in direct opposition, i.e., *attribute* versus *not attribute*.
3. **Indeterminate**: Neither **Same** nor **Opposite**. The **Proposition** and the **Conclusion** either have different subjects/attributes (adjectives) or there is no clear relationship between them.

For your classification:
- Compare the subject and attributes (adjectives) carefully.
- If the subjects are the same but the attributes (adjectives) are different, and neither **Same** nor **Opposite** can be determined, classify the relationship as **Indeterminate**.
- Ensure that unrelated attributes are NOT classified as **Same** or **Opposite**.'''