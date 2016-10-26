import re
import grammarClass

def getGrammar(fileName):
    with open(fileName) as f:
        lines = f.read()

    file_split = re.split(r"#Terminais|#Variaveis|#Inicial|#Regras", lines)

    file_rules = re.split(r" > |\n", file_split[4])

    exp = r"\[ ([^]]*) \]"

    grammar = grammarClass.Grammar()

    for index, line in enumerate(file_split):

        if index == 1:
            searchObj = re.findall(exp, line)
            if searchObj:
                grammar.terminals = searchObj

        elif index == 2:
            searchObj = re.findall(exp, line)
            if searchObj:
                grammar.variables = searchObj
                for x in searchObj:
                    grammar.rules[x] = []

        elif index == 3:
            searchObj = re.findall(exp, line)
            if searchObj:
                grammar.initial_var = searchObj

        elif index == 4:
            for index, l in enumerate(file_rules):
                if index % 2 != 0:
                    searchObj = re.findall(exp, l)
                else:
                    searchObj2 = re.findall(exp, l)
                    if searchObj2:
                        grammar.rules[''.join(searchObj)].append(searchObj2)

    rules = []
    temp_ter = []

    for var, ter in grammar.rules.items():
        for t in ter:
            temp_ter.append(''.join(t))
        rules.append("%s -> %s" % (var, ', '.join(temp_ter)))
        temp_ter = []

    result_grammar = ['Gramatica dada', 'Terminais: ' + ', '.join(grammar.terminals),
                      'Variaveis: ' + ', '.join(grammar.variables), 'Simbolo inicial: ' + ' '.join(grammar.initial_var),
                      'Regras: {' + ',\n'.join(rules) + '}']
    return '\n'.join(result_grammar)

    # print "\n\n\n"

    # print "Terminais: %s" % grammar.terminals
    # print "Variaveis: %s" % grammar.variables
    # print "Simbolo inicial: %s" % grammar.initial_var
    # print "Regras: "
    # for var, ter in grammar.rules.iteritems():
    #   print " %s -> %s" % (var, ter)

    # print "\n\n\n"