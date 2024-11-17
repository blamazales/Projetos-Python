from datetime import datetime

# Dados globais
usuarios = []
contas = []
valor_conta = 0
depositos = []
extrato = []
saques_diarios = 0
transacoes_diarias = 0
LIMITE_TRANSACOES = 10
AGENCIA_PADRAO = "0001"
numero_conta_sequencial = 1

# Função para cadastrar um usuário
def cadastrar_usuario(nome, cpf, endereco):
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove qualquer caractere não numérico do CPF
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print("Usuário já cadastrado com este CPF.")
            return
    usuarios.append({'nome': nome, 'cpf': cpf, 'endereco': endereco})
    print(f"Usuário {nome} cadastrado com sucesso.")

def buscar_usuario_por_cpf(cpf):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    print("Usuário não encontrado.")
    return None

def criar_conta(cpf):
    global numero_conta_sequencial
    usuario = buscar_usuario_por_cpf(cpf)
    if not usuario:
        return
    conta = {'agencia': AGENCIA_PADRAO, 'numero': numero_conta_sequencial, 'cpf': cpf}
    contas.append(conta)
    numero_conta_sequencial += 1
    print(f"Conta criada com sucesso! Agência: {conta['agencia']}, Número: {conta['numero']}")

def listar_contas_do_usuario(cpf):
    contas_usuario = [conta for conta in contas if conta['cpf'] == cpf]
    if not contas_usuario:
        print("Nenhuma conta encontrada para este usuário.")
    else:
        print(f"Contas do usuário com CPF {cpf}:")
        for conta in contas_usuario:
            print(f"Agência: {conta['agencia']}, Número: {conta['numero']}")

# Funções para gerenciamento de transações bancárias
def exibir_menu_conta(conta):
    print("\nMenu da Conta Bancária:")
    print(f"Conta em uso: Agência {conta['agencia']}, Número {conta['numero']}")
    print("1. Saque")
    print("2. Depósito")
    print("3. Extrato")
    print("4. Voltar ao menu principal")

def validar_transacao():
    if transacoes_diarias >= LIMITE_TRANSACOES:
        print(f"Limite diário de {LIMITE_TRANSACOES} transações atingido.")
        return False
    return True

def validar_saque(valor):
    if valor > 500:
        print("O valor do saque não pode exceder R$500,00.")
        return False
    elif valor > valor_conta:
        print("Saldo insuficiente.")
        return False
    elif valor <= 0:
        print("O valor do saque deve ser positivo.")
        return False
    return True

def registrar_saque(valor):
    global valor_conta, saques_diarios, transacoes_diarias
    valor_conta -= valor
    extrato.append(f"Saque de R${valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    saques_diarios += 1
    transacoes_diarias += 1
    print(f"Saque de R${valor:.2f} realizado com sucesso. Saldo atual: R${valor_conta:.2f}")

def validar_deposito(valor):
    if valor <= 0:
        print("O valor do depósito deve ser positivo.")
        return False
    return True

def registrar_deposito(valor):
    global valor_conta, transacoes_diarias
    valor_conta += valor
    depositos.append(f"Depósito de R${valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    transacoes_diarias += 1
    print(f"Depósito de R${valor:.2f} realizado com sucesso. Saldo atual: R${valor_conta:.2f}")

def exibir_extrato(saldo, depositos, extrato):
    print("\nExtrato da Conta Bancária:")
    if depositos:
        print("Depósitos:")
        for i, deposito in enumerate(depositos, start=1):
            print(f"{i}. {deposito}")
    else:
        print("Nenhum depósito realizado.")

    if extrato:
        print("\nSaques:")
        for i, saque in enumerate(extrato, start=1):
            print(f"{i}. {saque}")
    else:
        print("Nenhum saque realizado.")

    print(f"\nSaldo atual: R${saldo:.2f}")

def realizar_saque(*, valor):
    if not validar_transacao():
        return
    global saques_diarios
    if saques_diarios >= 3:
        print("Limite de 3 saques diários atingido.")
        return
    if validar_saque(valor):
        registrar_saque(valor)

def realizar_deposito(valor, /):
    if not validar_transacao():
        return
    if validar_deposito(valor):
        registrar_deposito(valor)

def visualizar_extrato():
    exibir_extrato(valor_conta, depositos=depositos, extrato=extrato)

# Função principal
def iniciar_programa():
    while True:
        print("\nMenu Principal:")
        print("1. Cadastrar usuário")
        print("2. Criar conta")
        print("3. Listar contas do usuário")
        print("4. Sair")
        opcao = input("Escolha uma opção (1-4): ")

        if opcao == '1':
            nome = input("Digite o nome do usuário: ")
            cpf = input("Digite o CPF do usuário: ")
            endereco = input("Digite o endereço do usuário (logradouro, numero, bairro, cidade, estado): ")
            cadastrar_usuario(nome, cpf, endereco)
        elif opcao == '2':
            cpf = input("Digite o CPF do usuário para criar a conta: ")
            criar_conta(cpf)
        elif opcao == '3':
            cpf = input("Digite o CPF do usuário para listar as contas: ")
            listar_contas_do_usuario(cpf)
        elif opcao == '4':
            print("Encerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção entre 1 e 4.")

        if contas:
            cpf_usuario = input("Digite o CPF do usuário para acessar uma conta: ")
            contas_usuario = [conta for conta in contas if conta['cpf'] == cpf_usuario]
            if contas_usuario:
                conta = contas_usuario[0]
                while True:
                    exibir_menu_conta(conta)
                    opcao_conta = input("Escolha uma opção (1-4): ")
                    if opcao_conta == '1':
                        try:
                            valor = float(input("Digite o valor do saque (até R$500,00): "))
                            realizar_saque(valor=valor)
                        except ValueError:
                            print("Por favor, insira um valor numérico válido.")
                    elif opcao_conta == '2':
                        try:
                            valor = float(input("Digite o valor do depósito: "))
                            realizar_deposito(valor)
                        except ValueError:
                            print("Por favor, insira um valor numérico válido.")
                    elif opcao_conta == '3':
                        visualizar_extrato()
                    elif opcao_conta == '4':
                        print("Voltando ao menu principal.")
                        break
                    else:
                        print("Opção inválida. Por favor, escolha uma opção entre 1 e 4.")
            else:
                print(f"Nenhuma conta encontrada para o CPF {cpf_usuario}.")
        else:
            print("Nenhuma conta cadastrada.")

# Iniciar o programa
iniciar_programa()
