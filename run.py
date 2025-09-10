import argparse
import importlib
from tqdm import tqdm
import time
import logging
import json
import os
import spacy

from LLM_modules.verification_module import verify_direct
from explore_from_root import deduct_from_root
from rank_premise import split_facts_based_on_subj_of_interest, rank_facts, check_if_need_other_facts

# Setup openai api key
os.environ["OPENAI_API_KEY"] = ""

def load_prompts(dataset: str):
    base_prompt_path = f"prompt.{dataset}"

    fs_module = importlib.import_module(f"{base_prompt_path}.forward_selection")
    der_module = importlib.import_module(f"{base_prompt_path}.derivation")
    ver_module = importlib.import_module(f"{base_prompt_path}.verification")
    bs_module = importlib.import_module(f"{base_prompt_path}.backward_selection")

    return {
        "forward_selection_module": {
            "system_prompt": fs_module.forward_selection_system_prompt,
            "demos": fs_module.forward_selection_demos,
        },
        "derivation_module": {
            "system_prompt": der_module.derivation_system_prompt,
            "demos": der_module.derivation_demos,
        },
        "verification_module": {
            "system_prompt": ver_module.verification_system_prompt,
            "demos": ver_module.verification_demos,
        },
        "backward_selection_module": {
            "system_prompt": bs_module.backward_selection_system_prompt,
            "demos": bs_module.backward_selection_demos,
        },
    }


