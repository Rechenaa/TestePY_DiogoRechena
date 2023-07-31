import random

class contas:
    def __init__(self, nome, idade):
        self.nome = nome
        self.numeroConta = random.randint(10000000000, 99999999999)
        self.idade = idade
        self.dinheiro = 0
        file_object = open("infi_banco.txt", 'a')
        file_object.write(self.nome + " " + str(self.numeroConta) + " " + str(self.idade) + " " + str(self.dinheiro) + '\n')
        file_object.close()