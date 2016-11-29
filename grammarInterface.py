import grammarFunctions as gram
import grammarEarleyParser
from easygui import *

exit_prog = 0
title = "Trabalho Final - Linguagens Formais e Automatos"
msg = "Trabalho Final - Linguagens Formais e Automatos\nConstruído por:\nLucas da Silva Flores (242317)\nMaicon da Cunha Vieira (242275)\nPatrick Dornelles da Silva Vieira (242320)\nVinicius Costa Barbosa dos Santos (242283)"
choices = ["Continuar", "Sair"]
choice = buttonbox(msg, image="teletubbies.png", choices=choices)
if choice == "Continuar":
    while exit_prog != 1:

        msg = "Escolha a opção desejada:"
        title = "Trabalho Final - Linguagens Formais e Automatos"
        choices = ['Escolher arquivo', 'Fazer gramática', 'Sair']

        choice = buttonbox(msg, title, choices)

        if choice == 'Escolher arquivo':
            fileName = fileopenbox("Nome do arquivo de gramática:", title, "*.txt")

            if fileName:
                msg = "Escolha a opção desejada:"
                choices = ['Simplificar gramática', 'Early Parser', 'Editar', 'Voltar']
                while choice != 'Voltar':
                    choice = buttonbox(msg, title, choices)


                    if choice == 'Simplificar gramática':
                        textbox("Resultado da simplificação da gramática", title, gram.simplifyAndChomsky(fileName))
                        choice = 'Voltar'


                    elif choice == 'Early Parser':

                        op = buttonbox("Escolha uma opção:", title, ["Verificar palavra", "Palavras aceitas até tamanho dado"])

                        if op == "Verificar palavra":

                            outra_palavra = 1

                            while outra_palavra:

                                palavra2 = enterbox('Insira uma palavra para reconhecimento:', title)
                                if palavra2:
                                    textbox("Early Parser", title, grammarEarleyParser.earlyParser(fileName, palavra2))

                                choice = buttonbox("Deseja testar outras palavras nesta mesma gramática?", title,
                                                   ["Outra palavra", "Voltar"])

                                if choice != "Outra palavra":
                                    choice = 'Voltar'

                                    outra_palavra = 0

                        elif op == "Palavras aceitas até tamanho dado":

                            outro_tamanho = 1

                            while outro_tamanho:

                                tamanho = enterbox('Insira o tamanho maximo das palavras:', title)
                                if tamanho:
                                    textbox("Palavras aceitas pela gramática:", title, grammarEarleyParser.combinacoes(fileName, tamanho))

                                choice = buttonbox("Deseja testar outros tamanhos nesta mesma gramática?", title,
                                                   ["Outro tamanho", "Voltar"])

                                if choice != "Outro tamanho":
                                    choice = 'Voltar'

                                    outro_tamanho = 0



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

                    op = buttonbox("Escolha uma opção:", title, ["Verificar palavra", "Palavras aceitas até tamanho dado"])

                    if op == "Verificar palavra":

                        outra_palavra = 1

                        while outra_palavra:

                            palavra2 = enterbox('Insira uma palavra para reconhecimento:', title)

                            if palavra2:
                                textbox("Early Parser", title, grammarEarleyParser.earlyParser(localFile, palavra2))

                            choice = buttonbox("Deseja testar outras palavras nesta mesma gramática?", title,

                                               ["Outra palavra", "Voltar"])

                            if choice != "Outra palavra":
                                choice = 'Voltar'

                                outra_palavra = 0


                    elif op == "Palavras aceitas até tamanho dado":

                        outro_tamanho = 1

                        while outro_tamanho:

                            tamanho = enterbox('Insira o tamanho maximo das palavras:', title)

                            if tamanho:
                                textbox("Palavras aceitas pela gramática:", title,
                                        grammarEarleyParser.combinacoes(localFile, tamanho))

                            choice = buttonbox("Deseja testar outros tamanhos nesta mesma gramática?", title,

                                               ["Outro tamanho", "Voltar"])

                            if choice != "Outro tamanho":
                                choice = 'Voltar'

                                outro_tamanho = 0


                elif choice == 'Editar':
                    fileString = textbox("Edite o arquivo:", title, gram.takeStringFromFile(localFile))
                    localFile = gram.saveEditFile(localFile, fileString)


        elif choice == 'Sair':
            exit_prog = 1


msg = "Muito obrigado"
choices = ["Sair"]
choice = buttonbox(msg, image="denniszord.png", choices=choices)

exit()
