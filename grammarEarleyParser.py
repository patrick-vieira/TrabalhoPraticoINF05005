import copy
import itertools
import re

import grammarClass


class struct_elemento_tabela:
    index = 0
    variavel = ''
    producao = []
    posicao = []
    back_pointer = []
    operacao = ''

    def to_string(self):
        ret = ''

        ret += '|\t ' + str(self.index) + '\t |'
        ret += '|\t ' + self.variavel + '\t |'
        ret += '|\t ' + ' '.join(self.producao) + '\t\t |'
        ret += '|\t ' + str(self.posicao) + '\t |'
        ret += '|\t ' + str(self.back_pointer) + '\t |'
        ret += '|\t ' + self.operacao + '\t\t|'

        return ret


class EarleyParser:
    def __init__(self, gramatica: object) -> object:
        self.arvore_var = []
        self.arvore = []
        self.NEXT = 0
        self.palavra_arvore = []
        self.raizes_das_arvores = []
        self.gramatica = copy.deepcopy(
            gramatica)  # faz uma copia fisica da gramatica, previne erro caso a gramatica seja alterada
        self.palavra = ''
        self.palavra_reconhecida = False
        self.status_aceitacao = ''
        self.palavras_reconhecidas = []
        self.reconhecer_palavras_ate_tamanho = 5
        self.simbolo_marcador = 'º'
        self.conjunto_de_producoes_Dn = []
        self.tabela = []
        self.chart = []
        self.contador = 0

    def to_str(self):

        string_retorno = ''

        for index, Dn in enumerate(self.conjunto_de_producoes_Dn):

            string_retorno += "D" + str(index) + ':\n'

            for elemento in Dn:
                string_retorno += '\n'
                string_retorno += elemento.to_string()

            string_retorno += '\n'

        return string_retorno

    def verifica_palavra(self, palavra):

        for pal in palavra:
            if pal not in self.gramatica.terminals:
                return "Terminais desconhecidos"

        self.palavra_reconhecida = False

        self.conjunto_de_producoes_Dn = []

        self.predict_inicial()

        self.palavra = palavra

        adc_comp = True
        adc_pred = True

        for index, terminal in enumerate(palavra):
            rodar_mais = 5
            scan_resultado = self.scan(terminal, index)  # se conseguiu fazer scan no terminal
            if scan_resultado:
                while adc_comp or adc_pred or rodar_mais > 0 and not self.palavra_reconhecida:  # executa predict e complete até que nem um deles tenha adicionado mais produções em Dn

                    adc_comp = self.complete()

                    adc_pred = self.predict(index + 1)

                    if not (adc_pred and adc_comp):
                        rodar_mais -= 1
            else:
                break

        return self.complete_verifica_aceitacao()

    @property
    def proxima_pos(self):

        ret = self.contador

        self.contador += 1

        return ret


    def predict_inicial(self):

        for variavel, producoes in self.gramatica.rules.items():

            if variavel == ''.join(self.gramatica.initial_var):  # procura a produção da variavel inicial

                lista_predict_inicial = []

                for producao in producoes:  # para cada uma das produções da variavel inicial cria uma linha da tabela

                    elemento_D0 = struct_elemento_tabela()

                    elemento_D0.index = self.proxima_pos

                    producao_marcada = []

                    producao_marcada.insert(0, self.simbolo_marcador)  # insere o marcador no inicio

                    for var_ter in producao:
                        producao_marcada.append(var_ter)

                    elemento_D0.variavel = variavel

                    elemento_D0.producao = producao_marcada

                    elemento_D0.posicao = [0, 0]

                    elemento_D0.back_pointer = []

                    elemento_D0.operacao = 'Predict inicial'

                    lista_predict_inicial.append(elemento_D0)

                self.conjunto_de_producoes_Dn.append(lista_predict_inicial)

        while self.predict(0):  # executa predict até que nãotenha adicionado mais produções em D0, e complete não precisa pois em D0 marcador não avança
            pass

    def procura_mesma_producao_no_Dn(self, index, variavel, producao, posicao, back_pointer):

        ###varre a lista de elementos de DN e verificar em cada um deles se já não existe essa produção

        for elemento in self.conjunto_de_producoes_Dn[index]:
            if elemento.variavel == variavel and elemento.producao == producao and elemento.posicao == posicao and elemento.back_pointer == back_pointer:
                return False
        return True

    def predict(self, indice_Dn):

        flag_producao_nova = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[indice_Dn])

        for elemento_tabela in producoes_DN:

            posicao_marcador = elemento_tabela.producao.index(self.simbolo_marcador)

            if posicao_marcador == len(elemento_tabela.producao)-1:   ##marcador no fim da produção não precisa de predict
                continue

            variavel_predict = elemento_tabela.producao[posicao_marcador + 1]

            if variavel_predict in self.gramatica.variables:  # verifica se apos o marcador tem uma variavel e adiciona as produções da gramatica em Dn

                for producao in self.gramatica.rules[variavel_predict]:  # para cada uma das produções da variavel do predict

                    producao_predict = []

                    producao_predict.insert(0, self.simbolo_marcador)  # insere o marcador no inicio

                    for var_ter in producao:
                        producao_predict.append(var_ter)

                    if self.procura_mesma_producao_no_Dn(indice_Dn, variavel_predict, producao_predict,
                                                         [indice_Dn, indice_Dn], []):
                        # elemento_Dn = struct_elemento_tabela(self.proxima_pos)  # se a prução não existe ainda, cria novo elemento

                        elemento_Dn = struct_elemento_tabela()

                        elemento_Dn.index = self.proxima_pos

                        elemento_Dn.variavel = variavel_predict

                        elemento_Dn.producao = producao_predict

                        elemento_Dn.posicao = [indice_Dn, indice_Dn]

                        elemento_Dn.back_pointer = []

                        elemento_Dn.operacao = 'Predict'

                        self.conjunto_de_producoes_Dn[indice_Dn].append(elemento_Dn)

                        flag_producao_nova = True

        return flag_producao_nova

    def scan(self, terminal_procurado,indice_Dn):  # procura no D-index por alguma produção onde o terminal do lado direito do marcador, se sim cria D-index+1

        flag_encontrou = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[indice_Dn])

        for elemento in producoes_DN:

            variavel_dn = elemento.variavel

            producao_dn = elemento.producao

            posicao_marcador = producao_dn.index(self.simbolo_marcador)

            if posicao_marcador == len(elemento.producao)-1:   ##marcador no fim da produção não precisa de predict
                continue

            terminal_scan = producao_dn[posicao_marcador + 1]

            if terminal_scan in self.gramatica.terminals and terminal_scan == terminal_procurado:  # verifica se apos o marcador tem um terminal e redundantemente se é a variavel que procuramos

                producao_escaneada = copy.deepcopy(producao_dn)

                producao_escaneada[posicao_marcador + 1], producao_escaneada[posicao_marcador] = producao_escaneada[
                                                                                                     posicao_marcador], \
                                                                                                 producao_escaneada[
                                                                                                     posicao_marcador + 1]  # move marcador para direita

                elemento_Dn = struct_elemento_tabela()

                elemento_Dn.index = self.proxima_pos

                elemento_Dn.variavel = variavel_dn

                elemento_Dn.producao = producao_escaneada

                elemento_Dn.posicao = []
                elemento_Dn.posicao.append(elemento.posicao[0])
                elemento_Dn.posicao.append(indice_Dn + 1)

                elemento_Dn.back_pointer = []

                elemento_Dn.operacao = 'Scan'

                if len(self.conjunto_de_producoes_Dn) - 1 == indice_Dn + 1:  # se já existe a lista Dn append
                    self.conjunto_de_producoes_Dn[indice_Dn + 1].append(elemento_Dn)

                else:  # se ainda n existe uma lista nova cria uma
                    self.conjunto_de_producoes_Dn.append([elemento_Dn])

                flag_encontrou = True

        return flag_encontrou

    def complete(self):  # se o marcador esta no final da gramatica (antes do /n), 'puxa' todas as produções do /n que tenham marcador antes de variavel, mas movendo o marcador para direita

        flag_producao_nova = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[-1])

        for elemento in producoes_DN:

            variavel_dn = elemento.variavel

            producao_dn = elemento.producao

            if producao_dn[-1] == self.simbolo_marcador:  # se no fim da producao esta o marcador

                origem_prod = elemento.posicao[0]

                cont_avancos = self.complete_puxa_avanca_marcador(variavel_dn, origem_prod, elemento.index)

                if cont_avancos > 0:  # todo ta muito feia essa logica aqui, da pra melhorar
                    flag_producao_nova = True

        return flag_producao_nova

    def complete_puxa_avanca_marcador(self, variavel_dn, origem_prod, index_back_pointer):

        contador_producoes_adicionadas = 0

        producoes_DN_que_completou = copy.deepcopy(self.conjunto_de_producoes_Dn[origem_prod])

        for elemento_dn_completo in producoes_DN_que_completou:  # para cada elemento que completou

            variavel_dn_completo = elemento_dn_completo.variavel

            producao_dn_completo = elemento_dn_completo.producao

            posicao_marcador_dn_completo = producao_dn_completo.index(self.simbolo_marcador)

            if posicao_marcador_dn_completo == len(elemento_dn_completo.producao)-1:   ##marcador no fim da produção não precisa de predict
                continue

            variavel_direita_do_marcador_dn_completo = producao_dn_completo[posicao_marcador_dn_completo + 1]

            if variavel_direita_do_marcador_dn_completo == variavel_dn:

                producao_dn_completo[posicao_marcador_dn_completo + 1], producao_dn_completo[posicao_marcador_dn_completo] = \
                    producao_dn_completo[posicao_marcador_dn_completo], producao_dn_completo[posicao_marcador_dn_completo + 1]  # move marcador para direita

                elemento_dn_completo.operacao = 'Complete'

                elemento_dn_completo.posicao[1] = len(self.conjunto_de_producoes_Dn) - 1

                elemento_dn_completo.back_pointer.append(index_back_pointer)

                if self.procura_mesma_producao_no_Dn(len(self.conjunto_de_producoes_Dn) - 1, variavel_dn_completo, producao_dn_completo, elemento_dn_completo.posicao, elemento_dn_completo.back_pointer):
                    elemento_dn_completo.index = self.proxima_pos
                    self.conjunto_de_producoes_Dn[-1].append(elemento_dn_completo)

                    contador_producoes_adicionadas += 1

        return contador_producoes_adicionadas

    def trigger_complete(self, producao_dn):

        posicao_marcador = producao_dn.index(self.simbolo_marcador)

        variavel_direita_marcador = producao_dn[posicao_marcador + 1]

        onde_palavra_foi_gerada = producao_dn[-2]  # TODO pegar com regex

        if variavel_direita_marcador == onde_palavra_foi_gerada:  # verifica se apos o marcador tem um /n
            return True

        return False

    def complete_verifica_aceitacao(self):

        self.raizes_das_arvores = []

        if len(self.conjunto_de_producoes_Dn) - 1 == len(self.palavra):

            str_mensagem = 'Palavra: ' + ' '.join(self.palavra)
            str_mensagem += '\nArvore apartir do(s) elemento(s):'

            producoes_D_ultimo = copy.deepcopy(self.conjunto_de_producoes_Dn[-1])

            for elemento in producoes_D_ultimo: #para cada elemento da ultima lista

                if elemento.posicao == [0, len(self.palavra)] and elemento.producao[-1] == self.simbolo_marcador:  #verifica se foi criado em 0 e terminou em Dn
                    self.raizes_das_arvores.append(elemento)
                    str_mensagem += "\n" + elemento.to_string()

            if len(self.raizes_das_arvores) > 0:

                print(str_mensagem)

                return True

            else:
                print('Palavra não foi aceita.')

        return False

    def combinacoes_palavras_possiveis(self, tamanho_entrada=0):

        if tamanho_entrada > 0:
            self.reconhecer_palavras_ate_tamanho = tamanho_entrada

        for tamanho_palavra in range(1, self.reconhecer_palavras_ate_tamanho):

            for combinacao in itertools.product(self.gramatica.terminals, repeat=tamanho_palavra):

                palavra_teste = []

                for term in combinacao:
                    palavra_teste.append(term)

                print('Testando combinação: ' + str(combinacao))

                resultado = self.verifica_palavra(palavra_teste)

                if resultado:

                    self.palavras_reconhecidas.append(combinacao)

        return self.palavras_reconhecidas

    def gera_arvore_derivacao(self, indice_raiz):
        """ver o PDF que o sor colocou no moodle
        e o txt resultado JM para palavra do PDF
        nele tem todos os elementos para fazer a afunção,
        no final coloquei como é feita a chamada

        recurção simples

        raiz(index):
            apend(raiz(todos back_pointers))
            return  var ou terminal
        """

        pass



