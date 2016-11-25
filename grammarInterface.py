import grammarFunctions as gram
from easygui import *

exit_prog = 0

while exit_prog != 1:

    msg = "Escolha a opção desejada:"
    title = "Trabalho Final - Linguagens Formais e Automatos"
    choices = ['Escolher arquivo', 'Fazer gramática', 'Sair']
    choice = buttonbox(msg, title, choices)

    if choice == 'Escolher arquivo':
        fileName = fileopenbox("Nome do arquivo de gramática:", title, "*.txt")

        msg = "Escolha a opção desejada:"
        choices = ['Simplificar gramática', 'Early', 'Voltar', 'Sair']
        choice = buttonbox(msg, title, choices)

        while choice != 'Voltar':
            if choice == 'Simplificar gramática':
                textbox("Resultado da simplificação da gramática", title, gram.simplifyAndChomsky(fileName))
                choice = 'Voltar'

            elif choice == 'Early Parser':
                msgbox('Ainda não tem, mas vai')

            elif choice == 'Sair':
                exit_prog = 1


    elif choice == 'Fazer gramática':
        terminais = enterbox('Insira os terminais', title, strip=False)
        variaveis = enterbox('Insira as variáveis', title)
        inicial = enterbox('Insira a variável inicial', title)
        choices = ['Proxima', 'Acabou']
        regras = []

        while choice != 'Acabou':
            choice = buttonbox('Insira as regras da gramática', title, choices)
            if choice == 'Proxima':
                regras.append(enterbox('Insira uma regra', title))
        gram.makeGrammarFile(terminais, variaveis, inicial, regras)

        choices = ['Simplificar gramática', 'Early', 'Voltar', 'Sair']
        choice = buttonbox(msg, title, choices)
        while choice != 'Voltar':
            if choice == 'Simplificar gramática':
                textbox("Resultado da simplificação da gramática", title,
                        gram.simplifyAndChomsky('GramaticaGerada.txt'))
                choice = 'Voltar'

            elif choice == 'Early Parser':
                msgbox('Ainda não tem, mas vai')

            elif choice == 'Sair':
                exit_prog = 1


    elif choice == 'Sair':
        exit_prog = 1

exit()
