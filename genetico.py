# -*- coding: utf-8 -*-
import tcc
import math
import random
import time
import os
import multiprocessing as mp

class Individuo():
    def __init__(self, geracao=0):
        total = pow(2, bits)
        self.mapa = list(range(total))
        self.nota_avaliacao = 0
        self.proporcao_roleta = 0
        self.qtd_termos = 0
        self.expressao = []
        self.geracao = geracao
        self.template = tcc.gerar_template(lista)
        self.cromossomo = tcc.gerar_individuo(lista, self.template, self.mapa)


    def avaliacao(self, template, entradas):
        custo, termos, expressao = tcc.cols_prox_estado_e_mint(bitin, bits, entradas, template, self.cromossomo)
        custo_out, terms, expres = tcc.cols_saida_e_mint(bitin, bitout, bits, entradas, template, self.cromossomo)

        for i in range(len(custo_out)):
            custo.append(custo_out[i])

        for i in range(len(terms)):
            termos.append(terms[i])

        for i in range(len(expres)):
            expressao.append(expres[i])

        custo_total = 0
        for i in custo:
            custo_total += i

        termos_total = 0
        for i in termos:
            termos_total += i

        print(self.cromossomo, custo_total)

        self.nota_avaliacao = custo_total
        self.qtd_termos = termos_total
        self.expressao = expressao

    def crossover(self, outro_individuo):
        corte = round(random.random() * len(self.cromossomo))
        #corte = 3

        filho1 = []
        aux = self.cromossomo[0][0::]
        filho1.append(aux)
        filho1.append(outro_individuo.cromossomo[1][0:corte] + self.cromossomo[1][corte::])

        filho2 = []
        aux = self.cromossomo[0][0::]
        filho2.append(aux)
        filho2.append(self.cromossomo[1][0:corte] + outro_individuo.cromossomo[1][corte::])

        filhos = [Individuo(self.geracao + 1),
                  Individuo(self.geracao + 1)]

        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2

        return filhos

    def troca(self):
        total = pow(2, bits)
        mapa = list(range(total))
        for i in range(len(self.cromossomo[1])):
            if self.cromossomo[1][i] in mapa:
                mapa.remove(self.cromossomo[1][i])

        if not len(mapa) == 0:
            for j in range(len(self.cromossomo[1])):
                for k in range(j+1, len(self.cromossomo[1])):
                    if self.cromossomo[1][j] == self.cromossomo[1][k]:
                        valor = random.choice(mapa)
                        mapa.append(self.cromossomo[1][j])
                        self.cromossomo[1][j] = valor
                        mapa.remove(valor)
                    if j+1 > len(self.cromossomo[1]):
                        break

        return self

    def mutacao(self, taxa_mutacao):

        if random.random() < taxa_mutacao:

            if random.random() < 0.5:
                if len(self.mapa) == 0:
                    p1 = random.choice(self.cromossomo[1])
                    pos1 = self.cromossomo[1].index(p1)
                else:
                    p1 = random.choice(self.mapa)
                    pos1 = self.mapa.index(p1)
            else:
                p1 = random.choice(self.cromossomo[1])
                pos1 = self.cromossomo[1].index(p1)

            p2 = random.choice(self.cromossomo[1])
            while p1 == p2:
                p2 = random.choice(self.cromossomo[1])

            pos2 = self.cromossomo[1].index(p2)

            self.cromossomo[1][pos1] = p2
            self.cromossomo[1][pos2] = p1

        return self


class AlgoritimoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []

    def inicializa_populacao(self):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo())
        self.melhor_solucao = self.populacao[0]

    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.nota_avaliacao)

    def preenche_template(self):
        for i in range(len(self.populacao)):
            self.populacao[i].template = tcc.preencher_template(lista, self.populacao[i].template, self.populacao[i].cromossomo)

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao < self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self):
        soma = 0
        for i in range(len(self.populacao)):
            soma += self.populacao[i].nota_avaliacao
        return soma

    def calcula_proporcao(self):
        pior = self.populacao[len(self.populacao) - 1].nota_avaliacao
        for i in range(len(self.populacao)):
            valor = int((self.populacao[i].nota_avaliacao / pior) * 100) - 100
            self.populacao[i].proporcao_roleta = abs(valor)

    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random.random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            if self.populacao[i].proporcao_roleta == 0:
                soma += self.populacao[i].nota_avaliacao
            else:
                soma += self.populacao[i].nota_avaliacao * (self.populacao[i].proporcao_roleta / 10) * 2
            pai += 1
            i += 1

        return pai

    def executarParalelo(self, populacao, entradas):
        processos = []
        for i in range(len(populacao)):
            p = mp.Process(target=populacao[i].avaliacao(populacao[i].template, entradas))
            p.start()
            processos.append(p)

        for p in processos:
            p.join()

    def resolver(self, numero_geracoes, taxa_mutacao, entradas):
        #print(entradas)
        self.inicializa_populacao()
        self.preenche_template()

        self.executarParalelo(self.populacao, entradas)

        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)

        self.calcula_proporcao()
        taxa_cruzamento = int(0.4 * self.tamanho_populacao)

        for geracao in range(numero_geracoes):
            # self.processo(taxa_cruzamento, taxa_mutacao)
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []

            for individuos_gerados in range(0, taxa_cruzamento, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)

                if pai1 == pai2:
                    pai2 = self.seleciona_pai(soma_avaliacao)

                # print('p1', pai1, 'p2', pai2)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                for i in range(len(filhos)):
                    if len(filhos[i].cromossomo[1]) == len(set(filhos[i].cromossomo[1])):
                        nova_populacao.append(filhos[i].mutacao(taxa_mutacao))
                    else:
                        nova_populacao.append(filhos[i].troca())

            for i in range(len(nova_populacao)):
                aux = random.choice(self.populacao)
                self.populacao.remove(aux)

            nova_populacao.extend(self.populacao)

            self.populacao = list(nova_populacao)
            self.preenche_template()

            self.executarParalelo(self.populacao, entradas)

            self.ordena_populacao()

            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)

            self.calcula_proporcao()
            self.melhor_individuo(melhor)

            # print(cont)
            # if cont > 5:
            # print('criterio de parada')
            # break

            arq = open('teste2.txt', 'a')
            texto = str(melhor.cromossomo) + ' - ' + str(melhor.nota_avaliacao) + ' - ' + str(
                melhor.qtd_termos) + ' - ' + str(melhor.expressao) + '\n'
            arq.write(texto)
            arq.close()

        print(self.melhor_solucao.geracao)
        return self.melhor_solucao.cromossomo, self.melhor_solucao.nota_avaliacao, self.melhor_solucao.qtd_termos


