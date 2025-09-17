import pymongo
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client.ac1
users = db.users

## ↓ adiciona os três usuários padrão para operações básicas ↓
usuarios_inicias = [
    {"user": "admin", "password": "123"},
    {"user": "usuario1", "password": "senha1"},
    {"user": "usuario2-", "password": "442"}
]

def verif_dupl(user, password):
    # ↓ aqui ele verifica se o user já existe na coleção e, se sim, retorna o código
    if users.find_one({'user': user}):
        return -1
    else:
        users.insert_one({"user": user, "password": password})
        return None

for usuario in usuarios_inicias:
    # ↓ aqui ele chama a função pra verificar se os usuários iniciais já existem
    verif_dupl(usuario['user'], usuario['password'])

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
    userLogIn = input('Insira seu usuário: ')
    passwordLogIn = input('Insira senha: ')
    tentativas = 0
    ## ↓ aqui ele verifica se o user  e a senha que a pessoa colocou batem ↓
    login = (db.users.find_one({"user": userLogIn, "password": passwordLogIn}))
    print (login)
    while tentativas < 3:
        ''' 
           verifica se o usuário é o administrador em específico, isso só é possível por conta
         ↓ da função verif_dupl() que impede a ocorrência de duplicatas ↓
        '''
        if db.users.find_one({"user":"admin", "password":"123"}):
            while True:
                ## ↓ menuzin do adm ↓
                print("-" * 10, " Menu do administrador ", ("-" * 10))
                print("1.Ver Perfil")
                print("2.Criar usuário")
                print("3.Sair")
                print("4.Remover usuário")
                print("5.Ver todos os usuários cadastrados")
                op = int(input(""))
                if op == 1:
                    print(userLogIn)
                elif op == 2:
                    cadastro()
                elif op == 3:
                    ## ↓ seta tentativas pra 4 para que o código volte para antes do while e saia do loop ↓
                    tentativas = 4
                    break
                elif op == 4:
                    userDelete = input("Digite o nome do usuário que deseja excluir do banco: ")
                    users.delete_one({"user": userDelete})
                elif op == 5:
                    for user in (db.users.find()):
                        print(user)
                else:
                    print("Escolha entre as opções disponíveis")
        elif db.users.find_one({"user": userLogIn, "password": passwordLogIn}):
            print("Login realizado com sucesso!")
            ## ↓ menuzinho pós login ↓
            while True:
                print("-" * 10, " Menu ", ("-" * 10))
                print("1.Ver Perfil")
                print("2.Criar usuário")
                print("3.Sair")
                op = int(input(""))
                if op == 1:
                    print(userLogIn)
                elif op == 2:
                    cadastro()
                elif op == 3:
                    tentativas = 4
                    break
                else:
                    print("Escolha entre as opções disponíveis")
        ## verifica se a senha para o user especificado está correta ($ne = not equal)
        elif db.users.find_one({"user":userLogIn, "password":{"$ne": passwordLogIn}}):
            tentativas += 1
            print ('Senha inválida')
            return
        else:
            tentativas += 1
            print ('Usuário não encontrado')
            return
print('-'*10, 'Menu', '-'*10)

def menu():
    ch = int(input('Escolha uma opção \n 1. Logar \n 2. Cadastrar \n 3. Encerrar'))
    if ch == 1:
        logar()
    elif ch == 2:
        cadastro()
    elif ch == 3:
        exit()
    else:
        print('Escolha uma opção válida')
        return
menu()