import sys
import pprint
from nltk.corpus import BracketParseCorpusReader
import time

corpus_root = r"wsj"
file_pattern = r".*/wsj_.*\.mrg"


def extracting_cfg(corpus_root, file_pattern):#returns cfg eith only 2 non-terminals on the right
    ptb = BracketParseCorpusReader(corpus_root, file_pattern)
    cfg_dict = {}
    unite_productions ={}
    lexicon = {}
    for file in ptb.fileids():
        #file = ptb.fileids()[0]
        print(file)
        for sentence in  ptb.parsed_sents(file):  # iterating through sentences
            #sentence =ptb.parsed_sents(file)[some_i]
            if len(sentence.leaves())<=8:
                #print(sentence.leaves())
                for subtree in sentence.subtrees():  # extracting subtree
                    left_side = subtree.label()
                    right_side = []
                    for children in subtree:
                        if isinstance(children, str):  # reached leaf node
                            right_side.append(children)
                            if left_side in lexicon:
                                lexicon[left_side].add(children)
                            else:
                                lexicon[left_side] = set()
                                lexicon[left_side].add(children)
                        else:  # still not leafe node
                            right_side.append(children.label())
                    while len(right_side) > 2:  # making only 2 non-terminals on the right side
                        new_head = '_'.join(right_side[1:])  # generating new left side of the rule
                        new_right_side = right_side[:1] + [new_head]  # generating new right side of the rule
                        tup = tuple(new_right_side)
                        if left_side not in cfg_dict:  # new key
                            cfg_dict[left_side] = set()
                            cfg_dict[left_side].add(tup)
                        else:
                            cfg_dict[left_side].add(tup)
                        left_side = new_head
                        right_side = right_side[1:]
                    if len(right_side)==1:#unite production
                        if left_side in unite_productions:
                            unite_productions[left_side].add(tuple(right_side))
                        else:
                            unite_productions[left_side]=set()
                            unite_productions[left_side].add(tuple(right_side))
                    if left_side in cfg_dict:  # adding rule to the dict
                        cfg_dict[left_side].add(tuple(right_side))
                    else:
                        cfg_dict[left_side] = set()
                        cfg_dict[left_side].add(tuple(right_side))
    return cfg_dict,lexicon,unite_productions


def counting_unite_productions(cfg,lexicon): #extracting rules what have unite productions
    unite_dic = {}
    words = set()
    need_to_delete = []
    for key,value in lexicon.items():
        for word in value:
            words.add(tuple([word]))
    for key, value in cfg.items():
        if key not in lexicon:
            for right in value:
                if len(right)==1 and (right not in words) and (right[0] != key):#we found unite production
                    if key in unite_dic:
                        unite_dic[key].add(right)
                    else:
                        unite_dic[key]=set()
                        unite_dic[key].add(right)
    return unite_dic


def collapse_unit_productions(unite_dict,need_to_collapse):#returns grammar without unite productions specified in need_to_collapse
    deleting_from = []
    for key, value in need_to_collapse.items():
        for unit in value:
            unite_dict[key].remove(unit)#removing single non-terminal on right side
            for v in unite_dict[unit[0]]:
                if v != unit and v != key and (v not in value):
                    unite_dict[key].add(v)
    return unite_dict


def eliminate_all_unit(grammar,lexicon):
    have_unite = counting_unite_productions(grammar,lexicon)
    while have_unite:
        print(len(have_unite),sorted(have_unite))
        grammar = collapse_unit_productions(grammar, have_unite)
        have_unite = counting_unite_productions(grammar,lexicon)
    return  grammar

start_time = time.time()
cfg_1,lexicon,unite_productions = extracting_cfg(corpus_root, file_pattern)
fout = open('grammar.txt', 'w')
cnf = eliminate_all_unit(cfg_1,lexicon)
runningTime= time.time() - start_time
print(runningTime)
total_number_rules = 0
sys.stdout = fout
for key,value in cnf.items():
    for v in value:
        print(key,'->',' '.join(v))
        total_number_rules+=1
# print('Total number of rues = ',total_number_rules)
# pprint.pprint(unite_productions)
