import string
# Function to extract entity-relationship pairs and triples
def extract_key_words(nlp, text):
    doc = nlp(text)
    pairs = set()
    triples = set()

    for token in doc:
        if token.pos_ == "ADJ":
            pairs.add(token.text.lower())  # Add the adjective alone
            for child in token.head.children:
                if child.dep_ in {"nsubj", "dobj", "pobj"} and child.pos_ in {"NOUN", "PROPN"}:
                    pairs.add((child.lemma_.lower(), token.text.lower()))

        # Check for verbs with subject and object (e.g., "The rabbit needs the cat")
        if token.pos_ == "VERB":
            subject = None
            obj = None
            for child in token.children:
                if child.dep_ in {"nsubj", "nsubjpass"}:  # Subject
                    subject = child.lemma_.lower()
                if child.dep_ in {"dobj", "pobj"}:  # Object
                    obj = child.lemma_.lower()
            if subject and obj:
                triples.add((subject, token.lemma_, obj))
                pairs.add((token.lemma_, obj))
                pairs.add((subject, token.lemma_))
            elif obj:
                pairs.add((token.lemma_, obj))  # Add verb-object pair
            elif subject:
                pairs.add((subject, token.lemma_))

    return pairs.union(triples)


# Function to rank rules based on overlap with the statement to be proved (fact)
def rank_rules(nlp, rules, fact, remove_rule_with_zero_score=True):
    # Extract pairs for each rule and the fact
    extracted_rules = {rule: extract_key_words(nlp, rule) for rule in rules}
    extracted_fact = extract_key_words(nlp, fact)

    rule_scores = []

    # Function to calculate the score based on overlap
    def calculate_score(fact_pairs, rule_pairs):
        return len(fact_pairs.intersection(rule_pairs))

    # Analyze each rule and calculate its score based on overlap
    for rule, rule_pairs in extracted_rules.items():
        score = calculate_score(extracted_fact, rule_pairs)
        rule_scores.append((rule, score))

    # Sort rules by their score in descending order
    ranked_rules_scores = sorted(rule_scores, key=lambda x: x[1], reverse=True)
    if remove_rule_with_zero_score:
        ranked_rules = [rule for rule, score in ranked_rules_scores if score > 0]
    else:
        ranked_rules = [rule for rule, score in ranked_rules_scores]
    return ranked_rules_scores, ranked_rules


# Function to rank deadend paths based on overlap of the last rule of each deadend path with the statement to be proved (fact)
# in-place sorting pseudo_deadends_repo, from low to high
def rank_deadends_paths(nlp, pseudo_deadends_repo, fact):
    # pseudo_deadends_repo: list of list (path)
    # fact: str

    # Extract pairs for each rule in the last rule of each deadend path and the fact
    extracted_rules = {'/n'.join(path): extract_key_words(nlp, path[-1]) for path in pseudo_deadends_repo}
    extracted_fact = extract_key_words(nlp, fact)

    path_scores = dict()

    # Function to calculate the score based on overlap
    def calculate_score(fact_pairs, rule_pairs):
        return len(fact_pairs.intersection(rule_pairs))
    
    # Analyze each deadend path and calculate its score based on overlap
    for path in pseudo_deadends_repo:
        score = calculate_score(extracted_fact, extracted_rules['/n'.join(path)])
        path_scores['/n'.join(path)] = score
    
    # Sort paths by their score in ascending order
    pseudo_deadends_repo.sort(key=lambda path: path_scores['/n'.join(path)])
    return path_scores


# Function to rank facts based on overlap with rules and consider reference (subject) entities like "tiger"
def rank_facts(nlp, facts, rules, reference_entity=None, remove_fact_with_zero_score=True):
    # Extract pairs and triples for each fact and rule
    extracted_facts = {fact: extract_key_words(nlp, fact) for fact in facts}
    extracted_rules = {rule: extract_key_words(nlp, rule) for rule in rules}

    fact_scores = []

    # Function to calculate the score based on overlap and presence of reference entity
    def calculate_score(fact_pairs, rule_pairs, rule_text):
        overlap_score = len(fact_pairs.intersection(rule_pairs))
        if reference_entity and (overlap_score > 0) and (reference_entity.lower() in rule_text.lower()):
            reference_score = 0.5
        else:
            reference_score = 0
        return overlap_score + reference_score

    # Analyze each fact and calculate its score based on overlap and reference entity
    for fact, fact_pairs in extracted_facts.items():
        max_score = 0
        for rule, rule_pairs in extracted_rules.items():
            score = calculate_score(fact_pairs, rule_pairs, rule)

            # Use the highest score from matching rules
            # max_score = max(max_score, score)

            # Accumulate the scores from all matching rules (from graph perspective)
            max_score += score

        fact_scores.append((fact, max_score))

    # Sort facts by their score in descending order, because we will iterate from the beginning
    ranked_facts_scores = sorted(fact_scores, key=lambda x: x[1], reverse=True)
    if remove_fact_with_zero_score:
        ranked_facts = [fact for fact, score in ranked_facts_scores if score > 0]
    else:
        ranked_facts = [fact for fact, score in ranked_facts_scores]
    return ranked_facts_scores, ranked_facts


def split_facts_based_on_subj_of_interest(subj, facts):
    subj_facts = []
    other_facts = []
    for fact in facts:
        if subj.lower() in fact.lower():
            subj_facts.append(fact)
        else:
            other_facts.append(fact)
    return subj_facts, other_facts

def extract_text_from_repo(text, repo):
    repo_list = repo.split('\n')
    for line in repo_list:
        line_strip = line.translate(str.maketrans('', '', string.punctuation))
        text_strip = text.translate(str.maketrans('', '', string.punctuation))
        if line_strip.lower() in text_strip.lower():
            return line
    return None

# by checking the rules, if there are two different subjects have connections, to determine if need to check other facts
def check_if_need_other_facts(nlp, rules):

    def is_pronoun(token):
        """Check if a token is a pronoun."""
        return token.pos_ == "PRON"

    def extract_subjects_general(sentence):
        """
        Extract subjects and check if there are two different subjects based on the conditions.
        """
        doc = nlp(sentence)
        subjects = []
        
        # Extract all subjects in the sentence
        for token in doc:
            if token.dep_ in ["nsubj", "nsubjpass"]:
                subjects.append(token)
        
        # Check conditions for different subjects
        for i, subj1 in enumerate(subjects):
            for subj2 in subjects[i+1:]:
                # Condition 1: Pronoun vs. Specific Noun
                if is_pronoun(subj1) != is_pronoun(subj2):
                    return True
                
                # Condition 2: Different Pronouns (considered same)
                if is_pronoun(subj1) and is_pronoun(subj2):
                    continue  # Same subject
                
                # Condition 3: Different Specific Nouns
                if subj1.lemma_.lower() != subj2.lemma_.lower():  # Case insensitive comparison
                    return True
        
        return False

  
    for rule in rules:
        if extract_subjects_general(rule):
            return True
        
    return False

