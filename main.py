from time import sleep

import pymongo
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client.ac1
users = db.users

## ↓ adiciona os três usuários padrão para operações básicas ↓
usuarios_inicias = [
    {"user": "admin", "password": "123", "ac": '1'},
    {"user": "usuario1", "password": "senha1"},
    {"user": "usuario2", "password": "442"}
]

def verif_dupl(user, password,ac=''):
    # ↓ aqui ele verifica se o user já existe na coleção e, se sim, retorna o código
    if users.find_one({'user': user}):
        return -1
    else:
        users.insert_one({"user": user, "password": password, "ac" : ac})
        return None

for usuario in usuarios_inicias:
    # ↓ aqui ele chama a função pra verificar se os usuários iniciais já existem
    if usuario.get('ac'):
        verif_dupl(usuario['user'], usuario['password'], usuario['ac'])
        continue
    verif_dupl(usuario['user'], usuario['password'], '')



def cadastro():
    user = str(input("Insira nome de usuário: "))
    password = str(input("insira senha: "))
    confirmpass = input('Confirme a senha: ')
    if password == confirmpass:
        resultado = verif_dupl(user, password)
        if resultado:
            print("Usuário já existe. Tente novamente")
            cadastro()
        else:
            print ("Usuário cadastrado com sucesso!")
    else:
        print('Senha diferente')

def logar():
    tentativas = 0
    while tentativas < 3:
        userLogIn = input('Insira seu usuário: ')
        passwordLogIn = input('Insira senha: ')

        ## menu do adm
        if userLogIn == 'admin' and passwordLogIn == '123':
            print("Login realizado com sucesso!")
            while True:
                print("-" * 10, " Menu do administrador ", ("-" * 10))
                print("1.Ver Perfil")
                print("2.Criar usuário")
                print("3.Sair")
                print("4.Remover usuário")
                print("5.Ver todos os usuários cadastrados")
                op = int(input("Escolha: "))

                if op == 1:
                    print("Perfil:", userLogIn)
                elif op == 2:
                    cadastro()
                elif op == 3:
                    return
                elif op == 4:
                    userDelete = input("Digite o nome do usuário que deseja excluir: ")
                    if userDelete == 'admin':
                        print("Usuário chave para o funcionamento do banco, exclusão cancelada.")
                    elif db.users.find_one({"user": userDelete}):
                        users.delete_one({"user": userDelete})
                        print("Usuário deletado com sucesso.")
                    else:
                        print("Usuário não encontrado.")
                elif op == 5:
                    for user in db.users.find():
                        print(user)
                else:
                    print("Escolha entre as opções disponíveis")


        elif db.users.find_one({"user": userLogIn, "password": passwordLogIn}):
            print("Login realizado com sucesso!")
            ## menu normal
            while True:
                print("-" * 10, " Menu ", ("-" * 10))
                print("1.Ver Perfil")
                print("2.Criar usuário")
                print("3.Sair")
                print("4.Deletar minha conta")
                op = int(input("Escolha: "))

                if op == 1:
                    print("Perfil:", userLogIn)
                elif op == 2:
                    cadastro()
                elif op == 3:
                    return
                elif op == 4:
                    confirm = input("Digite seu usuário para confirmar a exclusão: ")
                    if confirm == userLogIn:
                        users.delete_one({"user": confirm})
                        print("Usuário excluído com sucesso.")
                        return
                    else:
                        print("Exclusão cancelada.")
                else:
                    print("Escolha entre as opções disponíveis")
        elif db.users.find_one({"user": userLogIn, "password": {"$ne": passwordLogIn}}):
            tentativas += 1
            print("Senha inválida")
        else:
            tentativas += 1
            print("Usuário não encontrado")
    ## aqui ele ta saindo do loop while, o que significa que a variavel 'tentativas' passou de 3
    print("Número máximo de tentativas excedido. Acesso bloqueado")
    i = 10
    while i > 0:
        print(f"Timeout {i} segundos")
        sleep(1)
        i -= 1
    return


def menu():
    print('-' * 10, 'Menu', '-' * 10)
    ch = int(input('Escolha uma opção \n 1. Logar \n 2. Cadastrar \n 3. Encerrar \n 4. Resetar banco (EXCLUI TODOS OS REGISTROS DO BANCO DE DADOS)\n'))
    if ch == 1:
        logar()
    elif ch == 2:
        cadastro()
    elif ch == 3:
        exit()
    elif ch == 4:
        db.users.delete_many({'user': {"$ne": "admin"}})
        menu()
    else:
        print('Escolha uma opção válida')
        return
menu()