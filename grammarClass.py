import copy
import re


class Grammar:  # Grammar: salva variaveis, terminais e regras

    def __init__(self, linhas):
        self.terminals = []
        self.variables = []
        self.initial_var = []
        self.rules = {}  # rules: um dicionario que mantem todas as regras salvas usando as variaveis como indice
        self.empty_word = {}  # Vlambda : conjunto (dicionario) das variaveis que constituem produções vazias(direta ou indiretamente)
        self.useless_symbol = {}  # dicionario com os simbolos inuteis
        self.accepts_empty = 0
        self.has_empty = 0
        self.is_simplificada = 0
        self.is_fnc = 0

        self.read_grammar(linhas)


    #sobreescrita da função str() para mostrar a gramatica de maneira mais didatica
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


    #parser do arquivo de texto
    def read_grammar(self, lines):
        file_split = re.split(r"#Terminais|#Variaveis|#Inicial|#Regras", lines)
        file_rules = re.split(r" > |\n", file_split[4])
        exp = r"\[ ([^]]*) \]"  # expressao regular para pegar conteudo dentro de []
        for index, line in enumerate(file_split):
            if index == 1:  # terminais
                searchObj = re.findall(exp, line)
                if searchObj:
                    self.terminals = searchObj  # preenchendo lista de terminais
            elif index == 2: #variaveis
                variaveis = re.findall(exp, line)
                if variaveis:
                    self.variables = variaveis  # preenchendo lista de variaveis
                    for variavel in variaveis:
                        self.rules[variavel] = []  # inicializa dicionario de producoes, indice são as variaveis
                        self.empty_word[variavel] = 0  # inicializa Vlambda
                        self.useless_symbol[variavel] = 1  # inicializa todas produções como contendo simbolos inuteis

            elif index == 3:  # simbolo inicial
                searchObj = re.findall(exp, line)
                if searchObj:
                    self.initial_var = searchObj
                    self.useless_symbol[''.join(searchObj)] = 0  # produção do simbolo inicial não é mais inutil

            elif index == 4:  # produções
                for index, l in enumerate(file_rules): #para cada produção
                    if index % 2 != 0: #as produções fora divididas a esquerda e direita do simbolo '>', esquerda impar direita par
                        esquerdaProd = re.findall(exp, l)  #variavel, lado esquerdo da '>', ou seja quando o index for impar
                    else:
                        direitaProd = re.findall(exp, l)
                        if direitaProd:
                            self.rules[''.join(esquerdaProd)].append(direitaProd)
                            #verifica se tem palavra vazia, se sim adiciona essa variavel a Vlambda (empty_word)
                            if 'V' in direitaProd:
                                print("Grammar.rules[%s].append(%s)" % (''.join(esquerdaProd), direitaProd))
                                self.has_empty = 1
                                self.empty_word[''.join(esquerdaProd)] = 1

    #etapa 1 Completa Vlambda (empty_word) indiretamente
    def simplificacao_stp1_prod_vazias(self):
        quant_var = 0
        while quant_var <= len(self.variables):
            for var, ter in self.rules.items():
                for item in ter:
                    rules_count = 0
                    for x in item:
                        if x in self.variables and self.empty_word[x]: ##
                            rules_count += 1
                    if rules_count == len(item):
                        self.empty_word[var] = 1
                    quant_var += 1

    #etapa 2 gera as combiações possiveis das produções que contem uma variavel em Vlambda
    def simplificacao_stp2_prod_vazias(self):
        for var, ter in self.rules.items():
            for item in self.rules[var]:
                for x in item:
                    if x in self.variables:
                        if self.empty_word[x]:
                            aux = list(item)
                            aux.remove(x)
                            if aux and aux not in self.rules[var]:
                                self.rules[var].append(aux)

    #etapa 3 substitui a variavel pela produção
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
        self.is_fnc = 1
        return temp

    def simplificar(self):
        temp = copy.deepcopy(self)
        temp.simplificacao_stp1_prod_vazias()
        temp.simplificacao_stp2_prod_vazias()
        temp.simplificacao_stp3_prod_vazias()
        self.is_simplificada = 1
        return temp
