import grammarFunctions as gram
from easygui import *

msg = "Escolha a opcao desejada"
title = "Trabalho Final - Linguagens Formais e Automatos"
choices = ['Simplificar Gramatica', 'Earley Parser']
choice = buttonbox(msg, title, choices)

if choice == 'Simplificar Gramatica':
    fileName = enterbox("Nome do arquivo de gramatica:", title)
    textbox(gram.getGrammar(fileName), title)
elif choice == 'Earley Parser':
    msgbox('Ainda não tem, mas vai')


