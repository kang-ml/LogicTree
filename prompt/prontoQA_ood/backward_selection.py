################### 
# demo_1
fact_collection_1 = '''Sally is a brimpus.
Sally is a lorpus.
Sally is a shumpus.
Sally is a zumpus, a wumpus, and a lorpus.
Sally is a gorpus and Sally is not a numpus and Sally is a vumpus.
Sally is a tumpus.
Sally is a yumpus.'''

curr_path_1 = '''Sally is a lorpus.
Everything that is a lorpus, a shumpus, and a brimpus is an impus.'''

fact_to_derive_1 = '''Sally is an impus.'''

fact_to_search_1 = '''Sally is a shumpus. Sally is a brimpus.'''

if_fact_exist_1 = 'True\nThe identified missing conditions in the fact repository: Sally is a shumpus. Sally is a brimpus.'
################### 


################### 
# demo_2
fact_collection_2 = '''Polly is a shumpus.
Polly is a gorpus.
Polly is a vumpus.
Polly is a impus and Polly is a wumpus and Polly is not a tumpus.'''

curr_path_2 = '''Polly is a jompus.
Everything that is a shumpus, an impus, and a jompus is a numpus.'''

fact_to_derive_2 = '''Polly is a numpus.'''

fact_to_search_2 = '''Polly is a shumpus. Polly is a impus.'''

if_fact_exist_2 = 'True\nThe identified missing conditions in the fact repository: Polly is a shumpus. Polly is a impus.'
################### 


################### 
# demo_3
fact_collection_3 = '''Alex is a shumpus, an impus, and a vumpus.
Alex is not a wumpus, Alex is a lempus, and Alex is a dumpus.'''

curr_path_3 = '''Alex is a shumpus, an impus, and a vumpus.
Everything that is a shumpus, an impus, and a jompus is a tumpus.'''

fact_to_derive_3 = 'None'

fact_to_search_3 = '''Alex is a jompus.'''

if_fact_exist_3 = 'False'
###################


###################
# demo_4
fact_collection_4 = '''Sam is a brimpus and a lempus and a jompus.
Sam is a wumpus and Sam is not a yumpus and Sam is a gorpus.'''

curr_path_4 = '''Sam is a brimpus and a lempus and a jompus.
Everything that is a lempus and a yumpus and a jompus is a sterpus.'''

fact_to_derive_4 = 'None'

fact_to_search_4 = '''Sam is a yumpus.'''

if_fact_exist_4 = 'False'
###################

backward_selection_demos = [{"facts": fact_collection_1,
                            "curr_path": curr_path_1,
                            "fact_to_derive": fact_to_derive_1,
                            "fact_to_search": fact_to_search_1,
                            "ans": if_fact_exist_1},
                            
                            {"facts": fact_collection_2,
                            "curr_path": curr_path_2,
                            "fact_to_derive": fact_to_derive_2,
                            "fact_to_search": fact_to_search_2,
                            "ans": if_fact_exist_2},
                            
                            {"facts": fact_collection_3,
                            "curr_path": curr_path_3,
                            "fact_to_derive": fact_to_derive_3,
                            "fact_to_search": fact_to_search_3,
                            "ans": if_fact_exist_3},
                            
                            {"facts": fact_collection_4,
                            "curr_path": curr_path_4,
                            "fact_to_derive": fact_to_derive_4,
                            "fact_to_search": fact_to_search_4,
                            "ans": if_fact_exist_4},]

backward_selection_system_prompt = """Suppose you are one of the greatest AI scientists, logicians. Given a specific fact, a rule, and a repository of facts, your task is to identify the missing fact(s) required to fully satisfy the rule's conditions and determine if the missing fact(s) exist in the fact repository.
- The given one specific fact already satisfies one of the rule's conditions. Identify the missing fact(s) needed to deduce the rule.
- Automatically adapt pronouns (e.g., "each," "everything") to the correct subject based on the context of the given rule and the given fact.
- Check if the missing fact(s) are present in the fact repository.
    - If the missing fact(s) are present in the fact repository, return **True** and the identified missing fact(s), along with the deduction result.
    - Otherwise, return **False**, along with the deduction result **None**."""