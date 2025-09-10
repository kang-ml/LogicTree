################### 
# demo_1
fact_collection_1 = '''Adler is angry.
Wiley is short.
Rosa is short.
Rosa is not angry.
Rosa is not poised.
Wiley is not poised.
Adler is different.
Wiley is not angry.
Rosa is shiny.
Wiley is not different.
Cary is short.
Blaine is not different.
Dan is shiny.'''

curr_path_1 = '''Dan is shiny.
If Dan is shiny and Adler is different, then Wiley is short.'''

fact_to_derive_1 = '''Wiley is short.'''

fact_to_search_1 = '''Adler is different.'''

if_fact_exist_1 = 'True\nThe identified missing condition in the fact repository: Adler is different.'
################### 


################### 
# demo_2
fact_collection_2 = '''Molly is frank.
Joseph is not wonderful.
Jasper is not poised.
Rose is octagonal.
Juliana is not substantial.
Juliana is talkative.
Molly is wonderful.
Juliana is wonderful.
Clarence is substantial.
Clarence is not frank.
Rose is talkative.
Jasper is not wonderful.'''

curr_path_2 = '''Molly is wonderful.
Jasper being talkative is equivalent to Molly being wonderful and Clarence being substantial.'''

fact_to_derive_2 = '''Jasper is talkative.'''

fact_to_search_2 = '''Clarence is substantial.'''

if_fact_exist_2 = 'True\nThe identified missing condition in the fact repository: Clarence is substantial.'
################### 


################### 
# demo_3
fact_collection_3 = '''Tyra is not persistent.
Juliana is new.
Cyril is not persistent.
Christopher is new.
Unwin is new.
Cyril is southern.
Tyra is not new.
Christopher is southern.
George is not strong.
Montague is not attractive.
Cyril is not attractive.'''

curr_path_3 = '''George is not strong.
If someone is not strong and not persistent, then he is not southern, and vice versa.'''

fact_to_derive_3 = 'None'

fact_to_search_3 = '''George is not persistent.'''

if_fact_exist_3 = 'False'
###################


###################
# demo_4
fact_collection_4 = '''Eli is not average.
Lamont is not octagonal.
Janine is several.
Eli is hollow.
Janine is not hollow.
Juliana is not average.
Juliana is not fair.
Eli is several.
Christina is hollow.
Janine is civil.
Lamont is hollow.'''

curr_path_4 = '''Juliana is not average.
Someone being both several and not hollow is equivalent to being not civil and not average.'''

fact_to_derive_4 = 'None'

fact_to_search_4 = '''Juliana is not civil.'''

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