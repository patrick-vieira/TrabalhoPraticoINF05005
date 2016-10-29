
class Grammar:  # Grammar: salva variaveis, terminais e regras
    terminals = []
    variables = []
    initial_var = []
    rules = {}  # rules: um dicionario que mantem todas as regras salvas usando as variaveis como indice
    empty_word = {}
    useless_symbol = {}
    excepts_empty = 0
    has_empty = 0