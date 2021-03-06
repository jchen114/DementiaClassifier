import SCA.L2SCA.analyzeText as at

try:
    import cPickle as pickle
except:
    import pickle

auxiliary_dependencies = frozenset([
    'auxpass',
    'cop',
    'aux',
    'xcomp'
])


class tree_node():

    def __init__(self, key, phrase=None):
        self.key = key
        self.phrase = phrase
        self.children = []

    def addChild(self, node):
        self.children.append(node)


# class StanfordServerThread(threading.Thread):

#     def __init__(self, port = 9000):
#         self.stdout = None
#         self.stderr = None
#         self.port = port
#         self.p = None
#         threading.Thread.__init__(self)

#     def run(self):
#         server_cmd = ['java', '-Xmx4g', '-cp', '\'stanford/stanford-corenlp-full-2015-12-09/*\'',
#                       'edu.stanford.nlp.pipeline.StanfordCoreNLPServer', '-port', str(self.port)]
#         self.p = subprocess.Popen(server_cmd)
#         # self.p = subprocess.call(server_cmd)

#     def stop_server(self):
#         self.p.kill()


# def start_stanford_server(port = 9000):
#     stanfordServerThread = StanfordServerThread()
#     stanfordServerThread.start()
#     return stanfordServerThread


def build_tree(parse_tree):
    node_stack = []
    build_node = False
    node_type  = None
    phrase = None
    root_node = None
    encounter_leaf = False
    for ch in parse_tree:
        # If we encounter a ( character, start building a node
        if ch == '(':
            if node_type:
                # Finished building node
                node_type = node_type.strip()
                new_node = tree_node(node_type)
                node_stack.append(new_node)
            # Reset
            encounter_leaf = False
            build_node = True
            node_type = None
            phrase = None
            continue
        if ch == ')':
            # pop from the stack and add it to the children for the node before it
            if phrase:
                new_node = tree_node(node_type, phrase)
                node_stack.append(new_node)
            popped_node = node_stack.pop()
            if len(node_stack) > 0:
                parent = node_stack[-1]
                parent.addChild(popped_node)
            else:
                root_node = popped_node
            phrase = None
            node_type = None
            build_node = False
            encounter_leaf = False
            continue
        if encounter_leaf and build_node:
            if not phrase:
                phrase = ''
            phrase += ch
            continue
        if ch.isspace():
            encounter_leaf = True
            continue
        if build_node:
            if not node_type:
                node_type = ''
            node_type = node_type + ch
            continue    
    return root_node


def get_height_of_tree(tree_node):

    depths = [0]
    for children in tree_node.children:
        depths.append(get_height_of_tree(children))
    depths = map(lambda x: x+1, depths)
    return max(depths)


def get_count_of_parent_child(child_type, parent_type, tree_node, prev_type=None):
    curr_type = tree_node.key
    count = 0
    if prev_type == parent_type and curr_type == child_type:
        count = 1
    for child in tree_node.children:
        count += get_count_of_parent_child(child_type, parent_type, child, curr_type)
    return count


def get_count_of_parent_children(child_types, parent_type, tree_node):
    count = 0
    curr_type = tree_node.key
    if not len(tree_node.children):
        return count
    curr_children = [child.key for child in tree_node.children]
    if curr_type == parent_type and set(child_types).issubset(set(curr_children)):
        count = 1
    for child in tree_node.children:
        count += get_count_of_parent_children(child_types, parent_type, child)
    return count


def get_NP_2_PRP(tree_node):
    return get_count_of_parent_child('PRP', 'NP', tree_node)


def get_ADVP_2_RB(tree_node):
    return get_count_of_parent_child('RP', 'ADVP', tree_node)


def get_NP_2_DTNN(tree_node):
    return get_count_of_parent_children(['DT','NN'], 'NP', tree_node)


def get_VP_2_VBG(tree_node):
    return get_count_of_parent_child('VBG', 'VP', tree_node)


def get_VP_2_VBGPP(tree_node):
    return get_count_of_parent_child(['VBG', 'PP'], 'VP', tree_node)


def get_VP_2_AUXVP(tree_node, dependents):
    return get_VP_to_aux_and_more(tree_node, "VP", dependents)


