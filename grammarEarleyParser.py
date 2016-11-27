import copy
import itertools
import re

import grammarClass

class EarleyParser:

    def __init__(self, gramatica: object) -> object:
        self.arvore = []
        self.NEXT = 0
        self.palavra_arvore = []
        self.gramatica = copy.deepcopy(gramatica) #faz uma copia fisica da gramatica, previne erro caso a gramatica seja alterada
        self.palavra = ''
        self.palavra_reconhecida = False
        self.status_aceitacao = ''
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
                return "Terminais desconhecidos"

        self.palavra_reconhecida = False

        self.conjunto_de_producoes_Dn = []

        self.predict_inicial()

        self.palavra = palavra

        adc_comp = True
        adc_pred = True


        for index, terminal in enumerate(palavra):
            rodar_mais = 5
            scan_resultado = self.scan(terminal, index)# se conseguiu fazer scan no terminal
            if scan_resultado:
                while adc_comp or adc_pred or rodar_mais > 0 and not self.palavra_reconhecida:  # executa predict e complete até que nem um deles tenha adicionado mais produções em Dn

                    adc_comp = self.complete()

                    adc_pred = self.predict(index+1)

                    if not (adc_pred and adc_comp):
                        rodar_mais -= 1
            else:
                break

        return self.complete_verifica_aceitacao()

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

    def aux_complete_puxa_avanca_marcador(self, variavel_completa, producao_dn):

        contador_producoes_adicionadas = 0

        origem_prod = int(producao_dn[-2].split('/')[1])

        producoes_DN_que_completou = copy.deepcopy(self.conjunto_de_producoes_Dn[origem_prod])

        for var, producoes in producoes_DN_que_completou.items():

            for producao in producoes:

                posicao_marcador = producao.index(self.simbolo_marcador)

                variavel = producao[posicao_marcador + 1]

                if variavel_completa == variavel:

                    producao[posicao_marcador + 1], producao[posicao_marcador] = producao[posicao_marcador], producao[posicao_marcador + 1]  # move marcador para direita

                    producao[-1] = '\tcomplete da producao ' + variavel_completa + ' ->' + ''.join(producao_dn).split('/' + str(origem_prod))[0]

                    if var in self.conjunto_de_producoes_Dn[-1]: #verifica se a variavel já existe no dn se existe só adiciona, se não cria e acidiona

                        if producao not in self.conjunto_de_producoes_Dn[-1][var]:
                            self.conjunto_de_producoes_Dn[-1][var].append(producao)

                            contador_producoes_adicionadas += 1

                    else:
                        self.conjunto_de_producoes_Dn[-1][var] = []

                        self.conjunto_de_producoes_Dn[-1][var].append(producao)

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

        if len(self.conjunto_de_producoes_Dn) - 1 == len(self.palavra):

            if ''.join(self.gramatica.initial_var) in self.conjunto_de_producoes_Dn[-1].keys():
                for producao_da_inicial in self.conjunto_de_producoes_Dn[-1][''.join(self.gramatica.initial_var)]:  #para cada producao de d0 verifica a posicao do marcador

                    posicao_marcador = producao_da_inicial.index(self.simbolo_marcador)

                    simbolo_direita_marcador = producao_da_inicial[posicao_marcador + 1]

                    if simbolo_direita_marcador == '/0':

                        self.palavras_reconhecidas.append(self.palavra)

                        self.palavra_reconhecida = True

                        self.status_aceitacao = 'Palavra reconhecida pela liguagem: No passo D' + str(len(self.conjunto_de_producoes_Dn)-1) + ' pala produção ' + ''.join(self.gramatica.initial_var) + ' -> ' + ''.join(producao_da_inicial)

                        #self.gera_arvore_derivacao(self.palavra)

                        return True

                self.status_aceitacao = 'Palavra não reconhecida pela liguagem: No passo D' + str(len(self.conjunto_de_producoes_Dn)-1) + ' nem uma produção de ' + ''.join(self.gramatica.initial_var) + ' esta com o marcador ' + self.simbolo_marcador + ' no fim da produção.'

        return False

    def complete(self): #se o marcador esta no final da gramatica (antes do /n), 'puxa' todas as produções do /n que tenham marcador antes de variavel, mas movendo o marcador para direita

        flag_producao_nova = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[-1])

        for variavel_dn, producoes_dn in producoes_DN.items():  # em todas as produções de dn

            for producao_dn in producoes_dn:

                if self.trigger_complete(producao_dn):

                    #cont_avancos = self.aux_complete_puxa_avanca_marcador(producao_dn)

                    cont_avancos = self.aux_complete_puxa_avanca_marcador(variavel_dn, producao_dn)

                    if cont_avancos > 0:  #todo ta muito feia essa logica aqui, da pra melhorar
                        flag_producao_nova = True

        return flag_producao_nova

    def scan(self, terminal_procurado,indice_dn):  # procura no D-index por alguma produção onde o terminal do lado direito do marcador, se sim cria D-index+1

        flag_encontrou = False

        producoes_DN = copy.deepcopy(self.conjunto_de_producoes_Dn[indice_dn])

        for variavel_dn, producoes_dn in producoes_DN.items():  # em todas as produções de dn

            for producao_dn in producoes_dn:  # busca todos os scans possiveis da variavel dn

                posicao_marcador = producao_dn.index(self.simbolo_marcador)

                terminal_scan = producao_dn[posicao_marcador + 1]

                if terminal_scan in self.gramatica.terminals and terminal_scan == terminal_procurado:  # verifica se apos o marcador tem um terminal e redundantemente se é a variavel que procuramos

                    producao_escaneada = copy.deepcopy(producao_dn)

                    producao_escaneada[posicao_marcador + 1], producao_escaneada[posicao_marcador] = producao_escaneada[posicao_marcador], producao_escaneada[posicao_marcador + 1]  # move marcador para direita

                    producao_escaneada[-1] = '\tscan terminal ' + terminal_procurado  # insere origem

                    if len(self.conjunto_de_producoes_Dn) - 1 == indice_dn:  # se o Dn não existe cria
                        self.conjunto_de_producoes_Dn.append({})

                    if variavel_dn in self.conjunto_de_producoes_Dn[-1].keys():  # se já tem produções dessa variavel adiciona nela
                        self.conjunto_de_producoes_Dn[-1][variavel_dn].append(producao_escaneada)
                    else:
                        self.conjunto_de_producoes_Dn[-1][variavel_dn] = []
                        self.conjunto_de_producoes_Dn[-1][variavel_dn].append(producao_escaneada)

                    flag_encontrou = True

        if not flag_encontrou:
            self.status_aceitacao = 'Scan falhou ao achar o terminal ' + terminal_procurado

        return flag_encontrou

    def combinacoes_palavras_possiveis(self, tamanho_entrada=0):

        if tamanho_entrada > 0:
            self.reconhecer_palavras_ate_tamanho = tamanho_entrada

        for tamanho_palavra in range(1, self.reconhecer_palavras_ate_tamanho):

            for combinacao in itertools.product(self.gramatica.terminals, repeat=tamanho_palavra):

                palavra_teste = []

                for term in combinacao:
                    palavra_teste.append(term)

                if combinacao == ('(', 'int', '+', 'int', ')'):
                    print("stop")

                resultado = self.verifica_palavra(palavra_teste)

                print(str(resultado) + str(combinacao) + ' Status = ' + self.status_aceitacao)

                if resultado:
                    pass
                    #self.palavras_reconhecidas.append(combinacao)

        return self.palavras_reconhecidas


    def valida_avanco_caracter(self, token, palavra):

        posicao_marcador = palavra.index(self.simbolo_marcador)

        direita_marcador = palavra[posicao_marcador + 1]

        if token == direita_marcador:
            palavra[posicao_marcador + 1], palavra[posicao_marcador] = palavra[posicao_marcador], palavra[posicao_marcador + 1]
            return True

        return False

    def arvore_testar_variavel(self, variavel):
        pass

    def arvore_testar_producao(self, producao):

        #chama Sn
        pass

    def gera_arvore_derivacao(self, palavra_entrada):

        tokens = []
        for var in self.gramatica.variables:
            tokens.append(var)
        for ter in self.gramatica.terminals:
            tokens.append(ter)

        for terminal in palavra_entrada:
            self.palavra_arvore.append(terminal)

        self.arvore.append(''.join(self.gramatica.initial_var))  # adiocina simbolo inicial na arvore

        self.valida_avanco_caracter(tokens[2], self.palavra_arvore)
        self.valida_avanco_caracter(tokens[1], self.palavra_arvore)

        #quando chega em um terminal executa a função valida_avanco_caracter

        self.NEXT = 0

        for pro in self.gramatica.rules[self.arvore[-1]]:
            temp_next = self.NEXT
            if self.arvore_testar_producao(pro):#cham recurção da variaveç
                arvore = True
            pass


        arvore_var = []

        arvore_var.append(''.join(self.gramatica.initial_var)) #adiocina simbolo inicial na arvore
        arvore_ter = []

        for index, caracter in enumerate(self.palavra): #para cada simbolo da palavra
            for terminais_var_inicial in self.gramatica.rules[arvore_var[index]]:  #para cada variavel da lista de variaveis da arvore
                    for terminal in terminais_var_inicial:
                        if terminal == caracter:  #se a produção contem o que procuramos
                            pass



        for terminais_iniciais_que_finalizaram in self.conjunto_de_producoes_Dn[-1][''.join(self.gramatica.initial_var)]:
            pass


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

        printFinal.append('Palavra de entrada:' + ''.join(palavra))

        printFinal.append(oParcer.status_aceitacao)

        printFinal.append(oParcer.to_str())


        printFinal.append(str(resultado))

    return '\n----------------------------------------------------------------------\n'.join(printFinal)

def debug():

    fileName = 'C:\\users\\vieir\\Documents\\GitHub\\TrabalhoPraticoINF05005\\Earley-teste_arvore.txt'

    with open(fileName) as f:
        lines = f.read()

    if lines:
        grammar = grammarClass.Grammar(lines)

        oParcer = EarleyParser(grammar)

        #resultado = oParcer.verifica_palavra(('id', '+', 'id', '+', 'id', 'id', '+', 'id'))

        #resultado = oParcer.verifica_palavra(('(', 'int', '+', 'int', ')'))
        #resultado = oParcer.verifica_palavra(('int',))
#
        print(oParcer.to_str())

        print(oParcer.status_aceitacao)
        reconhecer_palavras_ate = 7
        oParcer.combinacoes_palavras_possiveis(reconhecer_palavras_ate)

        print("As palavras reconhecidas pela gramatica com tamanho até " + str(reconhecer_palavras_ate) + " são::\n" + str(oParcer.palavras_reconhecidas))

#debug()