import grammarFunctions as gram
from easygui import *

exit_prog = 0

while exit_prog != 1:

    msg = "Escolha a opção desejada:"
    title = "Trabalho Final - Linguagens Formais e Automatos"
    choices = ['Simplificar Gramática', 'Earley Parser', 'Sair']
    choice = buttonbox(msg, title, choices)

    if choice == 'Simplificar Gramática':

        msg = "Abrir arquivo da gramatica:"
        choices = ['Escolher arquivo']
        choice = buttonbox(msg, title, choices)

        if choice == 'Escolher arquivo':
            fileName = fileopenbox("Nome do arquivo de gramática:", title, "*.txt")

        textbox("Resultado da simplificação da gramática", title, gram.getGrammar(fileName))

    elif choice == 'Earley Parser':
        msgbox('Ainda não tem, mas vai')

    elif choice == 'Sair':
        exit_prog = 1

exit()