def get_VP_2_AUXADJP(tree_node, dependents):
    return get_VP_to_aux_and_more(tree_node, "ADJP", dependents)


def get_VP_to_aux_and_more(tree_node, sibling_to_check, dependents):
    count = 0
    if tree_node.key == 'VP':
        # Check children phrase to see if it is inside the aux dependencies
        child_keys = []
        aux_present = False
        for child in tree_node.children:
            if child.phrase:  # If child phrase exists
                if child.phrase in dependents:
                    aux_present = True
            child_keys.append(child.key)
        # Check for condition
        if aux_present:
            child_keys = set(child_keys)
            if sibling_to_check in child_keys:
                count += 1
    for child in tree_node.children:
        count += get_VP_to_aux_and_more(child, sibling_to_check, dependents)

    return count


def get_aux_dependency_dependent(dependencies):
    dependents_list = []
    for dependency in dependencies:
        if dependency['dep'] in auxiliary_dependencies:
            dependents_list.append(dependency['dependentGloss'])
    return dependents_list


def get_VP_2_AUX(dependencies):
    # return number of aux dependencies
    # ----------- ASSUMING that aux dependencies always have a VP as a parent node
    count = 0
    for dependency in dependencies:
        if dependency['dep'] in auxiliary_dependencies:
            count += 1
    return count


def get_VP_2_VBDNP(tree_node):
    return get_count_of_parent_child(['VBD', 'NP'], 'VP', tree_node)


def get_INTJ_2_UH(tree_node):
    return get_count_of_parent_child('UH', 'INTJ', tree_node)


def get_ROOT_2_FRAG(tree_node):
    return get_count_of_parent_child('FRAG', 'ROOT', tree_node)


def get_all_syntactics_features(sample):
    # Make a temporary file for writing to
    tmp_file = open('sample_file.txt','w+')
    raw_text = ''
    for utterance in sample:
        raw_text += utterance['raw']
    tmp_file.write(raw_text)
    tmp_file.close()
    output_file = open('sample_output.txt', 'w')
    at.analyze_file(tmp_file.name, output_file)
    analyzed_file = open(output_file.name, 'r')
    headers = analyzed_file.readline().split(',')[1:] # Headers
    data = analyzed_file.readline().split(',')[1:] # actual data
    features = dict(zip(headers,data))
    return features


def get_number_of_nodes_in_tree(root_node):
    if len(root_node.children) == 0:
        return 1
    count = 1
    for child in root_node.children:
        count += get_number_of_nodes_in_tree(child)
    return count


def get_CFG_counts(root_node, dict):
    if dict.has_key(root_node.key):
        dict[root_node.key] += 1
    if len(root_node.children) > 0:  # Child leaf
        for child in root_node.children:
            dict = get_CFG_counts(child, dict)
    return dict


def get_all_tree_features(sample):
    features = {
        'tree_height': 0,
        'NP->PRP': 0,
        'ADVP->RB': 0,
        'NP->DT_NN': 0,
        'VP->AUX_VP': 0,
        'VP->VBG': 0,
        'VP->VBG_PP': 0,
        'VP->AUX_ADJP': 0,
        'VP->AUX': 0,
        'VP->VBD_NP': 0,
        'INTJ->UH': 0,
        'ROOT->FRAG': 0
    }
    total_nodes = 0
    for utterance in sample:
        for tree in range(0, len(utterance['parse_tree'])):
            parse_tree = utterance['parse_tree'][tree]
            root_node = build_tree(parse_tree)
            total_nodes += get_number_of_nodes_in_tree(root_node)
            features['tree_height'] += get_height_of_tree(root_node)
            features['NP->PRP'] += get_NP_2_PRP(root_node)
            features['ADVP->RB'] += get_ADVP_2_RB(root_node)
            features['NP->DT_NN'] += get_NP_2_DTNN(root_node)
            features['VP->VBG'] += get_VP_2_VBG(root_node)
            features['VP->VBG_PP'] += get_VP_2_VBGPP(root_node)
            features['VP->VBD_NP'] += get_VP_2_VBDNP(root_node)
            features['INTJ->UH'] += get_INTJ_2_UH(root_node)
            features['ROOT->FRAG'] += get_ROOT_2_FRAG(root_node)
            # Needs special love
            dependencies = utterance['basic_dependencies'][tree]
            features['VP->AUX'] += get_VP_2_AUX(dependencies)
            dependents = get_aux_dependency_dependent(dependencies)
            features['VP->AUX_VP'] += get_VP_2_AUXVP(root_node,dependents)
            features['VP->AUX_ADJP'] += get_VP_2_AUXADJP(root_node,dependents)

    #================ DIVIDING BY NUMBER OF total nodes in the sample ===============#
    for k,v in features.iteritems():
        features[k] /= float(total_nodes)

    return features


