import math
import random
import qm
import numpy as np


def gerar_template(lista):
    tabela = []

    linhas = len(lista)
    for i in range(2, linhas):
        aux = lista[i].split()
        z = 0
        l = []
        for j in range(6):

            if j == 1 or j == 3:
                l.append('')
            else:
                l.append(aux[z])
                z += 1
        tabela.append(l)
    return tabela


def gerar_individuo(lista, tabela):
    qtd_estados = int(lista[0])
    bits = math.ceil(math.log2(qtd_estados))
    total = pow(2, bits)
    mapa = list(range(total))
    individuo = np.zeros((2, qtd_estados + 1), dtype=str)

    x = 0
    for j in range(1, len(tabela)):
        if tabela[j][0] not in individuo:
            individuo[0][x] = tabela[j][0]
            x += 1

    for i in range(qtd_estados):
        valor = random.choice(mapa)
        individuo[1][i] = valor
        mapa.remove(valor)
    return individuo


def converterSaida(num, bitout):
    binary = bin(num)[2:]
    aux = ''
    if len(binary) < bitout:
        t = len(binary)
        while t < bitout:
            aux += '0'
            t += 1
        binary = aux + binary
    return binary


def converter(num, bits):
    binario = bin(num)[2:]
    aux = ''
    if len(binario) < bits:
        t = len(binario)
        while t < bits:
            aux += '0'
            t += 1
        binario = aux + binario

    return binario


def preencher_template(lista, tabela, individuo):
    linhas = len(lista)
    bitout = int(lista[1].split()[1])
    bits = math.ceil(math.log2(int(lista[0])))

    for i in range(linhas - 2):
        for j in range(1, 4, 2):
            for y in range(5):
                if tabela[i][j-1] == individuo[0][y]:
                    num = int(individuo[1][y])
                    tabela[i][j] = converter(num, bits)

        tabela[i][5] = converterSaida(int(tabela[i][5]), bitout)

    return tabela


def cols_prox_estado_e_mint(bits, tabela):
    #pegar variaveis individual da coluna de proximo estado
    resposta = criar_variaveis_prox_estado(bits)
    lista_variaveis = resposta[0]

    for item in tabela:
        for j in range(len(lista_variaveis)):
            lista_variaveis['y'+str(j)].append(item[3][j])

    #obter os mintermos de cada variavel
    mintermos = resposta[1]
    for i in range(len(mintermos)):
        mintermos['y' + str(i)] = obter_mintermos(lista_variaveis['y' + str(i)], tabela)

    #salvar custo de cada coluna
    custos = []
    for i in range(len(mintermos)):
        custos.append(calcula_custo(bits, mintermos['y' + str(i)]))

    return custos


def cols_saida_e_mint(bits, tabela):
    resposta = criar_variaveis_saida(bits)
    lista_saida = resposta[0]
    for item in tabela:
        for j in range(len(lista_saida)):
            lista_saida['s'+str(j)].append(item[5][j])

    # obter os mintermos da saida
    mintermos = resposta[1]
    for i in range(len(mintermos)):
        mintermos['s' + str(i)] = obter_mintermos(lista_saida['s' + str(i)], tabela)

    custo_saida = []
    for i in range(len(mintermos)):
        custo_saida.append(calcula_custo(3, mintermos['s' + str(i)]))

    return custo_saida


def criar_variaveis_saida(n_bits):
    variaveis_saida = {}
    mintermos = {}
    retorno = []
    for i in range(n_bits):
        l = []
        variaveis_saida['s' + str(i)] = l
        mintermos['s' + str(i)] = l

    retorno.append(variaveis_saida)
    retorno.append(mintermos)
    return retorno


def calcula_custo(bits, mintermos):
    aux = str(mintermos)
    aux = aux[1:-1]
    n = bits + 1

    resultado = qm.main_test(n, aux)
    #print(resultado)

    custo = []
    for i in resultado:
        cont = 0
        for l in i:
            if l != '-':
                cont += 1
        custo.append(cont)

    custo_total = 0
    for j in custo:
        custo_total += j

    custo_total += len(resultado)
    return custo_total


def criar_variaveis_prox_estado(bits):
    lista_variaveis = {}
    mintermos = {}
    retorno = []
    for i in range(bits):
        l = []
        lista_variaveis['y' + str(i)] = l
        mintermos['y' + str(i)] = l

    retorno.append(lista_variaveis)
    retorno.append(mintermos)
    return retorno


def obter_mintermos(lista_variaveis, tabela):
    aux = []
    mint = []
    cont = 0
    for valor in lista_variaveis:
        if valor == '1':
            aux.append(tabela[cont][1] + tabela[cont][4])

        cont += 1

    for i in aux:
        mint.append(int(i, base=2))

    return mint

def main():
    arq = open('maquinaVendas.txt', 'r')
    lista = arq.readlines()
    qtd_estados = int(lista[0])
    bitout = int(lista[1].split()[1])
    bits = math.ceil(math.log2(qtd_estados))

    tabela = gerar_template(lista)
    individuo = gerar_individuo(lista, tabela)

    novatabela = preencher_template(lista, tabela, individuo)
    custo = cols_prox_estado_e_mint(bits, novatabela)
    custo_saida = cols_saida_e_mint(bitout, novatabela)

    for i in range(len(custo_saida)):
        custo.append(custo_saida[i])

    print(custo)


if __name__ == "__main__":
    main()