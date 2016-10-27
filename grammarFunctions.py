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
                    grammar.empty_word[x] = 0
                    grammar.useless_symbol[x] = 1

        elif index == 3:
            searchObj = re.findall(exp, line)
            if searchObj:
                grammar.initial_var = searchObj
                grammar.useless_symbol[''.join(searchObj)] = 0

        elif index == 4:
            for index, l in enumerate(file_rules):
                if index % 2 != 0:
                    searchObj = re.findall(exp, l)
                else:
                    searchObj2 = re.findall(exp, l)
                    if searchObj2:
                        grammar.rules[''.join(searchObj)].append(searchObj2)
                        if 'V' in searchObj2:
                            grammar.empty_word[''.join(searchObj)] = 1

    printFinal = []

    printFinal.append(printGrammar(grammar, 'Gramática extraída do arquivo ' + fileName))

    goToV(grammar)
    changeGrammar(grammar)
    cleanV(grammar)

    printFinal.append("\n" + printGrammar(grammar, "(1) Exclusão de Produções Vazias"))

    print("\n\n\n")

    print("Terminais: %s" % grammar.terminals)
    print("Variaveis: %s" % grammar.variables)
    print("Simbolo inicial: %s" % grammar.initial_var)
    print("Regras: ")
    for var, ter in grammar.rules.items():
        print("%s -> %s" % (var, ter))

    for var, ter in grammar.empty_word.items():
        print("%s -> %d" % (var, ter))

    print("\n\n\n")

    varClosure(grammar)

    printFinal.append("\n" + printGrammar(grammar, "(2) Exclusão de Produções Simples"))

    print("\n\n\n")

    print("Terminais: %s" % grammar.terminals)
    print("Variaveis: %s" % grammar.variables)
    print("Simbolo inicial: %s" % grammar.initial_var)
    print("Regras: ")
    for var, ter in grammar.rules.items():
        print("%s -> %s" % (var, ter))

    print("\n\n\n")

    uslessSymbol(grammar)

    printFinal.append("\n" + printGrammar(grammar, "(3) Exclusão de Produções Inuteis"))

    return '\n----------------------------------------------------------------------\n'.join(printFinal)


def printGrammar(grammar, subTitle):
    rules = []
    temp_ter = []

    for var, ter in grammar.rules.items():
        for t in ter:
            temp_ter.append(''.join(t))
        rules.append("%s -> %s" % (var, ' | '.join(temp_ter)))
        temp_ter = []

    result_grammar = [subTitle, 'Terminais: ' + ', '.join(grammar.terminals),
                      'Variaveis: ' + ', '.join(grammar.variables), 'Simbolo inicial: ' + ' '.join(grammar.initial_var),
                      'Regras: {' + ',\n'.join(rules) + '}']
    return '\n\n'.join(result_grammar)


def goToV(grammar):  # primeiro passo da etapa de simplificacao da gramatica - producoes vazias
    for var, ter in grammar.rules.items():
        for item in ter:
            rules_count = 0
            rules_not_count = 0
            for x in item:
                if x in grammar.variables:
                    rules_not_count += 1
                    if rules_count == len(item) - rules_not_count:
                        grammar.empty_word[var] = 1
                elif grammar.empty_word[var] == 1:
                    rules_count += 1
                    if rules_count == len(item) - rules_not_count:
                        grammar.empty_word[var] = 1


def changeGrammar(grammar):  # segundo passo da etapa de simplificacao da gramatica - producoes vazias
    for var, ter in grammar.rules.items():
        if grammar.empty_word[var]:
            changeVar(var, grammar)


def changeVar(var, grammar):  # func aux do segundo passo
    for item in grammar.rules[var]:
        for x in item:
            if x in grammar.variables:
                if grammar.empty_word[x]:
                    aux = list(item)
                    aux.remove(x)
                    if aux and aux not in grammar.rules[var]:
                        grammar.rules[var].append(aux)


def cleanV(grammar):  # terceiro passo da etapa de simplificacao da gramatica - producoes vazias
    for var, ter in grammar.rules.items():
        for item in ter:
            if 'V' in item:
                ter.remove(item)
        if ''.join(grammar.initial_var) == var and grammar.empty_word[var]:
            grammar.rules[var].append(list("V"))


def varClosure(grammar): # etapa de simplificacao da gramatica - producoes simples
    for var, ter in grammar.rules.items():
        number_of_rules = len(ter)
        i = 0
        j = 0
        while j < 2:
            j += 1
            while i <= number_of_rules:
                for item in ter:
                    i += 1
                    if ''.join(item) in grammar.variables:
                        print("eita: %s" % item)
                        ter.remove(item)
                        for x in grammar.rules[''.join(item)]:
                            print("uer: %s" % x)
                            if x not in grammar.rules[var] and x != ''.join(item):
                                grammar.rules[var].append(x)

def uslessSymbol(grammar):
    for var, ter in grammar.rules.items():
        for item in ter:
            for x in item:
                grammar.useless_symbol[x] = 0

    for var, numb in grammar.useless_symbol.items():
        if var in grammar.variables and numb:
            for x in grammar.rules[var]:
                for i in x:
                    grammar.useless_symbol[i] = 1
            grammar.variables.remove(var)
            del grammar.rules[var]

    for var, ter in grammar.rules.items():
        for item in ter:
            for x in item:
                grammar.useless_symbol[x] = 0


    for var, numb in grammar.useless_symbol.items():
        if var in grammar.terminals and numb:
            grammar.terminals.remove(var)