def get_all_CFG_features(sample):
    total_nodes = 0
    CFG_counts = {
        "ADJP": 0,
        "ADVP": 0,
        "CONJP": 0,
        "FRAG": 0,
        "INTJ": 0,
        "LST": 0,
        "NAC": 0,
        "NP": 0,
        "NX": 0,
        "PP": 0,
        "PRN": 0,
        "PRT": 0,
        "QP": 0,
        "RRC": 0,
        "UCP": 0,
        "VP": 0,
        "WHADJP": 0,
        "WHAVP": 0,
        "WHNP": 0,
        "WHPP": 0,
        "X": 0
    }
    for utterance in sample:
        for tree in range(0, len(utterance['parse_tree'])):
            parse_tree = utterance['parse_tree'][tree]
            root_node = build_tree(parse_tree)
            total_nodes += get_number_of_nodes_in_tree(root_node)
            CFG_counts = get_CFG_counts(root_node, CFG_counts)
    # ---- Normalize by total number of constituents in the sample
    for k,v in CFG_counts.iteritems():
        CFG_counts[k] /= float(total_nodes)
    return CFG_counts


def get_all(interview):
    feature_dict = get_all_syntactics_features(interview)
    feature_dict.update(get_all_tree_features(interview))
    feature_dict.update(get_all_CFG_features(interview))
    return feature_dict


def print_tree(root_node):
    queue = []
    queue.append(root_node)

    while len(queue) != 0:
        node = queue.pop(0) # POP first element
        print("current node = " + node.key)
        if node.phrase:
            print("phrase = " + node.phrase)
        for child in node.children:
            queue.append(child)


if __name__ == '__main__':
    with open('../stanford/processed/pickles/dbank_control.pickle', 'rb') as handle:
        control = pickle.load(handle)
    test_set = control[1:]
    features = []
    for interview in test_set:
        features.append(get_all_CFG_features(interview))

    #thread = start_stanford_server() # Start the server
    #trees = get_parse_tree('The quick brown fox jumped over the lazy dog. I wore the black hat to school.')
    #node = build_tree(trees[0])
    #thread.stop_server()

    #root = build_tree('u(ROOT\n  (S\n    (NP (DT The) (JJ quick) (JJ brown) (NN fox))\n    (VP (VBD jumped)\n      (PP (IN over)\n        (NP (DT the) (JJ lazy) (NN dog))))\n    (. .)))')
    # process dbank control

	#get_structure_features('stanford/processed/dbank/control', 'dbank/control_SCA')
    # process dbank dementia
    #get_structure_features('stanford/processed/dbank/dementia', 'dbank/dementia_SCA')
    # print "Starting server"
    # thread = start_stanford_server() # Start the server
    # try:
    #     tree = get_parse_tree('The quick brown fox jumped over the lazy dog.')
    #     root = build_tree(tree)
    #     print get_VP_2_AUX(tree_node)
    #     build_tree('u(ROOT\n  (S\n    (NP (DT The) (JJ quick) (JJ brown) (NN fox))\n    (VP (VBD jumped)\n      (PP (IN over)\n        (NP (DT the) (JJ lazy) (NN dog))))\n    (. .)))')
    # except Exception as e:
    #     print(e)
    # finally:
    #     print "Stopping server"
    #     thread.stop_server()


    # ------------------------   
    # Must start server by from commandline using:
    # java -Xmx4g -cp "stanford/stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000
    # ------------------------   
