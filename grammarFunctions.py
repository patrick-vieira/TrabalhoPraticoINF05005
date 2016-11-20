import copy

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
