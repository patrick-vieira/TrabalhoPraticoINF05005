import copy
import re


class Grammar:  # Grammar: salva variaveis, terminais e regras

    def __init__(self, linhas):
        self.terminals = []
        self.variables = []
        self.initial_var = []
        self.rules = {}  # rules: um dicionario que mantem todas as regras salvas usando as variaveis como indice
        self.empty_word = {}
        self.useless_symbol = {}
        self.accepts_empty = 0
        self.has_empty = 0

        self.read_grammar(linhas)

    def __str__(self):
        rules = []
        temp_ter = []

        for var, ter in sorted(self.rules.items()):
            for t in sorted(ter):
                temp_ter.append(''.join(t))
            rules.append("%s -> %s" % (var, ' | '.join(temp_ter)))
            temp_ter = []

        result_Grammar = ['Terminais: ' + ', '.join(sorted(self.terminals)),
                          'Variaveis: ' + ', '.join(sorted(self.variables)),
                          'Simbolo inicial: ' + ' '.join(self.initial_var),
                          'Regras: {' + ',\n'.join(rules) + '}']

        return '\n\n'.join(result_Grammar)

    def read_grammar(self, lines):
        file_split = re.split(r"#Terminais|#Variaveis|#Inicial|#Regras", lines)
        file_rules = re.split(r" > |\n", file_split[4])
        exp = r"\[ ([^]]*) \]"
        for index, line in enumerate(file_split):
            if index == 1:
                searchObj = re.findall(exp, line)
                if searchObj:
                    self.terminals = searchObj
            elif index == 2:
                searchObj = re.findall(exp, line)
                if searchObj:
                    self.variables = searchObj
                    for x in searchObj:
                        self.rules[x] = []
                        self.empty_word[x] = 0
                        self.useless_symbol[x] = 1

            elif index == 3:
                searchObj = re.findall(exp, line)
                if searchObj:
                    self.initial_var = searchObj
                    self.useless_symbol[''.join(searchObj)] = 0

            elif index == 4:
                for index, l in enumerate(file_rules):
                    if index % 2 != 0:
                        searchObj = re.findall(exp, l)
                    else:
                        searchObj2 = re.findall(exp, l)
                        if searchObj2:
                            self.rules[''.join(searchObj)].append(searchObj2)
                            if 'V' in searchObj2:
                                print("Grammar.rules[%s].append(%s)" % (''.join(searchObj), searchObj2))
                                self.has_empty = 1
                                self.empty_word[''.join(searchObj)] = 1

    def simplificacao_stp1_prod_vazias(self):
        quant_var = 0
        while quant_var <= len(self.variables):
            for var, ter in self.rules.items():
                for item in ter:
                    rules_count = 0
                    for x in item:
                        if x in self.variables and self.empty_word[x]:
                            rules_count += 1
                    if rules_count == len(item):
                        self.empty_word[var] = 1
            quant_var += 1

    def simplificacao_stp2_prod_vazias(self):
        for var, ter in self.rules.items():
            print("EITAAAAAAAAAA: %s" % self.empty_word)
            for item in self.rules[var]:
                for x in item:
                    if x in self.variables:
                        if self.empty_word[x]:
                            aux = list(item)
                            aux.remove(x)
                            if aux and aux not in self.rules[var]:
                                self.rules[var].append(aux)

    def simplificacao_stp3_prod_vazias(self):
        for var, ter in self.rules.items():
            for item in ter:
                if 'V' in item:
                    ter.remove(item)
                    print("churros")
            if ''.join(self.initial_var) == var and self.empty_word[var]:
                self.rules[var].append(list("V"))
                self.accepts_empty = 1

    def simplificacao_stp4_exclusao_prod_simples(self):
        for var, ter in self.rules.items():
            print("VARIAVEL ATUAL: %s" % var)
            i = 0
            while i != len(ter):
                i = len(ter)
                for item in ter:
                    print("ITEM ATUAL: %s" % item)
                    if ''.join(item) in self.variables:
                        print(self.variables)
                        ter.remove(item)
                        for x in self.rules[''.join(item)]:
                            if x not in self.rules[var] and x != ''.join(item):
                                self.rules[var].append(x)

    def simplificacao_stp5_exclusao_prod_inuteis(self):

        for x in self.variables:
            ter = self.rules[x]
            if not ter:
                print("YAAAAAAAAAY")
                self.useless_symbol[x] = 1
                self.rules.pop(x)
                self.variables.remove(x)
                for var, ter in self.rules.items():
                    for item in ter:
                        for i in item:
                            if x == i:
                                item.remove(x)

        for var, ter in self.rules.items():
            for item in ter:
                for x in item:
                    self.useless_symbol[x] = 0

        for var, numb in self.useless_symbol.items():
            if var in self.variables and numb:
                for x in self.rules[var]:
                    for i in x:
                        self.useless_symbol[i] = 1
                self.variables.remove(var)
                del self.rules[var]

        for var, ter in self.rules.items():
            for item in ter:
                for x in item:
                    self.useless_symbol[x] = 0

        for var, numb in self.useless_symbol.items():
            if var in self.terminals and numb:
                self.terminals.remove(var)

    def chomsky_stp1_separacao(self):  # forma normal de chomsky - separacao, cada terminal recebe uma variavel
        if self.accepts_empty:
            return "Forma normal de Chomsky \n\n A gramática aceita palavra vazia."

        for x in self.terminals:
            new_ter = [x]
            self.rules['T' + ''.join(x)] = []
            self.rules['T' + ''.join(x)].append(new_ter)
            self.variables.append('T' + ''.join(x))

        for var, ter in self.rules.items():
            for num, item in enumerate(ter):
                new_item = []
                for x in item:
                    if x in self.terminals and var != ''.join('T' + ''.join(x)):
                        new_item.append('T' + ''.join(x))
                    else:
                        new_item.append(x)
                ter[num] = new_item

    def chomsky_stp2_novas_variaveis(self):
        count = 1  # contador de novas variaveis
        new_vars = []
        numb_vars = 0

        while numb_vars != len(self.variables):
            numb_vars = len(self.variables)
            for var in self.variables:
                ter = self.rules[var]
                for num, item in enumerate(ter):
                    new_item = []
                    if len(item) > 2:
                        print("Item %s da var %s tem %d itens" % (''.join(item), var, len(item)))
                        new_vars.append(''.join('V' + str(count)))
                        new_item = [item[0], ''.join('V' + str(count))]
                        self.variables.append(''.join('V' + str(count)))
                        self.rules[''.join('V' + str(count))] = []
                        self.rules[''.join('V' + str(count))].append(item[1:])
                        count += 1
                    else:
                        new_item = item

                    ter[num] = new_item
            print(new_vars)
            new_vars = []

    def to_chomsky(self):
        temp = copy.deepcopy(self)
        temp.chomsky_stp1_separacao()
        temp.chomsky_stp2_novas_variaveis()
        return temp

    def simplificar(self):
        temp = copy.deepcopy(self)
        temp.simplificacao_stp1_prod_vazias()
        temp.simplificacao_stp2_prod_vazias()
        temp.simplificacao_stp3_prod_vazias()
        return temp