if __name__ == '__main__':
    arq = open('kiss2/bbtas.kiss2', 'r')
    lista = arq.readlines()
    qtd_estados = int(lista[4].split()[1])
    bitout = int(lista[2].split()[1])
    bitin = int(lista[1].split()[1])
    bits = math.ceil(math.log2(qtd_estados))

    entradas = []
    if bitin == 1:
        entradas = ['0', '1']
    elif bitin == 2:
        entradas = ['00', '01', '10', '11']
    elif bitin == 3:
        entradas = ['000', '001', '010', '011', '100', '101', '110', '111']
    elif bitin == 4:
        entradas = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
                    '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
    elif bitin == 5:
        entradas = ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111',
                    '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111',
                    '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111',
                    '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111']
    elif bitin == 6:
        entradas = ['000000', '000001', '000010', '000011', '000100', '000101', '000110', '000111',
                    '001000', '001001', '001010', '001011', '001100', '001101', '001110', '001111',
                    '010000', '010001', '010010', '010011', '010100', '010101', '010110', '010111',
                    '011000', '011001', '011010', '011011', '011100', '011101', '011110', '011111',
                    '100000', '100001', '100010', '100011', '100100', '100101', '100110', '100111',
                    '101000', '101001', '101010', '101011', '101100', '101101', '101110', '101111',
                    '110000', '110001', '110010', '110011', '110100', '110101', '110110', '110111',
                    '111000', '111001', '111010', '111011', '111100', '111101', '111110', '111111']
    elif bitin == 7:
        entradas = ['0000000', '0000001', '0000010', '0000011', '0000100', '0000101', '0000110', '0000111',
                    '0001000', '0001001', '0001010', '0001011', '0001100', '0001101', '0001110', '0001111',
                    '0010000', '0010001', '0010010', '0010011', '0010100', '0010101', '0010110', '0010111',
                    '0011000', '0011001', '0011010', '0011011', '0011100', '0011101', '0011110', '0011111',
                    '0100000', '0100001', '0100010', '0100011', '0100100', '0100101', '0100110', '0100111',
                    '0101000', '0101001', '0101010', '0101011', '0101100', '0101101', '0101110', '0101111',
                    '0110000', '0110001', '0110010', '0110011', '0110100', '0110101', '0110110', '0110111',
                    '0111000', '0111001', '0111010', '0111011', '0111100', '0111101', '0111110', '0111111',
                    '1000000', '1000001', '1000010', '1000011', '1000100', '1000101', '1000110', '1000111',
                    '1001000', '1001001', '1001010', '1001011', '1001100', '1001101', '1001110', '1001111',
                    '1010000', '1010001', '1010010', '1010011', '1010100', '1010101', '1010110', '1010111',
                    '1011000', '1011001', '1011010', '1011011', '1011100', '1011101', '1011110', '1011111',
                    '1100000', '1100001', '1100010', '1100011', '1100100', '1100101', '1100110', '1100111',
                    '1101000', '1101001', '1101010', '1101011', '1101100', '1101101', '1101110', '1101111',
                    '1110000', '1110001', '1110010', '1110011', '1110100', '1110101', '1110110', '1110111',
                    '1111000', '1111001', '1111010', '1111011', '1111100', '1111101', '1111110', '1111111']
    elif bitin == 8:
        entradas = ['00000000', '00000001', '00000010', '00000011', '00000100', '00000101', '00000110', '00000111',
                    '00001000', '00001001', '00001010', '00001011', '00001100', '00001101', '00001110', '00001111',
                    '00010000', '00010001', '00010010', '00010011', '00010100', '00010101', '00010110', '00010111',
                    '00011000', '00011001', '00011010', '00011011', '00011100', '00011101', '00011110', '00011111',
                    '00100000', '00100001', '00100010', '00100011', '00100100', '00100101', '00100110', '00100111',
                    '00101000', '00101001', '00101010', '00101011', '00101100', '00101101', '00101110', '00101111',
                    '00110000', '00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111',
                    '00111000', '00111001', '00111010', '00111011', '00111100', '00111101', '00111110', '00111111',
                    '01000000', '01000001', '01000010', '01000011', '01000100', '01000101', '01000110', '01000111',
                    '01001000', '01001001', '01001010', '01001011', '01001100', '01001101', '01001110', '01001111',
                    '01010000', '01010001', '01010010', '01010011', '01010100', '01010101', '01010110', '01010111',
                    '01011000', '01011001', '01011010', '01011011', '01011100', '01011101', '01011110', '01011111',
                    '01100000', '01100001', '01100010', '01100011', '01100100', '01100101', '01100110', '01100111',
                    '01101000', '01101001', '01101010', '01101011', '01101100', '01101101', '01101110', '01101111',
                    '01110000', '01110001', '01110010', '01110011', '01110100', '01110101', '01110110', '01110111',
                    '01111000', '01111001', '01111010', '01111011', '01111100', '01111101', '01111110', '01111111',
                    '10000000', '10000001', '10000010', '10000011', '10000100', '10000101', '10000110', '10000111',
                    '10001000', '10001001', '10001010', '10001011', '10001100', '10001101', '10001110', '10001111',
                    '10010000', '10010001', '10010010', '10010011', '10010100', '10010101', '10010110', '10010111',
                    '10011000', '10011001', '10011010', '10011011', '10011100', '10011101', '10011110', '10011111',
                    '10100000', '10100001', '10100010', '10100011', '10100100', '10100101', '10100110', '10100111',
                    '10101000', '10101001', '10101010', '10101011', '10101100', '10101101', '10101110', '10101111',
                    '10110000', '10110001', '10110010', '10110011', '10110100', '10110101', '10110110', '10110111',
                    '10111000', '10111001', '10111010', '10111011', '10111100', '10111101', '10111110', '10111111',
                    '11000000', '11000001', '11000010', '11000011', '11000100', '11000101', '11000110', '11000111',
                    '11001000', '11001001', '11001010', '11001011', '11001100', '11001101', '11001110', '11001111',
                    '11010000', '11010001', '11010010', '11010011', '11010100', '11010101', '11010110', '11010111',
                    '11011000', '11011001', '11011010', '11011011', '11011100', '11011101', '11011110', '11011111',
                    '11100000', '11100001', '11100010', '11100011', '11100100', '11100101', '11100110', '11100111',
                    '11101000', '11101001', '11101010', '11101011', '11101100', '11101101', '11101110', '11101111',
                    '11110000', '11110001', '11110010', '11110011', '11110100', '11110101', '11110110', '11110111',
                    '11111000', '11111001', '11111010', '11111011', '11111100', '11111101', '11111110', '11111111']
    elif bitin == 9:
        entradas = ['000000000', '000000001', '000000010', '000000011', '000000100', '000000101', '000000110', '000000111',
                    '000001000', '000001001', '000001010', '000001011', '000001100', '000001101', '000001110', '000001111',
                    '000010000', '000010001', '000010010', '000010011', '000010100', '000010101', '000010110', '000010111',
                    '000011000', '000011001', '000011010', '000011011', '000011100', '000011101', '000011110', '000011111',
                    '000100000', '000100001', '000100010', '000100011', '000100100', '000100101', '000100110', '000100111',
                    '000101000', '000101001', '000101010', '000101011', '000101100', '000101101', '000101110', '000101111',
                    '000110000', '000110001', '000110010', '000110011', '000110100', '000110101', '000110110', '000110111',
                    '000111000', '000111001', '000111010', '000111011', '000111100', '000111101', '000111110', '000111111',
                    '001000000', '001000001', '001000010', '001000011', '001000100', '001000101', '001000110', '001000111',
                    '001001000', '001001001', '001001010', '001001011', '001001100', '001001101', '001001110', '001001111',
                    '001010000', '001010001', '001010010', '001010011', '001010100', '001010101', '001010110', '001010111',
                    '001011000', '001011001', '001011010', '001011011', '001011100', '001011101', '001011110', '001011111',
                    '001100000', '001100001', '001100010', '001100011', '001100100', '001100101', '001100110', '001100111',
                    '001101000', '001101001', '001101010', '001101011', '001101100', '001101101', '001101110', '001101111',
                    '001110000', '001110001', '001110010', '001110011', '001110100', '001110101', '001110110', '001110111',
                    '001111000', '001111001', '001111010', '001111011', '001111100', '001111101', '001111110', '001111111',
                    '010000000', '010000001', '010000010', '010000011', '010000100', '010000101', '010000110', '010000111',
                    '010001000', '010001001', '010001010', '010001011', '010001100', '010001101', '010001110', '010001111',
                    '010010000', '010010001', '010010010', '010010011', '010010100', '010010101', '010010110', '010010111',
                    '010011000', '010011001', '010011010', '010011011', '010011100', '010011101', '010011110', '010011111',
                    '010100000', '010100001', '010100010', '010100011', '010100100', '010100101', '010100110', '010100111',
                    '010101000', '010101001', '010101010', '010101011', '010101100', '010101101', '010101110', '010101111',
                    '010110000', '010110001', '010110010', '010110011', '010110100', '010110101', '010110110', '010110111',
                    '010111000', '010111001', '010111010', '010111011', '010111100', '010111101', '010111110', '010111111',
                    '011000000', '011000001', '011000010', '011000011', '011000100', '011000101', '011000110', '011000111',
                    '011001000', '011001001', '011001010', '011001011', '011001100', '011001101', '011001110', '011001111',
                    '011010000', '011010001', '011010010', '011010011', '011010100', '011010101', '011010110', '011010111',
                    '011011000', '011011001', '011011010', '011011011', '011011100', '011011101', '011011110', '011011111',
                    '011100000', '011100001', '011100010', '011100011', '011100100', '011100101', '011100110', '011100111',
                    '011101000', '011101001', '011101010', '011101011', '011101100', '011101101', '011101110', '011101111',
                    '011110000', '011110001', '011110010', '011110011', '011110100', '011110101', '011110110', '011110111',
                    '011111000', '011111001', '011111010', '011111011', '011111100', '011111101', '011111110', '011111111',
                    '100000000', '100000001', '100000010', '100000011', '100000100', '100000101', '100000110', '100000111',
                    '100001000', '100001001', '100001010', '100001011', '100001100', '100001101', '100001110', '100001111',
                    '100010000', '100010001', '100010010', '100010011', '100010100', '100010101', '100010110', '100010111',
                    '100011000', '100011001', '100011010', '100011011', '100011100', '100011101', '100011110', '100011111',
                    '100100000', '100100001', '100100010', '100100011', '100100100', '100100101', '100100110', '100100111',
                    '100101000', '100101001', '100101010', '100101011', '100101100', '100101101', '100101110', '100101111',
                    '100110000', '100110001', '100110010', '100110011', '100110100', '100110101', '100110110', '100110111',
                    '100111000', '100111001', '100111010', '100111011', '100111100', '100111101', '100111110', '100111111',
                    '101000000', '101000001', '101000010', '101000011', '101000100', '101000101', '101000110', '101000111',
                    '101001000', '101001001', '101001010', '101001011', '101001100', '101001101', '101001110', '101001111',
                    '101010000', '101010001', '101010010', '101010011', '101010100', '101010101', '101010110', '101010111',
                    '101011000', '101011001', '101011010', '101011011', '101011100', '101011101', '101011110', '101011111',
                    '101100000', '101100001', '101100010', '101100011', '101100100', '101100101', '101100110', '101100111',
                    '101101000', '101101001', '101101010', '101101011', '101101100', '101101101', '101101110', '101101111',
                    '101110000', '101110001', '101110010', '101110011', '101110100', '101110101', '101110110', '101110111',
                    '101111000', '101111001', '101111010', '101111011', '101111100', '101111101', '101111110', '101111111',
                    '110000000', '110000001', '110000010', '110000011', '110000100', '110000101', '110000110', '110000111',
                    '110001000', '110001001', '110001010', '110001011', '110001100', '110001101', '110001110', '110001111',
                    '110010000', '110010001', '110010010', '110010011', '110010100', '110010101', '110010110', '110010111',
                    '110011000', '110011001', '110011010', '110011011', '110011100', '110011101', '110011110', '110011111',
                    '110100000', '110100001', '110100010', '110100011', '110100100', '110100101', '110100110', '110100111',
                    '110101000', '110101001', '110101010', '110101011', '110101100', '110101101', '110101110', '110101111',
                    '110110000', '110110001', '110110010', '110110011', '110110100', '110110101', '110110110', '110110111',
                    '110111000', '110111001', '110111010', '110111011', '110111100', '110111101', '110111110', '110111111',
                    '111000000', '111000001', '111000010', '111000011', '111000100', '111000101', '111000110', '111000111',
                    '111001000', '111001001', '111001010', '111001011', '111001100', '111001101', '111001110', '111001111',
                    '111010000', '111010001', '111010010', '111010011', '111010100', '111010101', '111010110', '111010111',
                    '111011000', '111011001', '111011010', '111011011', '111011100', '111011101', '111011110', '111011111',
                    '111100000', '111100001', '111100010', '111100011', '111100100', '111100101', '111100110', '111100111',
                    '111101000', '111101001', '111101010', '111101011', '111101100', '111101101', '111101110', '111101111',
                    '111110000', '111110001', '111110010', '111110011', '111110100', '111110101', '111110110', '111110111',
                    '111111000', '111111001', '111111010', '111111011', '111111100', '111111101', '111111110', '111111111']

    tamanho_populacao = 2*qtd_estados*bits
    taxa_mutacao = 0.02
    #tabela = tcc.gerar_template(lista)
    #individuo = Individuo()
    ag = AlgoritimoGenetico(tamanho_populacao)

    inicio = time.time()
    resp, cust, termos = ag.resolver(500, taxa_mutacao, entradas)
    fim = time.time()
    temp = fim - inicio

    print(resp, cust, termos, temp)
    #novatabela = tcc.preencher_template(lista, tabela, individuo)