import copy
import re
import grammarClass


def simplifyAndChomsky(fileName):
    printFinal = []

    with open(fileName) as f:
        lines = f.read()

    if lines:

        grammar = grammarClass.Grammar(lines)
        printFinal.append('Gramática extraída do arquivo ' + fileName)
        printFinal.append(str(grammar))

        gramatica_simplificada = grammar.simplificar()
        printFinal.append("(1) Exclusão de Produções Vazias")
        printFinal.append("\n" + str(gramatica_simplificada))

        gramatica_simplificada.simplificacao_stp4_exclusao_prod_simples()
        printFinal.append("(2) Exclusão de Produções Simples")
        printFinal.append("\n" + str(gramatica_simplificada))

        gramatica_simplificada.simplificacao_stp5_exclusao_prod_inuteis()
        printFinal.append("(3) Exclusão de Produções Inuteis")
        printFinal.append("\n" + str(gramatica_simplificada))

        gramatica_chomsky = copy.deepcopy(gramatica_simplificada)

        temp = gramatica_chomsky.chomsky_stp1_separacao()


        if not isinstance(temp, str):
            printFinal.append("Forma normal de Chomsky - Tranformação de terminais")
            printFinal.append("\n" + str(gramatica_chomsky))

            gramatica_chomsky.chomsky_stp2_novas_variaveis()
            printFinal.append("Forma normal de Chomsky - Tranformação das produções de conjunto maior que 2")
            printFinal.append("\n" + str(gramatica_chomsky))

        else:
            printFinal.append(temp)

    return '\n----------------------------------------------------------------------\n'.join(printFinal)


def makeGrammarFile(terminais, variaveis, inicial, regras):
    textFile = open('GramaticaGerada.txt', 'w+')
    #lista de caracteres especiais
    LSpecialChar = [' ', '-', '>', ',', '.', '|', '=', '/']

    #separa strings caracter por caracter e deleta caracteres especiais
    LStringTerminais = list(terminais)
    Lterminais = []
    for i in range(len(LStringTerminais)):
        charFlag = 0
        for j in range(len(LSpecialChar)):
            if LStringTerminais[i] == LSpecialChar[j]:
                charFlag = 1
        if charFlag == 0:
            Lterminais.append(LStringTerminais[i])

    LStringVariaveis = list(variaveis)
    Lvariaveis = []
    for i in range(len(LStringVariaveis)):
        charFlag = 0
        for j in range(len(LSpecialChar)):
            if LStringVariaveis[i] == LSpecialChar[j]:
                charFlag = 1
        if charFlag == 0:
            Lvariaveis.append(LStringVariaveis[i])

    LStringInicial = list(inicial)
    Linicial = []
    for i in range(len(LStringInicial)):
        charFlag = 0
        for j in range(len(LSpecialChar)):
            if LStringInicial[i] == LSpecialChar[j]:
                charFlag = 1
        if charFlag == 0:
            Linicial.append(LStringInicial[i])

    LStringRegras = []
    for i in range(len(regras)):
        LStringRegras.append(list(regras[i]))
    Lregras = [[] for i in range(len(LStringRegras))]
    for i in range(len(LStringRegras)):
        for j in range(len(LStringRegras[i])):
            charFlag = 0
            for k in range(len(LSpecialChar)):
                if LStringRegras[i][j] == LSpecialChar[k]:
                    charFlag = 1
            if charFlag == 0:
                Lregras[i].append(LStringRegras[i][j])


    #salva no arquivo
    textFile.write('#Terminais\n')
    for i in range(len(Lterminais)):
        textFile.write('[ ' + Lterminais[i] + ' ]\n')

    textFile.write('#Variaveis\n')
    for i in range(len(Lvariaveis)):
        textFile.write('[ ' + Lvariaveis[i] + ' ]\n')

    textFile.write('#Inicial\n')
    textFile.write('[ ' + Linicial[0] + ' ]\n')

    textFile.write('#Regras')
    for i in range(len(Lregras)):
        textFile.write('\n')
        for j in range(len(Lregras[i])):
            if j == 0:
                textFile.write('[ ' + Lregras[i][j] + ' ] >')
            else:
                textFile.write(' [ ' + Lregras[i][j] + ' ]')


    textFile.close()


def takeStringFromFile(fileName):
    textFile = open(fileName, 'r')
    fileString = textFile.read()
    textFile.close()
    return fileString


def saveEditFile(fileName, fileString):
    fileArray = re.split(r'[.]', fileName)
    fileName = fileArray[0]
    fileName = fileName + '_edit'
    fileName = fileName + '.txt'
    textFile = open(fileName, 'w+')
    textFile.write(fileString)
    textFile.close()
    return fileName

