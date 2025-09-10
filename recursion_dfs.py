from guidance import models
import logging
import re

from LLM_modules.forward_selection_module import related_rule_searcher
from LLM_modules.derivation_module import derivation_maker
from LLM_modules.verification_module import verify_true_and_false, verifier
from rank_premise import rank_rules, extract_text_from_repo

def recursion(gpt_model, nlp, prompts, paths, premises, conclusion, gpt_query_cnt, fact_repo=None, fact_derive_hashmap=None, pseudo_deadends_repo=None, search_with_gpt=True, double_check_deadend=True):
    forward_selection_system_prompt = prompts['forward_selection_module']['system_prompt']
    forward_selection_demos = prompts['forward_selection_module']['demos']
    derivation_system_prompt = prompts['derivation_module']['system_prompt']
    derivation_demos = prompts['derivation_module']['demos']
    verification_system_prompt = prompts['verification_module']['system_prompt']
    verification_demos = prompts['verification_module']['demos']

    while paths:
        # for i in range(len(paths)):
            logging.info(f"**Current paths**:\n{paths}\n")
            path = paths.pop()
            parent_node = path[-1]

            ###################
            val_gpt = models.OpenAI(gpt_model)
            val_gpt.echo = False
            val_gpt += verifier(system_prompt=verification_system_prompt, demos=verification_demos, final_node=parent_node, final_conclusion=conclusion)
            conclusion_val = val_gpt['ans']
            gpt_query_cnt += 1
            ###################

            # first check if it can direct to conclusion
            if conclusion_val == 'Same':
                return 'True', path, gpt_query_cnt
            elif conclusion_val == 'Opposite':
                return 'False', path, gpt_query_cnt

            # can't direct to conclusion
            # then search for related nodes: related_nodes/None
            # then derive: derived_node/None
            else:
                
                # search for related nodes
                if search_with_gpt:
                    ###################
                    search_gpt = models.OpenAI(gpt_model)
                    search_gpt.echo = False
                    search_gpt += related_rule_searcher(system_prompt=forward_selection_system_prompt, demos=forward_selection_demos, query_rules=premises, query_fact=parent_node)
                    related_nodes = search_gpt['ans']
                    gpt_query_cnt += 1
                    ###################
                else:
                    related_nodes = premises

                if 'None' not in related_nodes:
                    related_nodes_lst = [line.strip().lstrip("- ") for line in related_nodes.strip().splitlines() if line]
                    
                    # If search without gpt, first remove the rules that have 0 connection score with the parent_node
                    if not search_with_gpt:
                        _, related_nodes_lst = rank_rules(nlp, related_nodes_lst, parent_node, remove_rule_with_zero_score=True)
 
                    ############################## Optimize
                    # Sort related_nodes_lst by the number of consecutive overlapping words with the conclusion --> [a, b, c]
                    _, related_nodes_lst = rank_rules(nlp, related_nodes_lst, conclusion, remove_rule_with_zero_score=False)
                    related_nodes_str = '\n'.join(related_nodes_lst)
                    logging.info(f"**Sorted (up-->down) related nodes for _{parent_node}_**:\n{related_nodes_str}\n")

                    # record the deeper path in the order of [c, b, a], since we use paths.pop() to get the last path
                    deeper_paths = []
                    ##############################
                    
                    for related_node in related_nodes_lst:
                        # make sure related_node is retrieved from premises
                        # note the related_node can be used multiple times but make sure the derived_node is new/not in the path
                        related_node = extract_text_from_repo(related_node, premises)
                        if related_node != None: # and related_node not in path:
                            path_nodes = ' '.join(path)
                            # try derivation
                            ###################
                            derive_gpt = models.OpenAI(gpt_model)
                            derive_gpt.echo = False
                            derive_gpt += derivation_maker(system_prompt=derivation_system_prompt, demos=derivation_demos, parent_node_path=path_nodes, node=related_node)
                            derive_node = derive_gpt['ans'].strip()
                            gpt_query_cnt += 1
                            ###################

                            # make sure its a valid derivation
                            if ('None' not in derive_node) and (derive_node not in path) and (derive_node != related_node):
                                path_copy = path.copy()
                                path_copy.append(related_node)
                                path_copy.append(derive_node)

                                ############################## Optimize
                                # instead of paths.append(path_copy), we append path_copy to deeper_paths
                                deeper_paths.insert(0, path_copy)
                                ##############################
                                
                                # add to fact_repo
                                # add to fact_derive_hashmap
                                if derive_node not in fact_repo:
                                    fact_repo.append(derive_node)
                                    fact_derive_hashmap[derive_node] = path_copy.copy()

                                ############################## Optimize
                                # Apply the rule-based method to check if the newly-derived fact is already the target statement
                                # can save derivation_maker queries and validator queries
                                result, _ = verify_true_and_false(fact_statements=derive_node, target_statement=conclusion)
                                if result == 'True':
                                    return 'True', path_copy, gpt_query_cnt
                                elif result == 'False':
                                    return 'False', path_copy, gpt_query_cnt
                                # elif result == 'Not found': go to validator
                                ##############################
                            
                            # if this can't be derived, get the none_type category
                            elif 'None' in derive_node:
                                none_type_match = re.search(r"Reason:\s*(\w)", derive_node)
                                none_type = none_type_match.group(1) if none_type_match else None
                                if none_type == 'A':
                                    # assert 'Partial Information Met' in derive_node, f"None type A should have Partial Information Met"
                                    path_copy = path.copy()
                                    path_copy.append(related_node)
                                    pseudo_deadends_repo.append(path_copy)

                                ##############################
                                # Double derive, only use parent_node and related_node to derive
                                elif double_check_deadend: # and (none_type == 'B'):
                                    # assert none_type == 'B', f"should be None type B"
                                    # assert 'No Information Met' in derive_node, f"None type B should have No Information Met"
                                    
                                    # try derivation
                                    ###################
                                    double_derive_gpt = models.OpenAI(gpt_model)
                                    double_derive_gpt.echo = False
                                    double_derive_gpt += derivation_maker(system_prompt=derivation_system_prompt, demos=derivation_demos, parent_node_path=parent_node, node=related_node)
                                    double_derive_node = double_derive_gpt['ans'].strip()
                                    gpt_query_cnt += 1
                                    ###################

                                    # make sure its a valid derivation
                                    if ('None' not in double_derive_node) and (double_derive_node not in path) and (double_derive_node != related_node):
                                        path_copy = path.copy()
                                        path_copy.append(related_node)
                                        path_copy.append(double_derive_node)

                                        ################### Optimize
                                        deeper_paths.insert(0, path_copy)
                                        ###################
                                        
                                        # add to fact_repo
                                        # add to fact_derive_hashmap
                                        if double_derive_node not in fact_repo:
                                            fact_repo.append(double_derive_node)
                                            fact_derive_hashmap[double_derive_node] = path_copy.copy()

                                        ################### Optimize
                                        # Apply the rule-based method to check if the newly-derived fact is already the target statement
                                        # can save derivation_maker queries and validator queries
                                        result, _ = verify_true_and_false(fact_statements=double_derive_node, target_statement=conclusion)
                                        if result == 'True':
                                            return 'True', path_copy, gpt_query_cnt
                                        elif result == 'False':
                                            return 'False', path_copy, gpt_query_cnt
                                        # elif result == 'Not found': go to validator
                                        ###################

                                    # if this can't be derived, get the none_type category
                                    elif 'None' in double_derive_node:
                                        double_none_type_match = re.search(r"Reason:\s*(\w)", double_derive_node)
                                        none_type = double_none_type_match.group(1) if double_none_type_match else None
                                        if none_type == 'A':
                                            # assert 'Partial Information Met' in derive_node, f"None type A should have Partial Information Met"
                                            path_copy = path.copy()
                                            path_copy.append(related_node)
                                            pseudo_deadends_repo.append(path_copy)
                                ##############################
                                    

                    paths.extend(deeper_paths)

                else:
                    logging.info(f"No related nodes for _{parent_node}_\n")

    return 'Unknown', None, gpt_query_cnt