import sys
import pprint
from nltk.corpus import BracketParseCorpusReader


corpus_root = r"C:\Users\maksi\Documents\Python\NLP class\data_for_HW2\wsj"
file_pattern = r".*/wsj_.*\.mrg"


def return_rule(some_tree, some_dict,file):  # returns nodes on this level tree
    some_tree_parent = some_tree.label()#left side of the rule
    children_node_list = [] #right side of the rule
    for subtree in some_tree:
        if isinstance(subtree, str):#terminal state
            children = subtree
            some_dict['lexicon'].add(some_tree_parent)
        else:
            children = subtree.label()
        children_node_list.append(children)
    while len(children_node_list)>2:
        #converting it to CNF
        new_head = '_'.join(children_node_list[1:])#generating new left side of the rule
        new_children_node_list = children_node_list[:1]+[new_head] #generating new right side of the rule
        value = tuple(new_children_node_list)
        if some_tree_parent not in some_dict:
            some_dict[some_tree_parent]=set()
            some_dict[some_tree_parent].add(value)
        else:
            some_dict[some_tree_parent].add(value)
        some_tree_parent = new_head
        children_node_list = children_node_list[1:]
    #taking care of last rule whose right side len == 2
    value = tuple(children_node_list)
    if some_tree_parent not in some_dict:
        some_dict[some_tree_parent] = set()
        some_dict[some_tree_parent].add(value)
    else:
        some_dict[some_tree_parent].add(value)


def extracting_cnf(corpus_root, file_pattern):
    ptb = BracketParseCorpusReader(corpus_root, file_pattern)
    cnf_dict = {}
    cnf_dict['lexicon'] = set()
    #for file in ptb.fileids():
    #for file in ptb.fileids():
    file = ptb.fileids()[0]
    print(file)
    for s in range(1, len(ptb.parsed_sents(file))):
        tree = ptb.parsed_sents(file)[s]
        for sub in tree.subtrees():
            return_rule(sub, cnf_dict,file)
    return cnf_dict

def collapse_unit_productions(unite_dict):
    lexicon = unite_dict['lexicon'].copy()#here I have terminal productions
    # print(lexicon)
    del unite_dict['lexicon']
    new_dic = {}
    for key in unite_dict:
        if key not in lexicon:
            new_dic[key]=set()
            set_of_right_side = unite_dict[key]
            for single_right_side in set_of_right_side:
                if len(single_right_side)==1:
                    for e in unite_dict[single_right_side[0]]:
                        new_dic[key].add(e)
                else:
                    new_dic[key].add(single_right_side)
        else:
            new_dic[key] = unite_dict[key]
    return new_dic


orig = sys.stdout


cnf = extracting_cnf(corpus_root, file_pattern)
cnf_new = collapse_unit_productions(cnf)

# pprint.pprint(cnf)
fout = open('grammar.txt', 'w')
sys.stdout = fout
total_number_rules = 1
for key,value in cnf_new.items():
    for v in value:
        print(key,'->',' '.join(v))
        total_number_rules+=1
#print('Total number of rues = ',total_number_rules)

# ss = set()
# s1 = set()
# ss.add(tuple('a'))
# ss.add(tuple(['b','f']))
# ss.add(tuple(['c','d']))
# s1.add(tuple(' '.join(i) for i in ss))
# print(s1)