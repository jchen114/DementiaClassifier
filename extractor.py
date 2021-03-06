import subprocess
import threading

import SCA.L2SCA.analyzeText as at
import Driver as dvr

# import SCA.L2SCA.analyzeFolder as af


class tree_node():

    def __init__(self, key, phrase=None):
        self.key = key
        self.phrase = phrase
        self.children = []

    def addChild(self, node):
        self.children.append(node)


class StanfordServerThread(threading.Thread):

    def __init__(self, port = 9000):
        self.stdout = None
        self.stderr = None
        self.port = port
        self.p = None
        threading.Thread.__init__(self)

    def run(self):
        server_cmd = ['java', '-Xmx4g', '-cp', '\'stanford/stanford-corenlp-full-2015-12-09/*\'',
                      'edu.stanford.nlp.pipeline.StanfordCoreNLPServer', '-port', str(self.port)]
        self.p = subprocess.Popen(server_cmd)
        # self.p = subprocess.call(server_cmd)

    def stop_server(self):
        self.p.kill()


def start_stanford_server(port = 9000):
    stanfordServerThread = StanfordServerThread()
    stanfordServerThread.start()
    return stanfordServerThread


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
        if ch.isspace():
            encounter_leaf = True
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
        if build_node:
            if not node_type:
                node_type = ''
            node_type = node_type + ch
            continue    
    return root_node


def get_height_of_tree(tree_node):
    depth = 0
    for children in tree_node.children:
        depth += get_height_of_tree(children)
    return depth


def get_count_of_parent_child(child_type, parent_type, tree_node, prev_type = None):
    curr_type = tree_node.key
    count = 0
    if prev_type == parent_type and curr_type == child_type:
        count = 1
    for children in tree_node.children:
        count += get_count_of_parent_child(child_type, parent_type, children, curr_type)
    return count


def get_NP_2_PRP(tree_node):
    return get_count_of_parent_child('PRP', 'NP', tree_node)


def get_ADVP_2_RB(tree_node):
    return get_count_of_parent_child('ADVP', 'RP', tree_node)


def get_NP_2_DTNN(tree_node):
    return get_count_of_parent_child('NP', 'DT_NN', tree_node)


def get_VP_2_AUXVP(tree_node):
    return get_count_of_parent_child('VP', 'AUX_VP', tree_node)


def get_VP_2_VBG(tree_node):
    return get_count_of_parent_child('VP', 'VBG', tree_node)


def get_VP_2_VBGPP(tree_node):
    return get_count_of_parent_child('VP', 'VBG_PP', tree_node)


def get_VP_2_AUXADJP(tree_node):
    return get_count_of_parent_child('VP', 'AUX_ADJP', tree_node)


def get_VP_2_AUX(tree_node):
    return get_count_of_parent_child('VP', 'AUX', tree_node)


def get_VP_2_VBDNP(tree_node):
    return get_count_of_parent_child('VP', 'VBD_NP', tree_node)


def get_INTJ_2_UH(tree_node):
    return get_count_of_parent_child('INTJ', 'UH', tree_node)


def get_structure_features(sample):
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




if __name__ == '__main__':
    #test_sample = [{'raw':'The big dog ate the fox.'},{'raw':'The orange kitten exploded.'},{'raw':'Glass cut through his veins.'},{'raw':'He shoved a stick up his asshole'}]
    #features = get_structure_features(test_sample)
    #for k,v in features.iteritems():
    #    print 'feature: ' + str(k) + ' value: ' + str(v)

    #thread = start_stanford_server() # Start the server
    dvr.get_all_pickles()
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
