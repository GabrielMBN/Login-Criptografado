# Imports

import os
from cryptography.fernet import Fernet

# Padrões

option = None
name = None
granted = False
key = None
defaultPass = 'admin'
encDefaultPass = None
fernet = None

# Verificando se há necessidade/criando txt com user details e key

if not os.path.isfile('user_details.csv'):
    key = Fernet.generate_key()
    with open('filekey.key', 'w+') as filekey:
        filekey.write(key.decode())
    fernet = Fernet(key)
    encDefaultPass = fernet.encrypt(bytes(defaultPass, "utf-8"))
    user_details = open('user_details.csv', 'w+')
    user_details.write('admin,' + encDefaultPass.decode() + "\n")
    user_details.close()
else:
    with open('filekey.key', 'r') as filekey:
        key = filekey.read()
    fernet = Fernet(key.encode())
    encDefaultPass = defaultPass

# Login/registro garantido
    
def grant():
    global granted
    granted = True

# Efetuando login

def login(name, encPassword):
    global encDefaultPass
    global fernet
    success = False
    user_details = open('user_details.csv', 'r')
    for i in user_details:
        a, b = i.split(',')
        b = b.strip()
        if a == name:
            if fernet.decrypt(b.encode()).decode() == encPassword or encPassword == encDefaultPass:
                success = True
                break

    user_details.close()
    if success:
        print('Logado com sucesso!')
        grant()
    elif option == 'log':
        print('Nome de usuário ou senha errados!')
        print('----------------------------------------')
        name = None
        password = None
        access(option)
    else:
        print('Erro no login.')

# Efetuando registro
        
def register(name, password):
    encPassword = fernet.encrypt(bytes(password, "utf-8"))
    with open('user_details.csv', 'a') as fileuser:
        fileuser.write(name + "," + encPassword.decode() + "\n")
    fileuser.close()
    print('Registrado com sucesso!')
    print('----------------------------------------')
    login(name, password)

# Inputs de dados

def access(option):
    global name
    if option == 'log':
        name = input('Digite seu nome de usuário: ')
        print('----------------------------------------')
        password = input('Digite sua senha: ')
        print('----------------------------------------')
        login(name, password)
    else:
        reg_pass = input("Insira a chave para registro: ")
        if reg_pass != defaultPass:
            print("Chave de registro incorreta")
            return
        print('Digite seu nome e senha para registrar')
        print('----------------------------------------')
        name = input('Digite seu nome de usuário: ')
        print('----------------------------------------')
        password = input('Digite sua senha: ')
        print('----------------------------------------')
        register(name, password)

# Inicio

def begin():
    global option
    print('----------------------------------------')
    print('Bem vindo ao login')
    print('----------------------------------------')
    option = input('Logar ou registrar (log,reg): ')
    print('----------------------------------------')
    if option != 'log' and option != 'reg':
        begin()


begin()
access(option)
if granted:
    print('|--------------------------------------|')
    print('|  @@ Bem vindo ao teste de login  @@  |')
    print('|                                      |')
    print('|      vv DETALHES DE USUÁRIO: vv      |')
    print('|______________________________________|')
    print('     >> Nome de usuario: ', name, ' <<')
    print('')
