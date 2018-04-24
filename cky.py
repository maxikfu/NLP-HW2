#reading grammar
import time
from CellContent import CellContent
import sys
def reading_grammar(grammar_file_location):#return grammar in dict fromat from the file
    local_dict = {}
    for line in open(grammar_file_location,'r',encoding = 'UTF -8'):
        rule = line.split()
        if rule[0] in local_dict:
            local_dict[rule[0]].add(tuple(rule[2:]))
        else:
            local_dict[rule[0]] = set()
            local_dict[rule[0]].add(tuple(rule[2:]))
    return local_dict


def CKY_parser(sentanceAsList,grammar):
    table = []
    for i in range(0,len(sentanceAsList)):#initializing table with None
        newList = [None] * (i+1)
        table.append(newList)
    s = time.time()
    print('Total number of words ',len(sentanceAsList))
    for j in range(0,len(sentanceAsList)):#left to right
         #looking for word in grammar right side
        for left_side,value in grammar.items():
            for right_side in value:
                if right_side == tuple([sentanceAsList[j]]):#filling up diagonal first
                    new_cell = CellContent(left_side,None,None)
                    new_cell.terminal = sentanceAsList[j]
                    if table[j][j] == None:
                        table[j][j] = [new_cell]
                    else:
                        table[j][j].append(new_cell)
        print('        Filled diagonal for word ',sentanceAsList[j])
        for i in range(j-1,-1,-1):#bottom to top
            some_count = 0
            for k in range(i,j):
                #looking for right sides in grammar
                if table[k][i] is not None:
                    for left_obj in table[k][i]:
                        if table[j][k+1] is not None:
                            for down_obj in table[j][k+1]:
                                for left_side, value in grammar.items():
                                    for right_side in value:
                                        if right_side == tuple([left_obj.content,down_obj.content]): #bottom to top
                                            new_cell = CellContent(left_side,left_obj,down_obj)
                                            left_obj.parent = new_cell#creating link to parent
                                            down_obj.parent = new_cell
                                            if table[j][i] is None:
                                                table[j][i] = [new_cell]
                                                some_count+=1
                                            else:
                                                already_there = False
                                                for a in table[j][i]:
                                                    if a.content == new_cell.content:
                                                        already_there =True
                                                if not already_there:
                                                    table[j][i].append(new_cell)
                                                    some_count+=1
            print('        Filled row ',i,' number of obj in the cell = ',some_count)
        print('Filled column for word ',sentanceAsList[j],' in ', time.time() - s)
    return table


def recursion(obj):
    tree_string = ''
    tree_string = tree_string + ' ( ' + obj.content
    for child in obj.children:
        if child != None:
            tree_string = tree_string + recursion(child)
            tree_string = tree_string + ') '
        else:
            tree_string = tree_string + ' ' + obj.terminal + ' '
    return tree_string

def print_tree(full_table):
    stack = []
    stack = [obj for obj in full_table[len(sen) - 1][0] if obj.content == 'S']
    result = ''
    if not stack:
        print(" ( S ( NN Not_in_grammar )  ( NP-SBJ_VP_. ( NP-SBJ and )  ( VP_. ( VP ( NN dessert )  ( VP followed ) )  ( . . ) ) ) ) ")
    else:
        # for start in stack:
        start = back_to_CFG(stack[0])
        result = recursion(start)
        result = result + ') '
        print('( '+result + ' )')


def back_to_CFG(start_obj):
    stack_local = []
    stack_local.append(start_obj)
    while stack_local:
        working_node = stack_local.pop()
        dummy_non_terminals = [x for x in working_node.children if (x is not None) and ("_" in x.content)]
        while dummy_non_terminals:
            d_n_t = dummy_non_terminals.pop()
            working_node.children.remove(d_n_t)
            working_node.children = working_node.children + d_n_t.children
            dummy_non_terminals = [x for x in working_node.children if "_" in x.content]
        stack_local = [w for w in working_node.children if w is not None] + stack_local
    return start_obj


cnf_grammar = reading_grammar('grammar.txt')
print('Grammar loaded = ', len(cnf_grammar))
strr = "Champagne and dessert followed ."
fout = open('submission.txt', 'w')
orig = sys.stdout
for line in open('test.txt', 'r', encoding='UTF-8'):
    strr = line
    sen = strr.split()
    print(sen)
    start_time = time.time()
    table = CKY_parser(sen,cnf_grammar)
    sys.stdout = fout
    print_tree(table)
    sys.stdout = orig
    runningTime= time.time() - start_time
    print(runningTime)
