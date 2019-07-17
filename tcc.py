import math
import random
import qm
import string
from sympy.logic import SOPform
from sympy import symbols


def gerar_template(lista):
    tabela = []
    linhas = len(lista)

    # print(lista[5])
    for i in range(5, linhas):
        aux = lista[i].split()
        z = 0
        l = []
        for j in range(6):

            if j == 2 or j == 4:
                l.append('')
            else:
                if '-' in aux[z]:
                    aux[z] = aux[z].replace('-', '0')
                l.append(aux[z])
                z += 1
        tabela.append(l)

    return tabela


def gerar_individuo(lista, tabela, mapa):
    qtd_estados = int(lista[4].split()[1])
    #bits = math.ceil(math.log2(qtd_estados))
    # total = pow(2, bits)
    # mapa = list(range(total))
    individuo = []
    # print(len(tabela))

    aux = []
    for j in range(len(tabela)):
        if tabela[j][1] not in aux:
            aux.append(tabela[j][1])
        if tabela[j][3] not in aux:
            aux.append(tabela[j][3])
    individuo.append(aux)

    l = []
    for k in range(qtd_estados):
        valor = random.choice(mapa)
        l.append(valor)
        mapa.remove(valor)
    individuo.append(l)

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


def preencher_template(lista, template, individuo):
    linhas = len(lista)
    qtd_estados = int(lista[4].split()[1])
    bits = math.ceil(math.log2(qtd_estados))
    # print(individuo)
    for i in range(linhas - 5):
        for j in range(2, 5, 2):
            for y in range(qtd_estados):
                if template[i][j-1] == individuo[0][y]:
                    num = int(individuo[1][y])
                    template[i][j] = converter(num, bits)

    return template


def cols_prox_estado_e_mint(bitin, bits, entradas, template, individuo):
    #pegar variaveis individual da coluna de proximo estado
    resposta = criar_variaveis_prox_estado(bits)
    lista_variaveis = resposta[0]

    #print(lista_variaveis)
    #print(template)
    c = 0
    for item in template:
        #print(item[3][0])
        for j in range(len(lista_variaveis)):
            #print(c)
            lista_variaveis['y'+str(j)].append(item[4][j])
            c += 1

    #obter os mintermos de cada variavel
    mintermos = resposta[1]
    for i in range(len(mintermos)):
        mintermos['y' + str(i)] = obter_mintermos(lista_variaveis['y' + str(i)], template)

    #print(mintermos['y' + str(0)])
    #salvar custo de cada coluna
    #calcula_custo(bitin, bits, mintermos['y' + str(i)], individuo)
    custos = []
    termos = []
    expressao = []
    for i in range(len(mintermos)):
        valor, term, expres = calcula_custo(bitin, bits, entradas, mintermos['y' + str(i)], individuo)
        custos.append(valor)
        termos.append(term)
        expressao.append(expres)
    #print(custos)
    return custos, termos, expressao


def cols_saida_e_mint(bitin, bitout, bits, entradas, template, individuo):
    resposta = criar_variaveis_saida(bitout)
    lista_saida = resposta[0]
    for item in template:
        for j in range(len(lista_saida)):
            lista_saida['s'+str(j)].append(item[5][j])

    # obter os mintermos da saida
    mintermos = resposta[1]
    for i in range(len(mintermos)):
        mintermos['s' + str(i)] = obter_mintermos(lista_saida['s' + str(i)], template)

    custo_saida = []
    termos_saida = []
    expressao_saida = []
    for i in range(len(mintermos)):
        valor, term, expres = calcula_custo(bitin, bits, entradas, mintermos['s' + str(i)], individuo)
        custo_saida.append(valor)
        termos_saida.append(term)
        expressao_saida.append(expres)
    #print(custo_saida)
    return custo_saida, termos_saida, expressao_saida


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


def calcula_custo(bitin, bits, entradas, mintermos, individuo):

    n = bits + bitin
    dontcares = obter_dontcare(entradas, bits, individuo)

    var = list(string.ascii_lowercase[:n])

    test = symbols(var)
    #a, b, c, d, e = symbols('a b c d e')

    resultado = SOPform(test, mintermos, dontcares)

    expressao = str(resultado)
    #print(resultado)

    #custo = []
    termos = expressao.count('|')+1
    cont = 0
    for i in expressao:
        if i in var:
            cont += 1

    cont += termos
    #print(cont)
    #custo.append(cont)

    # custo_total = 0
    # for j in custo:
    #     custo_total += j

    #custo_total += len(resultado)
    return cont, termos, expressao


def calcula_custo_saida(bits, mintermos):
    aux = str(mintermos)
    aux = aux[1:-1]
    n = bits

    if aux == '':
        resultado = []
    else:
        resultado = qm.main_test(n, mintermos)

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


def obter_mintermos(lista_variaveis, template):

    #print(lista_variaveis)
    aux = []
    mint = []
    cont = 0
    for valor in lista_variaveis:
        if valor == '1':
            aux.append(template[cont][0] + template[cont][2])

        cont += 1

    #print(aux)

    for i in aux:
        novo = []
        for x in range(len(i)):
            # if i[x] == '-':
            #     novo.append(i[x])
            # else:
            novo.append(int(i[x]))
        mint.append(novo)

    #print(mint)
    return mint


def obter_dontcare(entradas, bits, individuo):
    mapa = list(range(pow(2, bits)))

    for i in range(len(individuo[1])):
        if individuo[1][i] in mapa:
            mapa.remove(individuo[1][i])

    no_used = []
    for x in mapa:
        aux = converter(x, bits)
        no_used.append(aux)

    dontcare = []
    for i in entradas:
        for j in no_used:
            dontcare.append(i + j)

    teste = []
    for i in dontcare:
        aux = []
        for x in range(len(i)):
            # if i[x] == '-':
            #     aux.append(i[x])
            # else:
            aux.append(int(i[x]))
        teste.append(aux)


    # print(teste)
    return teste


def main():
    arq = open('kiss2/bbara.kiss2', 'r')
    # lista = arq.readlines()
    # qtd_estados = int(lista[4].split()[1])
    # bitout = int(lista[2].split()[1])
    # bitin = int(lista[1].split()[1])
    # bits = math.ceil(math.log2(qtd_estados))
    #
    # entradas = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111' +
    #             '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
    #
    # tabela = gerar_template(lista)
    # individuo = gerar_individuo(lista, tabela)
    #
    # #obter_dontcare(bits, individuo)
    # novatabela = preencher_template(lista, tabela, individuo)
    # custo, termos, expressao = cols_prox_estado_e_mint(bitin, bits, entradas, novatabela, individuo)
    # custo_saida, terms, express = cols_saida_e_mint(bitin, bitout, bits, entradas, novatabela, individuo)
    #
    # for i in range(len(custo_saida)):
    #     custo.append(custo_saida[i])
    #
    # for i in range(len(terms)):
    #     termos.append(terms[i])
    #
    # for i in range(len(express)):
    #     expressao.append(express[i])
    #
    # #print(qtd_estados, bitout, bits)
    # print(novatabela)
    # print(custo, termos, expressao)


if __name__ == "__main__":
    main()