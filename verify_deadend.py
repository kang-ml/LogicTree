from LLM_modules.backward_selection_module import missing_fact_searcher
from rank_premise import rank_deadends_paths, extract_text_from_repo
from LLM_modules.verification_module import verify_true_and_false
from guidance import models
import logging

def veirfy_pseudo_deadends(gpt_model, nlp, prompts, fact_repo, target_statement, fact_derive_hashmap, pseudo_deadends_repo, gpt_query_cnt):
    # fact_repo: list
    # pseudo_deadends_repo: list of list (path)

    """
    # for the last rule in the deadend, (A+B-->C), we only want to search once, i.e., either search A or B
    # as long as the same rule has appeared twice, it means its conditions (facts) are already in the fact_repo
    # this only operate at each level of the pseudo_deadends_repo
    # this happens *only* when the rule is able to makes the path becomes a valid path
    visited_rules = set()
    """
    backward_selection_system_prompt = prompts['backward_selection_module']['system_prompt']
    backward_selection_demos = prompts['backward_selection_module']['demos']

    paths = []
    aug_facts = '\n'.join(fact_repo)

    ############################## Optimize
    # sort the pseudo_deadends_repo
    rank_deadends_paths(nlp, pseudo_deadends_repo, target_statement)
    pseudo_deadends_str = '\n\n'.join(['\n'.join(path) for path in pseudo_deadends_repo])
    logging.info(f"**Sorted (down-->up) pseudo deadends**:\n{pseudo_deadends_str}\n\n")
    ##############################

    while pseudo_deadends_repo:
        pseudo_deadends_path = pseudo_deadends_repo.pop()

        re_search_gpt = models.OpenAI(gpt_model)
        re_search_gpt.echo = False

        # search for the missing condition
        re_search_gpt += missing_fact_searcher(backward_selection_system_prompt, backward_selection_demos, aug_facts, pseudo_deadends_path)
        gpt_query_cnt += 1

        fact_to_search = re_search_gpt['fact_to_search'].strip()
        ans = re_search_gpt['ans'].strip()
        fact_to_derive = re_search_gpt['fact_to_derive'].strip()
        
        # make sure the fact_to_search is not like "someone/they/somthing is ..."
        fact_to_search_1 = extract_text_from_repo(fact_to_search, aug_facts)
        fact_to_search_2 = extract_text_from_repo(ans, aug_facts)
        fact_to_search = fact_to_search_1
        if fact_to_search_1 == None and fact_to_search_2 != None:
            fact_to_search = fact_to_search_2

        if ('true' in ans.lower()) and (fact_to_search != None):
            assert fact_to_derive != "None", "The fact to derive should not be None."

            path_copy = pseudo_deadends_path.copy()
            rule = path_copy.pop()
            path_copy.append(fact_to_search)
            path_copy.append(rule)
            path_copy.append(fact_to_derive)
            
            """
            # keep the most possible path at the end
            paths.insert(0, path_copy)
            """

            # add to fact_repo
            # add to fact_derive_hashmap
            if fact_to_derive not in fact_repo:
                fact_repo.append(fact_to_derive)
                fact_derive_hashmap[fact_to_derive] = path_copy.copy()

                # keep the most possible path at the end, and avoid duplicated paths
                paths.insert(0, path_copy)


            ############################## Optimize
            # Apply the rule-based method to check if the newly-derived fact is already the target statement
            # can save derivation_maker queries and validator queries
            # path_copy is the target path, including the newly-derived fact
            result, _ = verify_true_and_false(fact_statements=fact_to_derive, target_statement=target_statement)
            if result == 'True':
                return 'True', path_copy, gpt_query_cnt
            elif result == 'False':
                return 'False', path_copy, gpt_query_cnt
            # elif result == 'Not found': go to validator
            ##############################
    
    # paths is the list of the paths
    return 'Unknown', paths, gpt_query_cnt