''' Esse algoritmo reconhece palavras sem usar earley, apenas com a arvore.

    def valida_avanco_caracter(self, token):

        next = self.palavra_arvore[self.NEXT]

        if token == next:
            self.NEXT += 1
            # print("chegou no terminal: " + token)
            self.arvore_var.append(token)
            # self.arvore_var.append(']')
            return True

        return False

    def arvore_testar_variavel(self, variavel):

        next = self.NEXT  # salvando pra quando avançar mas n estar ok

        for token in self.gramatica.rules[variavel]:  # testa as produções dessa variavel

            self.NEXT = next

            if self.arvore_testar_producao(token):
                # self.arvore_var.append(''.join(variavel)) # trocar de posição pois a var que gerou o terminal é essa
                return True

    def arvore_testar_producao(self, token):

        if ''.join(token) in self.gramatica.terminals:  # se é um terminal
            if self.valida_avanco_caracter(''.join(token)):
                print("--------Produção anterior levou para terminal: " + ''.join(token))
                return True
            return False  # chegou em um terminal mas não é o que queremos

        if ''.join(token) in self.gramatica.rules.keys():  # se é variavel

            if self.arvore_testar_variavel(''.join(token)):
                print("-------Produção : " + ''.join(token))
                return True
            else:
                return False

        for producao in token:  # token é uma producao(lado direit) testar todas as suas variaveis e terminais elas se alguma aceitar continua

            # print("Produção: " + ''.join(token) + " -> " + producao)
            print("Para : " + producao + ' da produção: ' + ''.join(token))

            if not self.arvore_testar_producao(producao):  # se aceitou para
                print('=======  ' + producao + " não aceita")
                return False

            print('=======  Produção aceita ' + producao)

        return True

    def arvore_variavel_inicial(self):

        next = self.NEXT  # salvando pra quando avançar mas n estar ok

        for producoes_da_variavel_inicial in self.gramatica.rules[''.join(self.gramatica.initial_var)]:

            self.NEXT = next

            if self.arvore_testar_producao(producoes_da_variavel_inicial):  # se a producao finalizou

                if self.NEXT == len(self.palavra_arvore):
                    print("Produção inicial: " + ''.join(self.gramatica.initial_var) + ' aceitou em ' + ''.join(
                        producoes_da_variavel_inicial))
                    return True

                else:
                    print("Produção inicial: " + ''.join(self.gramatica.initial_var) + ' não aceitou em' + ''.join(
                        producoes_da_variavel_inicial))

        return False

    def gera_arvore_derivacao(self, palavra_entrada):

        tokens = []
        for var in self.gramatica.variables:
            tokens.append(var)
        for ter in self.gramatica.terminals:
            tokens.append(ter)

        self.palavra_arvore = []

        for terminal in palavra_entrada:
            self.palavra_arvore.append(terminal)

        self.arvore.append(''.join(self.gramatica.initial_var))  # adiocina simbolo inicial na arvore

        self.NEXT = 0

        palavra_aceita = self.arvore_variavel_inicial()

        if palavra_aceita:
            print("\n======================= \n=======================  Aceitou: " + ''.join(
                self.palavra_arvore) + "\n=======================")
        else:

            print("\n======================= \n=======================  Não Aceitou: " + ''.join(
                self.palavra_arvore) + "\n=======================")

        return palavra_aceita
'''



