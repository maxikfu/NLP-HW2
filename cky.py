#reading grammar
from CellContent import CellContent
import pprint
def reading_grammar(grammar_file_location):#return grammar in dict fromat from the file
    local_dict = {}
    for line in open(grammar_file_location):
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
        for i in range(j-1,-1,-1):#bottom to top
            for k in range(i,j):
                #looking for right sides in grammar
                if table[k][i] is not None:
                    for left_obj in table[k][i]:
                        if table[j][k+1] is not None:
                            for down_obj in table[j][k+1]:
                                for left_side, value in grammar.items():
                                    for right_side in value:
                                        if right_side == tuple([left_obj.content,down_obj.content]): #bottom to top                                    new_cell = CellContent(left_side, None, None)
                                            new_cell = CellContent(left_side,left_obj,down_obj)
                                            if table[j][i] is None:
                                                table[j][i] = [new_cell]
                                            else:
                                                already_there = False
                                                for a in table[j][i]:
                                                    if a.content == new_cell.content:
                                                        already_there =True
                                                if not already_there:
                                                    table[j][i].append(new_cell)
    return table


def print_tree(full_table):
    stack = []
    stack = [obj for obj in full_table[len(sen) - 1][0] if obj.content == 'S']
    result = ''
    if not stack:
        print('No grammar for this sentence')
    while stack:  # reveling tree untill there are any nodes left
        working_obj = stack.pop()  # we get last element
        result = result + ' ( ' + working_obj.content
        if working_obj.terminal is not None:  # means we recheed leafe
            result = result + ' ' + working_obj.terminal + ' ) '
        else:
            two_terminals = None
            stack.append(working_obj.right_backpointer)
            stack.append(working_obj.left_backpointer)
    print(result)



cnf_grammar = reading_grammar('toy/CNF_test.txt')
sen = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
table = CKY_parser(sen,cnf_grammar)
print_tree(table)
