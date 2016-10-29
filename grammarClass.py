import re

class Grammar:  # Grammar: salva variaveis, terminais e regras

    terminals = []
    variables = []
    initial_var = []
    rules = {}
    empty_word = {}
    useless_symbol = {}
    accepts_empty = 0
    has_empty = 0

    def __init__(self):
        self.terminals = []
        self.variables = []
        self.initial_var = []
        self.rules = {}  # rules: um dicionario que mantem todas as regras salvas usando as variaveis como indice
        self.empty_word = {}
        self.useless_symbol = {}
        self.accepts_empty = 0
        self.has_empty = 0

    @staticmethod
    def clean():
        Grammar.terminals = []
        Grammar.variables = []
        Grammar.initial_var = []
        Grammar.rules = {}
        Grammar.empty_word = {}
        Grammar.useless_symbol = {}
        Grammar.accepts_empty = 0
        Grammar.has_empty = 0

    @staticmethod
    def getGrammar(lines):
        file_split = re.split(r"#Terminais|#Variaveis|#Inicial|#Regras", lines)
        file_rules = re.split(r" > |\n", file_split[4])
        exp = r"\[ ([^]]*) \]"

        for index, line in enumerate(file_split):
            if index == 1:
                searchObj = re.findall(exp, line)
                if searchObj:
                    Grammar.terminals = searchObj

            elif index == 2:
                searchObj = re.findall(exp, line)
                if searchObj:
                    Grammar.variables = searchObj
                    for x in searchObj:
                        Grammar.rules[x] = []
                        Grammar.empty_word[x] = 0
                        Grammar.useless_symbol[x] = 1

            elif index == 3:
                searchObj = re.findall(exp, line)
                if searchObj:
                    Grammar.initial_var = searchObj
                    Grammar.useless_symbol[''.join(searchObj)] = 0

            elif index == 4:
                for index, l in enumerate(file_rules):
                    if index % 2 != 0:
                        searchObj = re.findall(exp, l)
                    else:
                        searchObj2 = re.findall(exp, l)
                        if searchObj2:
                            Grammar.rules[''.join(searchObj)].append(searchObj2)
                            if 'V' in searchObj2:
                                print("Grammar.rules[%s].append(%s)" %(''.join(searchObj), searchObj2))
                                Grammar.has_empty = 1
                                Grammar.empty_word[''.join(searchObj)] = 1


        return Grammar

    @staticmethod
    def printGrammar(subTitle):
        rules = []
        temp_ter = []

        for var, ter in sorted(Grammar.rules.items()):
            for t in sorted(ter):
                temp_ter.append(''.join(t))
            rules.append("%s -> %s" % (var, ' | '.join(temp_ter)))
            temp_ter = []

        result_Grammar = [subTitle, 'Terminais: ' + ', '.join(sorted(Grammar.terminals)),
                          'Variaveis: ' + ', '.join(sorted(Grammar.variables)),
                          'Simbolo inicial: ' + ' '.join(Grammar.initial_var),
                          'Regras: {' + ',\n'.join(rules) + '}']
        
        return '\n\n'.join(result_Grammar)

    @staticmethod
    def goToV():  # primeiro passo da etapa de simplificacao da gramatica - producoes vazias
        for var, ter in Grammar.rules.items():
            for item in ter:
                rules_count = 0
                for x in item:
                    if x in Grammar.variables and Grammar.empty_word[x]:
                        rules_count +=1
                if rules_count == len(item):
                    Grammar.empty_word[var] = 1

    @staticmethod
    def changeGrammar():  # segundo passo da etapa de simplificacao da gramatica - producoes vazias
        for var, ter in Grammar.rules.items():
            print(Grammar.empty_word)
            if Grammar.empty_word[var]:
                for item in Grammar.rules[var]:
                    for x in item:
                        if x in Grammar.variables:
                            if Grammar.empty_word[x]:
                                aux = list(item)
                                aux.remove(x)
                                if aux and aux not in Grammar.rules[var]:
                                    Grammar.rules[var].append(aux)

    @staticmethod
    def cleanV():  # terceiro passo da etapa de simplificacao da gramatica - producoes vazias
        for var, ter in Grammar.rules.items():
            for item in ter:
                if 'V' in item:
                    ter.remove(item)
            if ''.join(Grammar.initial_var) == var and Grammar.empty_word[var]:
                Grammar.rules[var].append(list("V"))
                Grammar.accepts_empty = 1

    @staticmethod
    def varClosure():  # etapa de simplificacao da gramatica - producoes simples
        for var, ter in Grammar.rules.items():
            print("VARIAVEL ATUAL: %s" % var)
            i = 0
            while i != len(ter):
                i = len(ter)
                for item in ter:
                    print("ITEM ATUAL: %s" %item)
                    if ''.join(item) in Grammar.variables:
                        print(Grammar.variables)
                        ter.remove(item)
                        for x in Grammar.rules[''.join(item)]:
                            if x not in Grammar.rules[var] and x != ''.join(item):
                                Grammar.rules[var].append(x)

    @staticmethod
    def uslessSymbol():  # etapa de simplificacao da gramatica - producoes inuteis
        for var, ter in Grammar.rules.items():
            for item in ter:
                for x in item:
                    Grammar.useless_symbol[x] = 0

        for var, numb in Grammar.useless_symbol.items():
            if var in Grammar.variables and numb:
                for x in Grammar.rules[var]:
                    for i in x:
                        Grammar.useless_symbol[i] = 1
                Grammar.variables.remove(var)
                del Grammar.rules[var]

        for var, ter in Grammar.rules.items():
            for item in ter:
                for x in item:
                    Grammar.useless_symbol[x] = 0

        for var, numb in Grammar.useless_symbol.items():
            if var in Grammar.terminals and numb:
                Grammar.terminals.remove(var)

    @staticmethod
    def chomsky():  # forma normal de chomsky - separacao, cada terminal recebe uma variavel
        for x in Grammar.terminals:
            new_ter = []
            new_ter.append(x)
            Grammar.rules['T' + ''.join(x)] = []
            Grammar.rules['T' + ''.join(x)].append(new_ter)
            Grammar.variables.append('T' + ''.join(x))

        for var, ter in Grammar.rules.items():
            for num, item in enumerate(ter):
                new_item = []
                for x in item:
                    if x in Grammar.terminals and var != ''.join('T' + ''.join(x)):
                        new_item.append('T' + ''.join(x))
                    else:
                        new_item.append(x)

                ter[num] = new_item

    @staticmethod
    def chomskyPart2():
        count = 1  # contador de novas variaveis
        new_vars = []
        numb_vars = 0
        while numb_vars != len(Grammar.variables):
            numb_vars = len(Grammar.variables)
            for var in Grammar.variables:
                ter = Grammar.rules[var]
                for num, item in enumerate(ter):
                    new_item = []
                    if len(item) > 2:
                        print("Item %s da var %s tem %d itens" % (''.join(item), var, len(item)))
                        new_vars.append(''.join('V' + str(count)))
                        new_item = [item[0], ''.join('V' + str(count))]
                        Grammar.variables.append(''.join('V' + str(count)))
                        Grammar.rules[''.join('V' + str(count))] = []
                        Grammar.rules[''.join('V' + str(count))].append(item[1:])
                        count += 1
                    else:
                        new_item = item

                    ter[num] = new_item
            print(new_vars)
            new_vars = []