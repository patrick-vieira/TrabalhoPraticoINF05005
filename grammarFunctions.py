import grammarClass as gm

def simplifyAndChomsky(fileName):

    grammar = gm.Grammar
    printFinal = []

    with open(fileName) as f:
        lines = f.read()

    if lines:
        grammar.getGrammar(lines)
        printFinal.append(grammar.printGrammar('Gramática extraída do arquivo ' + fileName))
        if grammar.has_empty:
            grammar.goToV()
            grammar.changeGrammar()
            grammar.cleanV()

            printFinal.append("\n" + grammar.printGrammar("(1) Exclusão de Produções Vazias"))

            print("\n\n\n")
            print("Terminais: %s" % grammar.terminals)
            print("Variaveis: %s" % grammar.variables)
            print("Simbolo inicial: %s" % grammar.initial_var)
            print("Regras: ")
            for var, ter in grammar.rules.items():
                print("%s -> %s" % (var, ter))
            print("\n\n\n")

        else:
            printFinal.append("(1) Exclusão de Produções Vazias \n\n Não existem produções vazias na gramatica")

        grammar.varClosure()

        printFinal.append("\n" + grammar.printGrammar("(2) Exclusão de Produções Simples"))

        print("\n\n\n")
        print("Terminais: %s" % grammar.terminals)
        print("Variaveis: %s" % grammar.variables)
        print("Simbolo inicial: %s" % grammar.initial_var)
        print("Regras: ")
        for var, ter in grammar.rules.items():
            print("%s -> %s" % (var, ter))
        print("\n\n\n")

        grammar.uslessSymbol()

        printFinal.append("\n" + grammar.printGrammar("(3) Exclusão de Produções Inuteis"))

        print("\n\n\n")
        print("Terminais: %s" % grammar.terminals)
        print("Variaveis: %s" % grammar.variables)
        print("Simbolo inicial: %s" % grammar.initial_var)
        print("Regras: ")
        for var, ter in grammar.rules.items():
            print("%s -> %s" % (var, ter))
        print("\n\n\n")

        if not grammar.accepts_empty:
            grammar.chomsky()

            print("\n\n\n")
            print("Terminais: %s" % grammar.terminals)
            print("Variaveis: %s" % grammar.variables)
            print("Simbolo inicial: %s" % grammar.initial_var)
            print("Regras: ")
            for var, ter in grammar.rules.items():
                print("%s -> %s" % (var, ter))
            print("\n\n\n")

            printFinal.append("\n" + grammar.printGrammar("Forma normal de Chomsky - Tranformação de terminais"))

            grammar.chomskyPart2()

            printFinal.append("\n" + grammar.printGrammar("Forma normal de Chomsky - Tranformação das produções de conjunto maior que 2"))

        else:
            printFinal.append("Forma normal de Chomsky \n\n A gramática aceita palavra vazia.")


        grammar.clean()

    return'\n----------------------------------------------------------------------\n'.join(printFinal)


