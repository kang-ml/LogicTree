import logging
from verify_deadend import veirfy_pseudo_deadends
from recursion_dfs import recursion

def postprocess(fact_derive_hashmap, path):
    # fact_derive_hashmap: {node: [node1, node2]...}
    # path: list of nodes [node1, node2, ...]
    aug_path = []
    path_string = '\n'.join(path)

    for fact, derive_path in fact_derive_hashmap.items():
        derive_path_string = '\n'.join(derive_path)
        # the fact is in the path, but the derived path is not in the path
        if (fact.lower() in path_string.lower()) and (derive_path_string.lower() not in path_string.lower()):
            aug_path.append(derive_path_string)
    
    aug_path.append(path_string)
    return '\n\n'.join(aug_path)

def deduct_from_root(gpt_model, nlp, prompts, paths, data_info, gpt_query_cnt, fact_repo=None, fact_derive_hashmap=None, pseudo_deadends_repo=None, double_check_deadend=True):
    ###############
    # data info
    rule_statements = data_info['rule_statements']
    target_statement = data_info['target_statement']
    true_answer = data_info['true_answer']
    ###############   

    ###################
    # start reasoning inference
    logging.info(f'**Starting point**:\n{paths}\n')
    result, path, gpt_query_cnt_total = recursion(gpt_model, nlp, prompts, paths, premises = rule_statements, conclusion = target_statement, gpt_query_cnt = gpt_query_cnt, fact_repo=fact_repo, fact_derive_hashmap=fact_derive_hashmap, pseudo_deadends_repo=pseudo_deadends_repo, double_check_deadend=double_check_deadend)
    ###################


    ###################
    # if the results is "True" or "False"
    if result != 'Unknown':
        logging.info(f'Total GPT queries: {gpt_query_cnt_total}')
        logging.info(f"The prediction is: {result}")
        logging.info(f"The true answer is: {true_answer}")
        assert path is not None, "The path should not be None."
        logging.info("----------------------")
        logging.info("The path is:")
        postprocess_path = postprocess(fact_derive_hashmap, path)
        logging.info(postprocess_path)
        logging.info("----------------------")

        return result, gpt_query_cnt_total
    ###################

    ###################
    # if the results is "Unknown", have further check
    elif result == 'Unknown':
        assert paths == [], "The paths should be empty after the first round of reasoning."
        logging.info(f'---Starting verifying {result}---')
        
        aug_facts = '\n'.join(fact_repo)
        logging.info(f"**Augmented fact statements**:\n{aug_facts}\n")

        while pseudo_deadends_repo:
            result, paths, gpt_query_cnt_total = veirfy_pseudo_deadends(gpt_model, nlp, prompts, fact_repo, target_statement, fact_derive_hashmap, pseudo_deadends_repo, gpt_query_cnt_total)
            
            # check if the target statement is verified in veirfy_pseudo_deadends process
            if result != 'Unknown':
                logging.info(f'Total GPT queries: {gpt_query_cnt_total}')
                logging.info(f"The prediction is: {result}")
                logging.info(f"The true answer is: {true_answer}")
                logging.info("----------------------")
                logging.info("The path is:")
                postprocess_path = postprocess(fact_derive_hashmap, paths)
                logging.info(postprocess_path)
                logging.info("----------------------")
                
                return result, gpt_query_cnt_total

            assert pseudo_deadends_repo == [], "The pseudo deadends should be empty after verification."
            result, path, gpt_query_cnt_total = recursion(gpt_model, nlp, prompts, paths, premises = rule_statements, conclusion = target_statement, gpt_query_cnt = gpt_query_cnt_total, fact_repo=fact_repo, fact_derive_hashmap=fact_derive_hashmap, pseudo_deadends_repo=pseudo_deadends_repo, double_check_deadend=double_check_deadend)
            
            ###########
            # keep track of the augmented fact statements
            aug_facts = '\n'.join(fact_repo)
            logging.info(f"**Augmented fact statements**:\n{aug_facts}\n")
            ###########
            
            # check if the target statement is verified in recursion process
            if result != 'Unknown':
                logging.info(f'Total GPT queries: {gpt_query_cnt_total}')
                logging.info(f"The prediction is: {result}")
                logging.info(f"The true answer is: {true_answer}")
                assert path is not None, "The path should not be None."
                logging.info("----------------------")
                logging.info("The path is:")
                postprocess_path = postprocess(fact_derive_hashmap, path)
                logging.info(postprocess_path)
                logging.info("----------------------")
                
                return result, gpt_query_cnt_total
        
        # after exploring all the pseudo deadends, if the result is still "Unknown"
        assert result == 'Unknown', "The result is still 'Unknown' after exploring all the pseudo deadends."
        logging.info(f'GPT queries in the current stage ({result}): {gpt_query_cnt_total}\n')

        return result, gpt_query_cnt_total
    ###################