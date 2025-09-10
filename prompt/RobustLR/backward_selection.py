################### 
# demo_1
fact_collection_1 = '''Charlie is blue.
Harry is not young.'''

curr_path_1 = '''Harry is not young.
Bob is green if Charlie is blue and Harry is not young.'''

fact_to_derive_1 = '''Bob is green.'''

fact_to_search_1 = '''Charlie is blue.'''

if_fact_exist_1 = 'True\nThe identified missing condition in the fact repository: Charlie is blue.'
################### 


################### 
# demo_2
fact_collection_2 = '''Charlie is blue.
Charlie is the aunt of Dave.
The grandmother of Erin is Bob.'''

curr_path_2 = '''Charlie is blue.
If Charlie is blue and Bob is the grandmother of Erin then Anne is not quiet.'''

fact_to_derive_2 = '''Anne is not quiet.'''

fact_to_search_2 = '''Bob is the grandmother of Erin.'''

if_fact_exist_2 = 'True\nThe identified missing condition in the fact repository: The grandmother of Erin is Bob.'
################### 


################### 
# demo_3
fact_collection_3 = '''Charlie is not blue.
Harry is young.'''

curr_path_3 = '''Harry is young.
Bob is not green if Charlie is blue and Harry is young.'''

fact_to_derive_3 = 'None'

fact_to_search_3 = '''Charlie is blue.'''

if_fact_exist_3 = 'False'
###################


###################
# demo_4
fact_collection_4 = '''Charlie is blue.
Fiona is the son of Dave.'''

curr_path_4 = '''Fiona is the son of Dave.
If Dave is red and Fiona is the son of Dave then Charlie is not young.'''

fact_to_derive_4 = 'None'

fact_to_search_4 = '''Dave is red.'''

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

backward_selection_system_prompt = """Suppose you are one of the greatest AI scientists, logicians. Given a specific fact, a rule, and a repository of facts, your task is to identify the missing fact required to fully satisfy the rule's conditions and determine if this missing fact exists in the fact repository.
- The given one specific fact already satisfies one of the rule's conditions. Identify the missing condition needed to deduce the rule.
- Automatically adapt pronouns (e.g., 'they', 'someone') to the correct subject based on the context of the given rule and the given fact.
- Check if the missing condition is present in the fact repository.
    - If the missing condition is present in the fact repository, return **True** and the identified missing condition, along with the deduction result.
    - Otherwise, return **False**, along with the deduction result **None**."""