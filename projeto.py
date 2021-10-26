import os
from datetime import datetime
 

def cadastraCliente(): 
    """Função que solicita as informações do usuario e cadastra o cliente"""

    nome = str(input("Digite o nome do titular da conta: ")) # Solicita a entrada do nome do titular da conta para o usuário
    cpf = str(input("Digite o cpf do titular da conta: ")) # Solicita a entrada do cpf do titular da conta para o usuário
    tipo_conta = str(input("Digite o tipo da conta (conta salário, comum ou plus): ")) # Solicita o tipo de conta para o usuário
    valor_inicial = float(input("Digite o valor inicial da conta: R$")) # Solicita o valor inicial para o usuário
    senha = str(input("Digite a senha da conta: ")) # Solicita a senha da conta para o usuário

    if os.path.isfile("./clientes/" + cpf + ".txt"): # verifica se o arquivo já existe
        print("\nEssa conta já existe.")

    else: # caso o arquivo não exista procede para essa etapa
        arquivo = open("./clientes/" + cpf + ".txt", "w") # cria o arquivo com o nome como o cpf do cliente
        arquivo.write("{0}\n{1}\n{2}\n{3:.2f}\n{4}" .format(nome, cpf, tipo_conta, valor_inicial, senha)) # insere as informações no arquivo, pulando linha entre cada uma delas
        arquivo.close # fecha o arquivo
        print("\nConta criada com sucesso.")


def deletaCliente():
    """Função que solicita as informações do usuario e deleta o cliente caso a senha e o cpf estejam corretos"""

    linhas = [] # define o tipo de dado da variavel linhas como lista
    cpf = str(input("Digite o cpf do titular da conta: ")) # solicia a entrada do cpf para o usuario
    senha = str(input("Digite a senha do titular da conta: ")) # solicia a entrada da senha para o usuario

    if os.path.isfile("./clientes/" + cpf + ".txt"): # verifica se o arquivo existe
        arquivo = open("./clientes/" + cpf + ".txt", "r") # abre o arquivo do cliente no modo de leitura
        linhas = arquivo.readlines() # lê e atribui os valores das linhas para a lista "linhas"
        arquivo.close() # fecha o arquivo

        if linhas[4].strip() == senha: # verifica se a senha está correta
            os.remove("./clientes/" + cpf + ".txt") # caso a senha estiver correta, apague o arquivo do cliente
            if os.path.isfile("./clientes/" + cpf + "_extrato.txt"): # verifica se existe algum arquivo de extrato do cliente
                os.remove("./clientes/" + cpf + "_extrato.txt") # caso existir, apague-o
            print("\nConta Apagada") # caso estiver correta apaga o arquivo e imprime uma mensagem informando que a conta foi apagada

        else: 
            print("\nSenha incorreta") # caso a senha estiver incorreta imprime uma mensagem informando que a senha está errada

    else: # caso o arquivo não exista imprime uma mensagem informando que a conta não existe
        print("\nNão existe uma conta cadastrada com o cpf informado.")


