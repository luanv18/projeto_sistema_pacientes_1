**Disciplina: Programação de Ciencia de Dados**
**Curso: MBA Ciência de Dados**
**Instrutor: Cassio Pinheiro**
**Integrante: Luan Victor**


Repositório Github:
Data de entrega: 08/11/2025

##  Requisitos Técnicos
Linguagem: Python 3.12 +
Tipos de dados, estruturas de controle, funções, compreensões, manipulação de arquivos

# Sistema de Controle de Pacientes e Consultas



## 📋 Objetivo

Projeto desenvolvido com foco na prática dos fundamentos da linguagem Python, abordando estruturas de dados, controle de fluxo, funções e manipulação de arquivos.
O sistema tem como objetivo registrar pacientes e consultas médicas, armazenando as informações tanto em memória (durante a execução) quanto em arquivos CSV para persistência dos dados.

## 🗺️ Diagrama de Contexto



## Funcionalidades por função

1. **Carregar pacientes**

**A função *carregar_paciente()* é responsável por inicializar o dicionário *global pacientes* a partir dos dados armazenados no arquivo *pacientes.csv*.**

**Ela garante que o programa possa continuar de onde parou, carregando os pacientes previamente cadastrados. Caso o arquivo não exista, ele é automaticamente criado com os cabeçalhos necessários.**

**Principais etapas:**

1. **Importa o módulo *csv* e torna a variável *pacientes* global, permitindo sua modificação dentro da função.**

2. **Tenta abrir o arquivo *pacientes.csv* e ler seu conteúdo usando *csv.DictReader*.**

3. **Caso o arquivo não exista, o bloco *except* é acionado, criando um novo arquivo com os cabeçalhos padrão.**

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

///////////////////////////////////////////////////////////////////////
2. **Cadastro de Pacientes**

**A função *cadastrar_paciente()* realiza o registro de novos pacientes, recebendo as informações diretamente da função principal (*main()*) através de *input()*.**

**Etapas do processo:**

1. **Verifica se o CPF informado já existe no dicionário global *pacientes*.**

2. **Caso o paciente ainda não esteja cadastrado, os dados são adicionados ao dicionário em memória.**

3. **O novo registro é então salvo no arquivo *pacientes.csv* em modo de acréscimo (*"a"*), garantindo persistência sem sobrescrever os dados anteriores.**

**Explicação adicional:**

**O parâmetro *newline=""* evita que sejam adicionadas linhas em branco extras ao salvar o arquivo.**

**O uso de *global pacientes* permite que o dicionário seja atualizado de forma acessível por outras funções.**

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

///////////////////////////////////////////////////////////////////////
3. **Registro de Consultas**

**A função *registrar_consulta()* é responsável por registrar uma nova consulta médica associada a um paciente já cadastrado.**

**Inicialmente, utilizamos o bloco *try/except* para verificar se o arquivo *consultas.csv* existe. Caso contrário, o arquivo é criado automaticamente com os cabeçalhos necessários para armazenar os dados de cada consulta.**

**Em seguida, inicializamos uma lista *consultas* para manter em memória todos os registros existentes, garantindo que novas consultas sejam adicionadas sem sobrescrever informações anteriores.**

**Após isso, o sistema solicita o CPF do paciente para vincular a consulta. Se o CPF informado não estiver cadastrado, o programa informa ao usuário que o paciente não foi encontrado e interrompe a execução da função com *return*.**

**Quando o CPF é válido, são solicitadas as informações da consulta — nome do médico, data, sintomas e diagnóstico — que são armazenadas em um dicionário e adicionadas à lista de consultas.**

**Por fim, o arquivo *consultas.csv* é aberto novamente em modo de acréscimo (*"a"*) e a nova consulta é gravada utilizando *csv.DictWriter*, respeitando os cabeçalhos definidos.**

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

///////////////////////////////////////////////////////////////////////
4. **Calculo Doenças Comuns**

**Nesta função, realizamos a leitura do arquivo *consultas.csv* para identificar e contar as doenças mais registradas no sistema.**

**Primeiro, abrimos o arquivo e lemos todos os registros utilizando o módulo *csv*. Em seguida, criamos um dicionário de contagem, onde cada chave representa o nome de uma doença (diagnóstico) e o valor indica quantas vezes ela aparece nos registros.**

**Para cada linha do arquivo, acessamos o campo “diagnostico” e incrementamos a contagem correspondente. Caso a doença ainda não exista no dicionário, ela é adicionada com valor inicial igual a 1.**

**Ao final, a lista de doenças é ordenada do maior para o menor número de ocorrências, permitindo identificar quais são as doenças mais comuns entre os pacientes.**

**O resultado é exibido de forma numerada e organizada no terminal.**

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

///////////////////////////////////////////////////////////////////////
5. **Atendimentos por Médico**

**De forma semelhante à função “Doenças Mais Comuns”, esta função analisa o arquivo *consultas.csv* para contar o número de atendimentos realizados por cada médico.**

**Primeiro, abrimos o arquivo e lemos os dados com *csv.DictReader*. Em seguida, criamos um dicionário de contagem, onde a chave representa o nome do médico e o valor indica quantos atendimentos ele realizou.**

**Para cada linha do arquivo, verificamos o campo “medico” e somamos +1 à sua contagem. Caso o nome do médico ainda não exista no dicionário, ele é adicionado com valor inicial igual a 1.**

**No final, a lista é ordenada do médico com mais atendimentos para o com menos, exibindo um ranking completo no terminal.**

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

///////////////////////////////////////////////////////////////////////
6.  **Historico paciente**

**Nessa função, pesquisamos o histórico completo de consultas de um paciente específico.**

**Primeiro, verificamos se o CPF informado está cadastrado no sistema. Caso não esteja, exibimos uma mensagem informando que o paciente não foi encontrado e encerramos a função.**

**Em seguida, abrimos o arquivo *consultas.csv* e percorremos todas as consultas registradas, filtrando apenas aquelas que correspondem ao CPF do paciente.**

**Por fim, exibimos de forma organizada todas as consultas do paciente, incluindo data, médico e diagnóstico, representando o histórico completo de atendimentos.**

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

## Função main()

**A função *main()* é o ponto central do programa.**
**Ela exibe o menu principal, permitindo ao usuário escolher entre as opções disponíveis (como cadastrar pacientes, registrar consultas, ver estatísticas e histórico).**
**Com base na escolha, chama a função correspondente e mantém o programa em execução até que o usuário opte por sair.**

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