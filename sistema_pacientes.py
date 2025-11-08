# sistema_pacientes.py

pacientes = {}  # {cpf: dados_paciente}
consultas = []  # Lista de consultas

def carregar_paciente():
    """Cadastra novo paciente."""
    
    import csv
    global pacientes

    try:
        with open("pacientes.csv", "r", newline="") as arquivo:
            lerpacientes = csv.DictReader(arquivo)
            for linha in lerpacientes:
                cpf = linha["cpf"]
                pacientes[cpf] = {
                'nome' :linha['nome'],
                'idade' :linha['idade'],
                'sexo' :linha['sexo'],
                'telefone' :linha['telefone']
                }

    except FileNotFoundError:
        print('Arquivo "pacientes.csv" não encontrando, gerando um novo arquivo...')
        with open("pacientes.csv", "w", newline="") as arquivo:
            criararquivo = csv.writer(arquivo)
            criararquivo.writerow(['cpf','nome','idade','sexo','telefone'])            
    

def cadastrar_paciente(cpf, nome, idade, sexo, telefone):
    
    import csv
    global pacientes

    if cpf in pacientes:
        print("paciente já cadastrado!")
        return
    
    pacientes[cpf] = {
        'nome': nome,
        'idade': idade,
        'sexo' : sexo,
        'telefone' : telefone
    }

    with open("pacientes.csv", "a", newline="") as arquivo:
        cadastrarpac = csv.writer(arquivo)
        cadastrarpac.writerow([cpf, nome, idade , sexo , telefone])
        print(f"Paciente {nome} cadastrado com sucesso!")


def registrar_consulta():
    """Registra nova consulta."""

    import csv
    global pacientes, consultas

    consultas = []

    try:
        with open("consultas.csv", "r", newline="") as arquivo:
            lerconsultas = csv.DictReader(arquivo)
            for linha in lerconsultas:
                consultas.append(linha)

    except FileNotFoundError:
        print('Arquivo "consultas.csv" não encontrando, gerando um novo arquivo...')
        with open("consultas.csv", "w", newline="") as arquivo:
            criararquivo = csv.writer(arquivo)
            criararquivo.writerow(['cpf','medico','data','sintomas','diagnostico'])  

    cpf = input("CPF do paciente: ")
    if cpf not in pacientes:
        print("CPF não cadastrado, cadastre o CPF antes de prosseguir para a consulta")
        return

    medico = input("Nome do Médico: ")
    data = input("Data: ")
    sintomas = input("Sintomas: ")
    diagnostico = input("Diagnostico: ")

    nova_consulta = {
        "cpf" : cpf,
        "medico" : medico,
        "data" : data,
        "sintomas" : sintomas,
        "diagnostico" : diagnostico
    }

    consultas.append(nova_consulta)

    with open("consultas.csv","a", newline="") as arquivo:
        escreverconsulta = csv.DictWriter(arquivo, fieldnames=["cpf", 'medico', "data" ,"sintomas", "diagnostico"])
        escreverconsulta.writerow(nova_consulta)
    
    print(f"Consulta de {pacientes[cpf]['nome']} registrada com sucesso!\n")


def calcular_doencas_comuns(limite=5):
    """Identifica doenças mais comuns."""
    import csv
    

    with open("consultas.csv", "r", newline="") as arquivo:
        contagem = csv.DictReader(arquivo)
        diagnosticos = []
        for linha in contagem:
            doenca = linha["diagnostico"].strip().lower()
            if doenca:
                diagnosticos.append(doenca)
    
    if not diagnosticos:
        print("Nenhum diagnostico encontrado.")
        return
    
    contagem = {}
    
    for doenca in diagnosticos:
        if doenca in contagem:
            contagem[doenca] += 1
        else:
            contagem[doenca] = 1
    
    lista_ordenada = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    print("\n Doenças mais comuns")
    for i, (doenca, quantidade) in enumerate(lista_ordenada[:limite], 1):
        print(f"{i}. {doenca.capitalize()} - {quantidade} caso(s)")

def calcular_atendimentos_por_medico():
    """Calcula atendimentos por médico."""
    import csv

    with open("consultas.csv", "r", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        contagem = {}
        
        for linha in leitor:
            medico = linha["medico"].strip().title()
            if medico:
                if medico in contagem:
                    contagem[medico] += 1
                else:
                    contagem[medico] = 1
        
        if not contagem:
            print("Nenhum atendimento encontrado.")
            return
        
        print("\n Atendimento por médico")
        for i, (medico, qtd) in enumerate(sorted(contagem.items(), key=lambda x: x[1], reverse=True), 1):
            print(f"{i}. {medico} - {qtd} atendimentos(s)")


def gerar_historico_paciente(cpf):
    """Gera histórico médico do paciente."""
    
    import csv
    global pacientes, consultas

    if cpf not in pacientes:
        print("Paciente não cadastrado.")
        return
    
    with open("consultas.csv", "r", newline="") as arquivo:
        lerconsultas = csv.DictReader(arquivo)
        historico = []
        for linha in lerconsultas:
            if linha['cpf'] == cpf:
                historico.append(linha)
    
    if not historico:
        print("Nenhuma consulta encontrada para este paciente.")
        return
    
    print(f"Registro de {pacientes[cpf]['nome'].upper()}")
    for i, c in enumerate(historico, 1):
        print(f"{i}. Data: {c['data']} | Médico: {c['medico']} | Diagnostico: {c['diagnostico']}")

def main():
    """Função principal."""

    carregar_paciente()

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1 - Cadastrar paciente")
        print("2 - Registrar consulta")
        print("3 - Listar pacientes")
        print("4 - Histórico do paciente")
        print("5 - Doenças mais comuns")
        print("6 - Atendimentos por médico")
        print("7 - Sair")
        

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cpf = input("CPF: ")
            nome = input('Nome: ')
            idade = input('Idade: ')
            sexo = input('Sexo: ')
            telefone = input('Telefone: ')

            cadastrar_paciente(cpf, nome, idade, sexo, telefone)

            continuar = input("Deseja cadastrar outro paciente? (sim/nao): ").lower()
            if continuar != "sim":
                print("Encerrando o cadastro...")

        elif opcao == "2":
            registrar_consulta()

        elif opcao == "3":
            print(pacientes)

        elif opcao == "4":
            cpf = input("Digite o CPF do paciente: ")
            gerar_historico_paciente(cpf)

        elif opcao == "5":
            calcular_doencas_comuns()
        
        elif opcao == "6":
            calcular_atendimentos_por_medico()

        elif opcao == "7":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida! Tente novamente.")

main()