def debitaCliente():
    """Função que solicita as informações do usuario e debita o cliente, levando em consideração a taxa de cada tipo de conta"""

    cpf = str(input("Digite o cpf do titular da conta: "))
    senha = str(input("Digite a senha do titular da conta: "))
    valor_debito = float(input("Digite o valor que deseja debitar da conta: "))


    if os.path.isfile("./clientes/" + cpf + ".txt"): # verifica se o arquivo existe
        arquivo = open("./clientes/" + cpf + ".txt", "r") # abre o arquivo do cliente em modo de leitura
        linhas = arquivo.readlines() # lê e atribui os valores das linhas para a lista "linhas"
        arquivo.close() # fecha o arquivo

        if linhas[4].strip() == senha: # verifica se a senha está correta
            saldo_anterior = linhas[3].strip() # armazena o valor do saldo anterior na variável "saldo_anterior"
            conta = linhas[2].strip() # armazena o tipo de conta na variável "conta"

            if conta.lower() == "comum": # verifica se o tipo da conta é comum
                taxa = 0.03
            
            elif conta.lower().replace("á", "a") == "salario": # verifica se o tipo da conta é salário
                taxa = 0.05

            elif conta.lower() == "plus": # verifica se o tipo da conta é plus
                taxa = 0.01 

            novo_saldo = (float(saldo_anterior) - (valor_debito+(valor_debito*taxa))) # calcula o novo saldo, levando em conta o saldo anterior, o valor do débito e a taxa

            if ((conta == "salário" or  conta == "salario") and novo_saldo < -0) : # caso a conta seja do tipo salário, verifica se o novo saldo estará no limite permitido
                print("\nO debito não pode ser concluido pois o saldo da conta não pode ser negativo.") # caso não esteja no limite, imprime uma mensagem informando que está fora do limite permitido
                return # caso o novo saldo não esteja no limite sai da função

            if conta == ("comum" and novo_saldo < 500.00) : # caso a conta seja do tipo comum, verifica se o novo saldo estará no limite permitido
                print("\nO debito não pode ser concluido pois o saldo da conta não pode ser menor que R$ 500,00.") # caso não esteja no limite, imprime uma mensagem informando que está fora do limite permitido
                return # caso o novo saldo não esteja no limite sai da função


            if (conta == "plus" and novo_saldo < -5000.00) : # caso a conta seja do tipo plus, verifica se o novo saldo estará no limite permitido
                print("\nO debito não pode ser concluido pois o saldo da conta não pode ser menor que R$ 5000,00.") # caso não esteja no limite, imprime uma mensagem informando que está fora do limite permitido
                return # caso o novo saldo não esteja no limite sai da função
           

            arquivo = open("./clientes/" + cpf + ".txt", "w") #abre o arquivo do cliente em modo de escrita

            for linha in linhas: # copia o arquivo do cliente apenas substituindo o valor do saldo anterior pelo valor do novo saldo
                linha = linha.strip()
                mudancas = linha.replace(str(saldo_anterior), str(novo_saldo))
                arquivo.write(mudancas + "\n")

            arquivo.close() # fecha e salva o arquivo

            agora = datetime.now() # armazena a data e o horario de agora
            data = agora.strftime("%d/%m/%Y %H:%M:%S") # formata a data e o horario
            arquivo_extrato = open("./clientes/" + cpf + "_extrato.txt", "a+") # abre o arquivo do extrato do cliente, criando se não existir um (a+)
            arquivo_extrato.write(data + " - " + str(valor_debito) + " " + str(taxa*valor_debito) + " " + str(novo_saldo) + "\n") # armazena as informações do deposito no arquivo
            arquivo_extrato.close() # fecha e salva o arquivo
            print("\nDébito realizado com sucesso.")

        else: # caso a senha estiver incorreta imprime uma mensagem informando que a senha está errada
            print("\nSenha incorreta") 

    else: # caso não exista uma conta com o CPF informado imprime uma mensagem informando que não existe uma conta cadastrada com aquele CPF
        print("\nA conta com o cpf informado não existe.")


def deposita():
    """Função que solicita as informações da conta destino do deposito e caso exista uma conta com o CPF informado deposite o valor na conta destino"""

    cpf = str(input("Digite o cpf do titular da conta: "))
    valor_deposito = float(input("Digite o valor de depósito: "))

    if os.path.isfile("./clientes/" + cpf + ".txt"): # verifica se o arquivo existe
        arquivo = open("./clientes/" + cpf + ".txt", "r") # abre o arquivo da conta do cliente em modo de leitura
        linhas = arquivo.readlines() # atribui o valor das linhas para a lista "linhas"
        arquivo.close() # fecha e salva o arquivo
        saldo_anterior = linhas[3].strip() # armazena o valor do saldo anterior
        novo_saldo = float(saldo_anterior) + float(valor_deposito) # calcula o novo saldo
        arquivo = open("./clientes/" + cpf + ".txt", "w") # abre o arquivo do cliente em modo de escrita

        for linha in linhas: # copia o arquivo, substituindo o saldo anterior com o novo saldo
            linha = linha.strip()
            mudancas = linha.replace(str(saldo_anterior), str(novo_saldo))
            arquivo.write(mudancas + "\n")
        arquivo.close()

        agora = datetime.now() # armazena a data e o horario de agora
        data = agora.strftime("%d/%m/%Y %H:%M:%S") # formata a data e o horario
        arquivo_extrato = open("./clientes/" + cpf + "_extrato.txt", "a+") # abre o arquivo do extrato do cliente, criando se não existir um (a+)
        arquivo_extrato.write(data + " + " + str(valor_deposito) + " " + "0.00" + " " + str(novo_saldo) + "\n") # armazena as informações do deposito no arquivo
        arquivo.close() # fecha e salva o arquivo
        print("\nDeposito realizado com sucesso.") # imprime uma mensagem informando que o deposito foi realizado com sucesso

    else:  # caso não exista uma conta com o CPF informado imprime uma mensagem informando que não existe uma conta cadastrada com aquele CPF
        print("\nNão existe uma conta cadastrada com o CPF informado.")

