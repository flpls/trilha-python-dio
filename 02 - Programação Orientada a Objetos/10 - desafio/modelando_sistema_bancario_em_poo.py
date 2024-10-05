import re

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[n] Novo Usuário
[a] Abertura de Conta

=> """


class Transacao:
    def registrar(self):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso!")


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso!")


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, numero, agencia, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        else:
            print("Saldo insuficiente para saque.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        else:
            print("Valor de depósito inválido.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite, limite_saques):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False
        elif valor > self.limite:
            print("Valor excede o limite de saque.")
            return False
        elif super().sacar(valor):
            self.numero_saques += 1
            return True
        else:
            return False


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF: "))  # Limpeza de caracteres.

    if not cpf.isdigit():  # Confirmação que o CPF contém apenas números
        print("CPF inválido. Deve conter apenas números.")
        return

    # Verifica se o CPF já está cadastrado
    if any(u.cpf == cpf for u in usuarios):
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/estado): ")

    # Criação do objeto PessoaFisica e adição à lista de usuários
    novo_cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    usuarios.append(novo_cliente)

    print(f"Usuário {nome} criado com sucesso!\n")


# Função para criar uma conta corrente
def criar_conta_corrente(usuarios, contas, numero_conta):
    cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF do usuário: "))

    # Verifica se o usuário com o CPF informado existe
    usuario = next((u for u in usuarios if u.cpf == cpf), None)

    if not usuario:
        print("Usuário não encontrado. Certifique-se de que o CPF está correto ou cadastre o usuário primeiro.")
        return

    # Cria a conta vinculada ao usuário
    nova_conta = ContaCorrente(numero_conta, "0001", usuario, limite=500, limite_saques=3)
    usuario.adicionar_conta(nova_conta)
    contas.append(nova_conta)

    print(f"Conta número {numero_conta} criada com sucesso para o usuário {usuario.nome}.\n")

    return numero_conta + 1


# Função para exibir o extrato da conta
def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            tipo = "Depósito" if isinstance(transacao, Deposito) else "Saque"
            print(f"{tipo}: R$ {transacao.valor:.2f}")
    print(f"\nSaldo: R$ {conta.saldo_atual():.2f}")
    print("================================")


# Função para sair
def sair():
    print("Saindo do sistema...")
    return True


# Função principal para controle do menu
def main():
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = input(menu).lower()

        if opcao == "d":
            cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF do usuário: "))
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if not usuario:
                print("Usuário não encontrado.")
                continue

            if not usuario.contas:
                print("Usuário não tem nenhuma conta cadastrada.")
                continue

            conta = usuario.contas[0]  # Considerando apenas a primeira conta
            valor = float(input("Informe valor de depósito: "))
            Deposito(valor).registrar(conta)

        elif opcao == "s":
            cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF do usuário: "))
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if not usuario:
                print("Usuário não encontrado.")
                continue

            if not usuario.contas:
                print("Usuário não tem nenhuma conta cadastrada.")
                continue

            conta = usuario.contas[0]  # Considerando apenas a primeira conta
            valor = float(input("Informe o valor de saque: "))
            Saque(valor).registrar(conta)

        elif opcao == "e":
            cpf = re.sub(r'[.\-\s]', '', input("Informe o CPF do usuário: "))
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if not usuario:
                print("Usuário não encontrado.")
                continue

            if not usuario.contas:
                print("Usuário não tem nenhuma conta cadastrada.")
                continue

            conta = usuario.contas[0]  # Considerando apenas a primeira conta
            exibir_extrato(conta)

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
