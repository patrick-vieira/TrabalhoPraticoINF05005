
class Grammar:  # Grammar: salva variaveis, terminais e regras
    def __init__(self):
        self.terminals = []
        self.variables = []
        self.initial_var = []
        self.rules = {}  # rules: um dicionario que mantem todas as regras salvas usando as variaveis como indice
        self.empty_word = {}
        self.useless_symbol = {}
        self.excepts_empty = 0
        self.has_empty = 0