def mostraSaldo():
    """Função que solicita as informações do usuario e caso a senha esteja correta e exista uma conta com o CPF informado, mostre o saldo da conta destino."""

    cpf = str(input("Digite o cpf do titular da conta: "))
    senha = str(input("Digite a senha do titular da conta: "))

    if os.path.isfile("./clientes/" + cpf + ".txt"): # verifica se o arquivo existe
        arquivo = open("./clientes/" + cpf + ".txt", "r") # abre o arquivo do cliente no modo de leitura
        linhas = arquivo.readlines() # lê e atribui os valores das linhas para a lista "linhas"
        arquivo.close() # fecha o arquivo

        if linhas[4].strip() == senha: # verifica se a senha está correta
            saldo = linhas[3].strip() 
            print("\nO seu saldo é de R$ {0:.2f}" .format(float(saldo))) # caso estiver correta apaga o arquivo e imprime uma mensagem informando o saldo do usuário

        else: 
            print("\nSenha incorreta") # caso a senha estiver incorreta imprime uma mensagem informando que a senha está errada


    else: # caso não exista uma conta com o CPF informado imprime uma mensagem informando que não existe uma conta cadastrada com aquele CPF
        print("\nNão existe uma conta cadastrada com o CPF informado.") 
    
def mostraExtrato():
    cpf = str(input("Digite o cpf do titular da conta: ")) # solicia a entrada do cpf para o usuario
    senha = str(input("Digite a senha do titular da conta: ")) # solicia a entrada da senha para o usuario

    if os.path.isfile("./clientes/" + cpf + ".txt"): # verifica se o arquivo existe
        if os.path.isfile("./clientes/" + cpf + "_extrato.txt"): # verifica se o arquivo existe
            arquivo_conta = open("./clientes/" + cpf + ".txt", "r") # abre o arquivo da conta em modo de leitura
            linhas_conta = arquivo_conta.readlines() # atribui linhas_conta como as linhas do arquivo da conta
            
            if linhas_conta[4].strip() == senha: # verifica se a senha está correta
                print("\nNome: {0}\nCPF: {1}\nConta: {2}" .format(linhas_conta[0].strip(), cpf, linhas_conta[2].strip())) # imprime o nome, cpf e o tipo de conta do usuário
                arquivo_conta.close() # fecha e salva o arquivo da conta

                arquivo_extrato = open("./clientes/" + cpf + "_extrato.txt", "r") # abre o arquivo do extrato no modo de leitura
                
                linhas = arquivo_extrato.readlines() # lê e atribui os valores das linhas do extrato para a lista "linhas"
                extrato = [] # inicia o extrato como uma lista vazia
                
                for linha in linhas: # atribui o valor das palavras separadas por espaço na lista "extrato"
                    linha_separada = linha.split(" ")
                    extrato.append(linha_separada)

                arquivo_extrato.close() # fecha o arquivo de extrato
                
                
                for x in range(len(extrato)): # printa o extrato, percorrendo a lista do extrato linha por linha
                    print("Data: {0} {1}  {2}  {3:<6}   Tarifa:  {4}  Saldo:   {5:<6}" .format(extrato[x][0], extrato[x][1], extrato[x][2], extrato[x][3], extrato[x][4], extrato[x][5]), end="")

            else: # caso a senha estiver incorreta imprime uma mensagem informando que a senha está errada
                print("\nSenha incorreta") 

        else: # caso o arquivo de extrato não exista imprime uma mensagem informando que a conta não existe
            print("\nNenhuma transação foi realizada na conta.")
    else:
            print("\nNão existe uma conta cadastrada com o cpf informado.")

while True:
    print("\nMenu:")
    print(" 1 - Novo Cliente\n 2 - Apaga Cliente\n 3 - Debita\n 4 - Deposita\n 5 - Saldo\n 6 - Extrato \n \n \n 0 - Sai") 
    opcao = int(input("Digite o número da opção desejada: "))

    if opcao == 0: #caso o usuario digite 0 o programa sai do loop infinito
        break

    if opcao == 1: #/caso o usuario digite 1 chame a função para cadastrar o cliente
        cadastraCliente()

    if opcao == 2: #caso o usuario digite 2 chame a função para deletar o cliente
        deletaCliente()

    if opcao == 3: #caso o usuario digite 3 chame a função para debitar o cliente
        debitaCliente()

    if opcao == 4: #caso o usuario digite 4 chame a função para depositar para o cliente
        deposita()

    if opcao == 5: #caso o usuario digite 5 chame a função para mostrar o saldo do cliente
        mostraSaldo()

    if opcao == 6: #caso o usuario digite 6 chame a função para mostrar o extrato do cliente
        mostraExtrato()
    