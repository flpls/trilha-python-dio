menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe valor de depósito: "))

        #Mensagem de confirmação de operação realizada acrescentada. 
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito no valor de {valor:.2f} realizado\n")
        
        else:
            print("Operação falhou: O valor informado é inválido")

    elif opcao == "s":
        valor = float(input("Informe valor de saque: "))
        
        #Diferentemente da resolução optei por declarar as condições individualmente pela legibilidade.
        
        #A condição de limites de saques sendo declarada primeiro reduz possibilidade de falha, impedindo que o usuário chegue a declarar valor de saque quando limite já foi alcançado. 
        if numero_saques == 3:
            print("Operação falhou! O limite diário de saques foi alcançado.")
        
        elif valor > saldo:
            print("Operação falhou! Seu saldo não é suficiente.")
        
        elif valor > limite: 
            print("Operação falhou! O valor excede o limite de saques.")

        #Mensagem de confirmação de operação realizada acrescentada.               
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Saque no valor de {valor:.2f} realizado\n")
        
        else:
            print("Operação falhou: O valor informado é inválido")

    elif opcao == "e":
       print("\n================ EXTRATO ================")
       print("Não foram realizadas movimentações." if not extrato else extrato)
       print(f"\nSaldo: R$ {saldo:.2f}")
       print("================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