def earlyParser(fileName, stringPalavra):
    printFinal = []
    palavra = re.split(r" ", stringPalavra)
    print(palavra)

    with open(fileName) as f:
        lines = f.read()

    if lines:
        grammar = grammarClass.Grammar(lines)
        printFinal.append('Gramática extraída do arquivo ' + fileName)
        printFinal.append(str(grammar))

        oParcer = EarleyParser(grammar)

        resultado = oParcer.verifica_palavra(palavra)

        printFinal.append('Palavra de entrada: ' + ' '.join(palavra))

        raizes = 'Arvore apartir do(s) elemento(s):'

        for raiz in oParcer.raizes_das_arvores:
            raizes += '\n\t ' + raiz.to_string()

        printFinal.append(raizes)

        #printFinal.append(oParcer.status_aceitacao)

        printFinal.append(oParcer.to_str())

        printFinal.append(str(resultado))

    return '\n----------------------------------------------------------------------\n'.join(printFinal)


def combinacoes(fileName, tamanho):
    printFinal = []

    with open(fileName) as f:
        lines = f.read()

    if lines:
        grammar = grammarClass.Grammar(lines)
        printFinal.append('Gramática extraída do arquivo ' + fileName)
        printFinal.append(str(grammar))

        oParcer = EarleyParser(grammar)

        reconhecer_palavras_ate = int(tamanho) + 1

        oParcer.combinacoes_palavras_possiveis(reconhecer_palavras_ate)

        printFinal.append('Até tamanho: ' + tamanho)

        resultado = []

        for item in oParcer.palavras_reconhecidas:
            if ''.join(item) not in resultado:
                resultado.append(''.join(item))

        printFinal.append(str('\n'.join(resultado)))

    return '\n----------------------------------------------------------------------\n'.join(printFinal)


