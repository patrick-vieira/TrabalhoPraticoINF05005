import grammarFunctions as gram
import grammarEarleyParser
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
        choices = ['Simplificar gramática', 'Early Parser', 'Editar', 'Voltar']
        while choice != 'Voltar':
            choice = buttonbox(msg, title, choices)


            if choice == 'Simplificar gramática':
                textbox("Resultado da simplificação da gramática", title, gram.simplifyAndChomsky(fileName))
                choice = 'Voltar'

            elif choice == 'Early Parser':
                palavra = enterbox('Insira uma palavra para reconhecimento:', title)
                textbox("Early Parser", title, grammarEarleyParser.earlyParser(fileName, palavra))
                choice = 'Voltar'

            elif choice == 'Editar':
                fileString = textbox("Edite o arquivo:", title, gram.takeStringFromFile(fileName))
                fileName = gram.saveEditFile(fileName, fileString)



    elif choice == 'Fazer gramática':
        terminais = enterbox('Insira os terminais', title)
        variaveis = enterbox('Insira as variáveis', title)
        inicial = enterbox('Insira a variável inicial', title)
        choices = ['Proxima', 'Acabou']
        regras = []
        localFile = 'GramaticaGerada.txt'

        while choice != 'Acabou':
            choice = buttonbox('Insira as regras da gramática', title, choices)
            if choice == 'Proxima':
                regras.append(enterbox('Insira uma regra', title))
        gram.makeGrammarFile(terminais, variaveis, inicial, regras)

        choices = ['Simplificar gramática', 'Early Parser', 'Editar', 'Voltar']

        while choice != 'Voltar':
            choice = buttonbox(msg, title, choices)

            if choice == 'Simplificar gramática':
                textbox("Resultado da simplificação da gramática", title,
                        gram.simplifyAndChomsky(localFile))
                choice = 'Voltar'

            elif choice == 'Early Parser':
                palavra2 = enterbox('Insira uma palavra para reconhecimento:', title)
                textbox("Early Parser", title, grammarEarleyParser.earlyParser(localFile, palavra2))
                choice = 'Voltar'

            elif choice == 'Editar':
                fileString = textbox("Edite o arquivo:", title, gram.takeStringFromFile(localFile))
                localFile = gram.saveEditFile(localFile, fileString)


    elif choice == 'Sair':
        exit_prog = 1

exit()
