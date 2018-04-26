import sys
fout = open('no_grammar.txt','w')
sys.stdout = fout
for line in open('test.txt','r',encoding='UTF-8'):
    sen = line.split()
    result = '(S'
    for x in sen:
        result = result + '( NP ' + x + ')'
    print(result+')')