################### 
# demo_1
fact_collection_1 = '''The bear is nice.
The bear likes the cat.
The bear likes the tiger.
The cat eats the bear.
The cat is cold.
The cat is kind.
The cat likes the rabbit.
The cat visits the rabbit.
The rabbit likes the tiger.
The rabbit visits the tiger.
The tiger eats the bear.
The tiger likes the bear.
The tiger visits the cat.'''

curr_path_1 = '''The cat likes the rabbit.
If someone is cold and they like the rabbit then the rabbit likes the cat.'''

fact_to_derive_1 = '''The rabbit likes the cat.'''

fact_to_search_1 = '''The cat is cold.'''

if_fact_exist_1 = 'True\nThe identified missing condition in the fact repository: The cat is cold.'
################### 


################### 
# demo_2
fact_collection_2 = '''Anne is big.
Anne is young.
Charlie is blue.
Charlie is kind.
Charlie is round.
Charlie is young.
Gary is big.
Harry is big.
Harry is blue.
Harry is kind.
Harry is nice.
Harry is smart.
Anne is kind.'''

curr_path_2 = '''Anne is big.
If something is big then it is kind.
Anne is kind.
All young, kind things are blue.'''

fact_to_derive_2 = '''Anne is blue.'''

fact_to_search_2 = '''Anne is young.'''

if_fact_exist_2 = 'True\nThe identified missing condition in the fact repository: Anne is young.'
################### 


################### 
# demo_3
fact_collection_3 = '''The cow likes the rabbit.
The cow needs the mouse.
The mouse likes the squirrel.
The rabbit needs the cow.
The rabbit sees the cow.
The squirrel is nice.
The squirrel needs the cow.
The rabbit likes the squirrel.'''

curr_path_3 = '''The rabbit needs the cow.
If someone needs the cow then they like the squirrel.
The rabbit likes the squirrel.
If someone likes the squirrel and the squirrel sees the cow then they are red.'''

fact_to_derive_3 = 'None'

fact_to_search_3 = '''The squirrel sees the cow.'''

if_fact_exist_3 = 'False'
###################


###################
# demo_4
fact_collection_4 = '''The bear chases the lion.
The bear chases the mouse.
The bear is red.
The bear is round.
The bear needs the squirrel.
The lion eats the bear.
The lion is kind.
The lion needs the bear.
The mouse is round.
The squirrel chases the bear.
The lion eats the squirrel.'''

curr_path_4 = '''The lion eats the bear.
If something eats the bear and the bear eats the lion then the lion is round.'''

fact_to_derive_4 = 'None'

fact_to_search_4 = '''The bear eats the lion.'''

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
- Automatically adapt pronouns (e.g., 'they', 'something', 'someone') to the correct subject based on the context of the given rule and the given fact.
- Check if the missing condition is present in the fact repository.
    - If the missing condition is present in the fact repository, return **True** and the identified missing condition, along with the deduction result.
    - Otherwise, return **False**, along with the deduction result **None**."""