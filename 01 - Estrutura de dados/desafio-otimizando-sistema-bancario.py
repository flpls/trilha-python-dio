import re 

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[n] Novo Usuário
[a] Abertura de Conta

=> """

# Variáveis globais.
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"
usuarios = []
contas = []
numero_conta = 1

# Função para depósito (positional only).
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito no valor de {valor:.2f} realizado\n")
    else:
        print("Operação falhou: O valor informado é inválido")
    
    return saldo, extrato

# Função para saque (keyword only).
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques == limite_saques:
        print("Operação falhou! O limite diário de saques foi alcançado.")
    elif valor > saldo:
        print("Operação falhou! Seu saldo não é suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor excede o limite de saques.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque no valor de {valor:.2f} realizado\n")
    else:
        print("Operação falhou: O valor informado é inválido")
    
    return saldo, extrato, numero_saques


# Função para exibir extrato (positional only e keyword only).
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("================================")

#Função para criar usuário.
def criar_usuario(usuarios):
    cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF: ")) # Limpeza de caracteres.
    
    if not cpf.isdigit(): #Confirmação que input contém apenas números
        print("CPF inválido. Deve conter apenas números.")
    
        # Verifica se o CPF já está cadastrado
    usuario_existente = any(usuario['cpf'] == cpf for usuario in usuarios)
    
    if usuario_existente:
        print("Já existe um usuário com esse CPF.")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/estado): ")
    
    # Adiciona o novo usuário à lista de usuários.
    usuarios.append({
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })
    
    print(f"Usuário {nome} criado com sucesso!\n")
    

# Função para criar uma conta corrente.
def criar_conta_corrente(usuarios, contas, numero_conta):
    cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF do usuário: "))
    
    # Verifica se o usuário com o CPF informado existe
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)
    
    if not usuario:
        print("Usuário não encontrado. Certifique-se de que o CPF está correto ou cadastre o usuário primeiro.")
        return
    
    # Cria a conta vinculada ao usuário
    contas.append({
        "numero_conta": numero_conta,
        "agencia": "0001",  # Padrão fixo de agência
        "cpf_usuario": cpf
    })
    
    print(f"Conta número {numero_conta} criada com sucesso para o usuário {usuario['nome']}.\n")
    
    return numero_conta + 1

# Função para sair
def sair():
    print("Saindo do sistema...")
    return True

# Função principal para controle do menu Implementa chamadas de funções de criar usuário e criar conta.
def main():
    global saldo, extrato, numero_saques, limite, numero_conta, numero_saques, contas
    
    while True:
        opcao = input(menu).lower()

        if opcao == "d":
            valor = float(input("Informe valor de depósito: "))  # Solicita o valor do depósito fora da função
            saldo, extrato = depositar(saldo, valor, extrato)  # Agora passa o valor como argumento
        elif opcao == "s":
            valor = float(input("Informe o valor de saque: "))  # Solicita o valor do saque fora da função
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES
            )
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "n":
            criar_usuario(usuarios)
        elif opcao == "a":
            numero_conta = criar_conta_corrente(usuarios, contas, numero_conta)
        elif opcao == "q":
            if sair():
                break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Função main.
main()

