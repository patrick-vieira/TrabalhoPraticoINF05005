import copy
import itertools
import re

import grammarClass

class EarleyParser:

    def __init__(self, gramatica: object) -> object:
        self.gramatica = copy.deepcopy(gramatica) #faz uma copia fisica da gramatica, previne erro caso a gramatica seja alterada
        self.palavra = ''
        self.palavra_reconhecida = False
        self.palavras_reconhecidas = []
        self.reconhecer_palavras_ate_tamanho = 5
        self.simbolo_marcador = 'º'
        self.conjunto_de_producoes_Dn = []

    def to_str(self):

        string_retorno = ''

        for index, Dn in enumerate(self.conjunto_de_producoes_Dn):

            string_retorno += "D" + str(index) + ':\n'

            for variavel, producoes in Dn.items():
                for producao in producoes:
                    string_retorno += '\t' + variavel + ' -> ' + ''.join(producao) + '\n'
        return string_retorno

    def verifica_palavra(self, palavra):

        for pal in palavra:
            if pal not in self.gramatica.terminals:
                return False

        self.conjunto_de_producoes_Dn = []

        self.predict_inicial()

        self.palavra = palavra

        for index, terminal in enumerate(palavra):
            scan_resultado = self.scan(terminal, index)# se conseguiu fazer scan no terminal
            if scan_resultado:
                while self.complete(index+1) or self.predict(index+1) and not self.palavra_reconhecida:  # executa predict e complete até que nem um deles tenha adicionado mais produções em Dn
                    pass
            else:
                return False

        return True


    def predict_inicial(self):

        for variavel, producoes in self.gramatica.rules.items():

            if variavel == ''.join(self.gramatica.initial_var): #procura a produção da variavel inicial

                producoes_da_variavel = {variavel: []}

                for producao in producoes:    #para cada uma das produções da variavel inicial

                    producao_marcada = []

                    producao_marcada.insert(0, self.simbolo_marcador)   # insere o marcador no inicio

                    for var_ter in producao:
                        producao_marcada.append(var_ter)

                    producao_marcada.append('/0') #insere o /0 no final

                    producao_marcada.append('\tpredict inicial') #insere origem

                    producoes_da_variavel[variavel].append(producao_marcada)

                self.conjunto_de_producoes_Dn.append(producoes_da_variavel)

        while self.predict(0):  #executa predict até que nãotenha adicionado mais produções em D0, e complete não precisa pois em D0 marcador não avança
            pass

    def is_slice_in_list(self, s, l):
        len_s = len(s)  # so we don't recompute length of s on every iteration
        return any(s == l[i:len_s + i] for i in range(len(l) - len_s + 1))

    def predict(self, indice_Dn):

        flag_producao_nova = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[indice_Dn])

        for variavel_dn, producoes_dn in producoes_DN.items():   #em todas as produções de dn

            for producao_dn in producoes_dn:

                posicao_marcador = producao_dn.index(self.simbolo_marcador)

                variavel_predict = producao_dn[posicao_marcador+1]

                if variavel_predict in self.gramatica.variables:    #verifica se apos o marcador tem uma variavel e adiciona as produções da gramatica em Dn

                    if variavel_predict not in self.conjunto_de_producoes_Dn[indice_Dn]:#verifica se já não existe a variavel
                        self.conjunto_de_producoes_Dn[indice_Dn][variavel_predict] = []  #inicializa a lista da variavel do predict

                    for producao in self.gramatica.rules[variavel_predict]:   #para cada uma das produções da variavel do predict

                        producao_predict = []

                        producao_predict.insert(0, self.simbolo_marcador)   # insere o marcador no inicio

                        for var_ter in producao:
                            producao_predict.append(var_ter)

                        producao_predict.append('/' + str(indice_Dn)) #insere o /n no final

                        pode_inserir = True

                        for pokayoke in self.conjunto_de_producoes_Dn[indice_Dn][variavel_predict]: #para cada uma das produções da variavel verifica se não tem esse dentro, mas com outra mensagem
                            if self.is_slice_in_list(producao_predict,pokayoke):
                                pode_inserir = False

                        if pode_inserir:
                            producao_que_chamou = ''.join(producao_dn).split('/' + str(indice_Dn))[0]  # TODO arrumar para não aparecer o que gerou a palavra anterior, só por boniteza

                            producao_predict.append('\tpredict da variavel ' + variavel_predict + ' da producao ' + producao_que_chamou)  # insere o /n no final

                            if producao_predict not in self.conjunto_de_producoes_Dn[indice_Dn][variavel_predict]:  # verifica se essa produção já não existe mesmo, nem precisa

                                self.conjunto_de_producoes_Dn[indice_Dn][variavel_predict].append(producao_predict)

                                flag_producao_nova = True




        return flag_producao_nova

    def aux_complete_puxa_avanca_marcador(self, producao_dn):

        contador_producoes_adicionadas = 0

        index_Dn_completado = int(producao_dn[-2].split('/')[1])

        producoes_DN_indice_complete = copy.deepcopy(self.conjunto_de_producoes_Dn[index_Dn_completado])

        for variavel_dn_completo, producoes_dn_completo in producoes_DN_indice_complete.items():  # em todas as produções do dn-completado avança o marcador

                posicao_marcador = producao.index(self.simbolo_marcador)

                variavel = producao[posicao_marcador + 1]

                if variavel_completa == variavel:

                    producao[posicao_marcador + 1], producao[posicao_marcador] = producao[posicao_marcador], producao[posicao_marcador + 1]  # move marcador para direita

                    producao[-1] = '\tcomplete da producao ' + ''.join(producao_dn).split('/' + str(index_Dn_completado))[0]

                    else:
                        self.conjunto_de_producoes_Dn[-1][variavel_dn_completo] = []
                        self.conjunto_de_producoes_Dn[-1][variavel_dn_completo].append(producao)
                        contador_producoes_adicionadas = contador_producoes_adicionadas + 1

        return contador_producoes_adicionadas

    def trigger_complete(self, producao_dn):

        posicao_marcador = producao_dn.index(self.simbolo_marcador)

        variavel_direita_marcador = producao_dn[posicao_marcador + 1]

        onde_palavra_foi_gerada = producao_dn[-2]  # TODO pegar com regex

        if variavel_direita_marcador == onde_palavra_foi_gerada:  # verifica se apos o marcador tem um /n
            return True

        return False

    def complete(self, indice_Dn): #se o marcador esta no final da gramatica (antes do /n), 'puxa' todas as produções do /n que tenham marcador antes de variavel, mas movendo o marcador para direita

        flag_producao_nova = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[indice_Dn])

        for variavel_dn, producoes_dn in producoes_DN.items():  # em todas as produções de dn

            for producao_dn in producoes_dn:

                if self.trigger_complete(producao_dn):

                self.palavra_reconhecida = True

                    if cont_avancos > 1:  #todo ta muito feia essa logica aqui, da pra melhorar
                        flag_producao_nova = True


        if ''.join(self.gramatica.initial_var) in self.conjunto_de_producoes_Dn[indice_Dn] and len(self.conjunto_de_producoes_Dn) == len(self.palavra):   #verifica se tem a variavel inicial no ultimo dn e se n é do tamanho da palavra

            for producoes_inicial in self.conjunto_de_producoes_Dn[indice_Dn][''.join(self.gramatica.initial_var)]:  #para cada producao de d0 verifica a posicao do marcador

                posicao_marcador = producoes_inicial.index(self.simbolo_marcador)

                simbolo_direita_marcador = producoes_inicial[posicao_marcador + 1]

                if simbolo_direita_marcador == '/0':

                    self.palavras_reconhecidas.append(self.palavra)
                    self.palavra_reconhecida = True
                    return False

        return flag_producao_nova

    def scan(self, terminal_procurado, indice_dn): #procura no D-index por alguma produção onde o terminal do lado direito do marcador, se sim cria D-index+1

        flag_encontrou = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[indice_dn])

        for variavel_dn, producoes_dn in producoes_DN.items():   #em todas as produções de dn

            producoes_do_scan = {variavel_dn: []}

            for producao_dn in producoes_dn: #busca todos os scans possiveis da variavel dn

                posicao_marcador = producao_dn.index(self.simbolo_marcador)

                terminal_scan = producao_dn[posicao_marcador+1]

                if terminal_scan in self.gramatica.terminals and terminal_scan == terminal_procurado:  #verifica se apos o marcador tem um terminal e redundantemente se é a variavel que procuramos

                    producao_escaneada = copy.deepcopy(producao_dn)

                    producao_escaneada[posicao_marcador+1], producao_escaneada[posicao_marcador] = producao_escaneada[posicao_marcador], producao_escaneada[posicao_marcador+1] #move marcador para direita

                    producao_escaneada[-1] = '\tscan terminal ' + terminal_procurado  # insere origem

                    producoes_do_scan[variavel_dn].append(producao_escaneada)

            #verificar se essas producões tem ao menos uma producao e já não esta no DN
            if producoes_do_scan not in self.conjunto_de_producoes_Dn[indice_dn][variavel_dn] and len(producoes_do_scan[variavel_dn]) > 0:

                self.conjunto_de_producoes_Dn.append(producoes_do_scan)

                flag_encontrou = True

        return flag_encontrou

    def combinacoes_palavras_possiveis(self):

        for tamanho_palavra in range(1, self.reconhecer_palavras_ate_tamanho):

            for combinacao in itertools.product(self.gramatica.terminals, repeat=tamanho_palavra):

                resultado = self.verifica_palavra(combinacao)

                print(str(resultado) + str(combinacao))

                if resultado:
                    self.palavras_reconhecidas.append(combinacao)

        return self.palavras_reconhecidas


def earlyParser(fileName, stringPalavra):
    printFinal = []
    palavra = re.split(r",", stringPalavra)
    print(palavra)

    with open(fileName) as f:
        lines = f.read()

    if lines:
        grammar = grammarClass.Grammar(lines)
        printFinal.append('Gramática extraída do arquivo ' + fileName)
        printFinal.append(str(grammar))

        oParcer = EarleyParser(grammar)

        resultado = oParcer.verifica_palavra(palavra)

        printFinal.append('Palavra de entrada:' + ''.join(palavra))
        printFinal.append(oParcer.to_str())

        if resultado == True:
            printFinal.append('Palavra é reconhecida pela gramática')
        else:
            printFinal.append('Palavra não é reconhecida pela gramática')

        printFinal.append(str(resultado))


