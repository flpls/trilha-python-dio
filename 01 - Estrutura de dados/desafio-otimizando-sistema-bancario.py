import re 

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[n] Novo Usuário
[a] Abertura de Conta

=> """

# Variáveis globais
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Função para depósito
def depositar(saldo, extrato):
    valor = float(input("Informe valor de depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito no valor de {valor:.2f} realizado\n")
    else:
        print("Operação falhou: O valor informado é inválido")
    
    return saldo, extrato

# Função para saque
def sacar(saldo, extrato, numero_saques, limite):
    valor = float(input("Informe valor de saque: "))

    if numero_saques == LIMITE_SAQUES:
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

# Função para exibir extrato
def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("================================")

# Função para criar um novo usuário
#TODO: Implementar registro de novos usuários com CPF válido
def criar_usuario(usuarios):
    cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF: "))
    soma_cpf = sum(int(char) for char in cpf)
    if soma_cpf % 11:
        # Verifica se o CPF já está cadastrado
        usuario_existente = any(usuario['cpf'] == cpf for usuario in usuarios)
        
        if usuario_existente:
            print("Já existe um usuário com esse CPF.")
            return
        
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (logradouro, número - bairro - cidade/estado): ")
        
        # Adiciona o novo usuário à lista de usuários
        usuario.append({
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "endereco": endereco
        })
        
        print(f"Usuário {nome} criado com sucesso!\n")
    else:
        print("CPF inválido.")

#TODO: Implementar vinculação de contas com CPF de usuário. 
# Função para criar uma nova conta corrente vinculada a um usuário
def criar_conta_corrente(usuarios, contas, numero_conta):
    cpf = input("Informe o CPF do usuário: ")
    
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

#TODO: Implementar chamadas de funções de criar usuário e criar conta.
# Função principal para controle do menu
def main():
    global saldo, extrato, numero_saques, limite
    
    while True:
        opcao = input(menu).lower()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, limite)
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "q":
            if sair():
                break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Executa o programa
main()
