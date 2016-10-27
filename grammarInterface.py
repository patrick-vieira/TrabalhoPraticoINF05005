import grammarFunctions as gram
from easygui import *

msg = "Escolha a opção desejada:"
title = "Trabalho Final - Linguagens Formais e Automatos"
choices = ['Simplificar Gramática', 'Earley Parser']
choice = buttonbox(msg, title, choices)

if choice == 'Simplificar Gramática':
    fileName = fileopenbox("Nome do arquivo de gramática:", title, "*.txt")
    textbox("Resultado da simplificação da gramática", title, gram.getGrammar(fileName))
elif choice == 'Earley Parser':
    msgbox('Ainda não tem, mas vai')