def debug():
    fileName = 'C:\\users\\vieir\\Documents\\GitHub\\TrabalhoPraticoINF05005\\Earley-JM.txt'

    with open(fileName) as f:
        lines = f.read()

    if lines:
        grammar = grammarClass.Grammar(lines)

        oParcer = EarleyParser(grammar)

        #resultado = oParcer.verifica_palavra(('int',))




        resultado = oParcer.verifica_palavra(('astronomers', 'saw', 'stars', 'with', 'ears'))
        print(oParcer.to_str())
        resultado = oParcer.verifica_palavra(('(', 'int', '+', 'int', ')'))
        # resultado = oParcer.verifica_palavra(('int',))
        #
        # oParcer.gera_arvore_derivacao(('(', 'int', ')'))
        # oParcer.gera_arvore_derivacao(('int', '+', 'int'))
        resultado = oParcer.gera_arvore_derivacao(('int', '+', 'int', '+', 'int'))
        resultado = oParcer.gera_arvore_derivacao(('int', '+', '(', 'int', ')'))

        resultado = oParcer.gera_arvore_derivacao(('int', 'int', '+', 'int', '+', 'int'))
        resultado = oParcer.gera_arvore_derivacao(('(', '+', 'int', '+', 'int', ')', '+', 'int'))
        resultado = oParcer.gera_arvore_derivacao(('(', 'int', '+', 'int', ')', '+', 'int'))
        resultado = oParcer.gera_arvore_derivacao(('(', 'int', '+', 'int', ')', '*', 'int'))

        print(oParcer.to_str())

        print(oParcer.status_aceitacao)
        reconhecer_palavras_ate = 7
        oParcer.combinacoes_palavras_possiveis(reconhecer_palavras_ate)

        print("As palavras reconhecidas pela gramatica com tamanho até " + str(
            reconhecer_palavras_ate) + " são::\n" + str(oParcer.palavras_reconhecidas))


#debug()
