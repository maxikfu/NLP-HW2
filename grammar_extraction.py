import sys

from nltk.corpus import BracketParseCorpusReader


corpus_root = r"C:\Users\maksi\Documents\Python\NLP class\HW2\wsj\wsj"
file_pattern = r".*/wsj_.*\.mrg"


def return_rule(some_tree, some_l):  # returns nodes on this level tree
    some_tree_root = some_tree.label()
    children_node_list = [some_tree_root, '->']
    for subtree in some_tree:
        if isinstance(subtree, str):#terminal state
            l = subtree
        else:
            l = subtree.label()
        children_node_list.append(l)
    while len(children_node_list)>4:
        #converting it to CNF
        new_head = '_'.join(children_node_list[3:])
        new_children_node_list = children_node_list[:3]+[new_head]
        if (tuple(new_children_node_list) not in some_l):
            some_l.add(tuple(new_children_node_list))
        children_node_list = [new_head,'->']+children_node_list[3:]
    if (tuple(children_node_list) not in some_l):
        some_l.add(tuple(children_node_list))


def extracting_cfg(corpus_root, file_pattern):
    ptb = BracketParseCorpusReader(corpus_root, file_pattern)
    li = set()
    #for file in ptb.fileids():
    file = ptb.fileids()[0]
    print(file)
    for s in range(1, len(ptb.parsed_sents(file))):
        tree = ptb.parsed_sents(file)[s]
        for sub in tree.subtrees():
            return_rule(sub, li)
    return li

orig = sys.stdout

cfg = {}
cfg = extracting_cfg(corpus_root, file_pattern)
fout = open('output.txt', 'w')
sys.stdout = fout
print(len(cfg))
for el in cfg:
    print(el)