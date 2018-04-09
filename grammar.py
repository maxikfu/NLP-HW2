import sys
import nltk
from nltk.corpus import BracketParseCorpusReader
# from __future__ import print_function

from nltk.tree import Tree

def chomsky_normal_form(tree, factor="right", horzMarkov=None, vertMarkov=0, childChar="|", parentChar="^"):

    if horzMarkov is None: horzMarkov = 999

    nodeList = [(tree, [tree.label()])]
    while nodeList != []:
        node, parent = nodeList.pop()
        if isinstance(node,Tree):

            # parent annotation
            parentString = ""
            originalNode = node.label()

            # add children to the agenda before we mess with them
            for child in node:
                nodeList.append((child, parent))

            # chomsky normal form factorization
            if len(node) > 2:
                childNodes = [child.label() for child in node]
                nodeCopy = node.copy()
                node[0:] = [] # delete the children

                curNode = node
                numChildren = len(nodeCopy)
                for i in range(1,numChildren - 1):
                    if factor == "right":
                        newHead = "%s%s<%s>%s" % (originalNode, childChar, "-".join(childNodes[i:min([i+horzMarkov,numChildren])]),parentString) # create new head
                        newNode = Tree(newHead, [])
                        curNode[0:] = [nodeCopy.pop(0), newNode]
                    curNode = newNode

                curNode[0:] = [child for child in nodeCopy]


corpus_root = r"C:\Users\maksi\Documents\Python\NLP class\HW2\wsj\wsj"
file_pattern = r".*/wsj_.*\.mrg"

ptb = BracketParseCorpusReader(corpus_root, file_pattern)

tree = ptb.parsed_sents('00/wsj_0001.mrg')[1]
#s= "(S (NP (DT the) (NNS kids)) (VP (VBD opened) (NP (DT the) (NN box)) (PP (IN on)(NP (DT the) (NN floor)))))"
#tree = Tree.fromstring(tree1)
tree.chomsky_normal_form()
for p in tree.productions():
    print (p)