def logictree(llm: str, spacy_model: str, dataset: str, test_range, max_queries, double_check_deadend):
    # Initialize SpaCy NLP model
    nlp = spacy.load(spacy_model)

    ##########################################
    # Load prompts
    prompts = load_prompts(dataset)

    ##########################################
    # Load dataset
    dataset_path = os.path.join("dataset", f"{dataset}.json")
    total_data = json.load(open(dataset_path))
    ans = {'A': "True", 'B': "False", 'C': 'Unknown'}

    total = 0
    correct = 0
    total_time = 0

    # Define test samples
    if test_range is None:
        sample_list = list(range(len(total_data)))
    else:
        sample_list = list(range(test_range[0], test_range[1]))
    ##########################################

    ######################################
    # Set up logging
    model_result_path = f"{llm}_results/{dataset}"
    if len(sample_list) == 1:
        file_name = f"{model_result_path}/single_sample_log_results/{sample_list[0]}_log.txt"
    else:
        file_name = f"{model_result_path}/multi_sample_log_results/{sample_list[0]}_{sample_list[-1]}_log.txt"

    # Ensure the directory exists before configuring logging
    log_dir = os.path.dirname(file_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.basicConfig(
        filename=file_name,
        filemode="w",
        level=logging.INFO,
        format="%(message)s"
    )
    ######################################

    for i in tqdm(range(len(sample_list))):
        idx = sample_list[i]
        total += 1

        ###############
        # start time info
        start_time = time.time()  # Start time for the iteration
        start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        logging.info(f"{start_time_str} - Start processing sample: {idx}\n")
        ###############

        ###############
        # data info
        data = total_data[idx]
        fact_statements = data['theory']['Fact'].replace(". ", ".\n").strip('\n')
        rule_statements = data['theory']['Rule'].replace(". ", ".\n").strip('\n')
        target_statement = data['question'].split('Based on the above information, is the following statement true, false, or unknown? ')[1]
        true_answer = ans[data['answer']]

        logging.info(f'**Facts**:\n{fact_statements}\n')
        logging.info(f'**Rules**:\n{rule_statements}\n')
        logging.info(f'**Question**:\n{target_statement}\n')

        print()
        print(f'Facts:\n{fact_statements}\n')
        print(f'Rules:\n{rule_statements}\n')
        print(f'Question:\n{target_statement}\n')

        data_info = {'fact_statements': fact_statements, 'rule_statements': rule_statements,
                     'target_statement': target_statement, 'true_answer': true_answer}
        ###############

        ###################
        # Use rule-based method (Spacy) to rank the facts.
        # The first group of facts are the ones including subjects of interest.
        # The second group of facts are the rest of the facts.
        fact_list = fact_statements.split('\n')
        rule_list = rule_statements.split('\n')

        doc = nlp(target_statement)
        subject = [token.lemma_ for token in doc if token.dep_ in {"nsubj", "nsubjpass"}][0]
        subj_facts, other_facts = split_facts_based_on_subj_of_interest(subject, fact_list)

        _, ranked_subj_facts = rank_facts(nlp, subj_facts, rule_list)
        _, ranked_other_facts = rank_facts(nlp, other_facts, rule_list, reference_entity=subject)
        check_other_facts = check_if_need_other_facts(nlp, rule_list)
        ###################

        gpt_query_cnt_total = 0

        ###################
        # first use rule-based method to check if the target statement is already in the fact statements
        result, path, gpt_query_cnt_total = verify_direct(llm, nlp, prompts, fact_statements, rule_statements,
                                                          target_statement, gpt_query_cnt=gpt_query_cnt_total)

        if (result != 'Not found') and (dataset != "prontoQA_ood"): # note: prontoQA_ood uses fictional words, so spacy doesn't work
            logging.info(f"Total GPT queries: {gpt_query_cnt_total}")
            logging.info(f"The prediction is: {result}")
            logging.info(f"The true answer is: {true_answer}")
            if path is not None:
                assert result != 'Unknown', "The result should not be Unknown."
                logging.info("----------------------")
                logging.info(f"The path is:\n{path}")
                logging.info("----------------------")
            if result == true_answer:
                correct += 1
        ###################

        else:
            ##### note: prontoQA_ood uses fictional words, so spacy for premise ranking doesn't work
            if dataset == "prontoQA_ood":
                ranked_subj_facts = fact_list.copy()
            #####

            result = 'Unknown'  # avoid result is "Not found"
            fact_repo = fact_statements.split('\n')
            # record the derived fact and their corresponding derive path
            fact_derive_hashmap = dict()
            pseudo_deadends_repo = []
            assert gpt_query_cnt_total == 0, "The gpt_query_cnt_total should be 0."

            ###################
            # get starting point with the same *subject* relation
            # start reasoning inference
            logging.info(f'Validating the subject starting points...')
            for subject_fact in ranked_subj_facts:
                assert pseudo_deadends_repo == [], "The pseudo deadends should be empty."
                paths = [[subject_fact]]
                result, gpt_query_cnt_total = deduct_from_root(llm, nlp, prompts, paths, data_info,
                                                               gpt_query_cnt=gpt_query_cnt_total,
                                                               fact_repo=fact_repo,
                                                               fact_derive_hashmap=fact_derive_hashmap,
                                                               pseudo_deadends_repo=pseudo_deadends_repo,
                                                               double_check_deadend=double_check_deadend)
                if result != 'Unknown':
                    break
            ###################

            ###################
            # if the results is "Unknown", have further check on other starting points
            if result == 'Unknown' and check_other_facts:
                logging.info(f'Validating the other starting points...')
                for other_fact in ranked_other_facts:
                    assert pseudo_deadends_repo == [], "The pseudo deadends should be empty."
                    paths = [[other_fact]]
                    result, gpt_query_cnt_total = deduct_from_root(llm, nlp, prompts, paths, data_info,
                                                                   gpt_query_cnt=gpt_query_cnt_total,
                                                                   fact_repo=fact_repo,
                                                                   fact_derive_hashmap=fact_derive_hashmap,
                                                                   pseudo_deadends_repo=pseudo_deadends_repo,
                                                                   double_check_deadend=double_check_deadend)
                    if result != 'Unknown':
                        break
                    # break if the total query count is larger than max_queries
                    if gpt_query_cnt_total > max_queries:
                        break
            ###################

            ###################
            if result == true_answer:
                correct += 1

            if result == 'Unknown':
                logging.info(f'Total GPT queries: {gpt_query_cnt_total}')
                logging.info(f"The prediction is: {result}")
                logging.info(f"The true answer is: {true_answer}")
            ###################

        print(f"The prediction for Sample {idx} is: {result}")
        print(f"The true answer for Sample {idx} is: {true_answer}")

        ###################
        # end time info
        end_time = time.time()  # End time for the iteration
        end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
        duration = (end_time - start_time) / 60  # Calculate time taken for the iteration
        logging.info(f"Sample {idx} processed in {duration:.2f} minutes")
        logging.info(f"{end_time_str} - End processing sample: {idx}\n\n\n")
        ###################

        total_time += duration

    print(f"Accuracy {correct}/{total}: {correct/total*100:.2f}%")
    logging.info(f"Accuracy {correct}/{total}: {correct/total*100:.2f}%")

    print(f"Average time {total_time:.2f}/{total}: {total_time/total:.2f} minutes")
    logging.info(f"Average time {total_time:.2f}/{total}: {total_time/total:.2f} minutes")


def main():
    parser = argparse.ArgumentParser(description="Run LogicTree with configurable options")
    parser.add_argument("--llm", type=str, default="gpt-4o", help="LLM model to use")
    parser.add_argument("--spacy_model", type=str, default="en_core_web_lg", help="SpaCy model to use")
    parser.add_argument("--dataset", type=str, choices=["LogicNLI", "RobustLR", "prontoQA_ood", "proofwriter", "ParaRules"],
                        default="proofwriter", help="Dataset to evaluate")
    parser.add_argument("--test_range", nargs=2, type=int, default=None, help="Start and end indices for test samples (default is all samples)")
    parser.add_argument("--max_queries", type=int, default=80, help="Maximum GPT query limit before stopping")
    parser.add_argument("--double_check_deadend", action="store_true", help="Enable double-checking predicted deadends")

    args = parser.parse_args()

    test_range = tuple(args.test_range) if args.test_range else None
    logictree(llm=args.llm,
              spacy_model=args.spacy_model,
              dataset=args.dataset,
              test_range=test_range,
              max_queries=args.max_queries,
              double_check_deadend=args.double_check_deadend)


if __name__ == "__main__":
    main()