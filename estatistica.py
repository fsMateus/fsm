from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1)

i = 0
iteracoes = []

x = []
arq = open('custos/beecount.txt', 'r')
for item in arq:
    x.append(int(item))
    i += 1
    iteracoes.append(i)
arq.close()
aux = np.array(x)
beecount = -np.sort(-aux)
media1 = np.mean(beecount)
desvio1 = np.std(beecount)

x = []
arq = open('custos/dk14-8.txt', 'r')
for item in arq:
    x.append(int(item))
arq.close()
aux = np.array(x)
dk14 = -np.sort(-aux)
media2 = np.mean(dk14)
desvio2 = np.std(dk14)

x = []
arq = open('custos/ex3-1.txt', 'r')
for item in arq:
    x.append(int(item))
arq.close()
aux = np.array(x)
ex3 = -np.sort(-aux)
media3 = np.mean(ex3)
desvio3 = np.std(ex3)

x = []
arq = open('custos/mc.txt', 'r')
for item in arq:
    x.append(int(item))
arq.close()
aux = np.array(x)
mc = -np.sort(-aux)
media4 = np.mean(mc)
desvio4 = np.std(mc)

x = []
arq = open('custos/tav1.txt', 'r')
for item in arq:
    x.append(int(item))
arq.close()
aux = np.array(x)
tav = -np.sort(-aux)
media5 = np.mean(tav)
desvio5 = np.std(tav)

x = []
arq = open('custos/train11.txt', 'r')
for item in arq:
    x.append(int(item))
arq.close()
aux = np.array(x)
train11 = -np.sort(-aux)
media6 = np.mean(train11)
desvio6 = np.std(train11)

# aux = np.array(x)
# norm1 = aux / np.linalg.norm(aux)
# valores = -np.sort(-aux)


# media = np.mean(valores)
# desvio = np.std(valores)

# max = np.max(valores)

# print(np.min(x))

# cum = np.cumsum(valores)
# pmf = cum / np.amax(cum)

# valor, count = np.unique(valores, return_counts=True)
# count = (count / np.amax(count)) / 10

# ax.plot(valor, count, 'r--', label='frequencia')
# ax.plot(valores, pmf, 'b--', label='cumulativa')
# ax.hist(valores, density=True, histtype='stepfilled', alpha=0.3)

ax.plot(beecount, norm.pdf(beecount, loc=media1, scale=desvio1), 'b', label='beecount')
ax.plot(dk14, norm.pdf(dk14, loc=media2, scale=desvio2), 'y', label='dk14')
ax.plot(ex3, norm.pdf(ex3, loc=media3, scale=desvio3), 'r', label='ex3')
ax.plot(mc, norm.pdf(mc, loc=media4, scale=desvio4), 'g', label='mc')
ax.plot(tav, norm.pdf(tav, loc=media5, scale=desvio5), 'k', label='tav')
ax.plot(train11, norm.pdf(train11, loc=media6, scale=desvio6), 'm', label='train11')
# ax.plot(valor, count, 'r--', label='Frequencia (X)')

# ax.set_xlim(40, 120)
# ax.hist(valores, density=True, histtype='stepfilled', alpha=0.3)

# plt.plot(iteracoes, beecount, 'r', label='beecount')
# plt.plot(iteracoes, dk14, 'b', label='dk14')
# plt.plot(iteracoes, ex3, 'g', label='ex3')
# plt.plot(iteracoes, mc, 'k', label='mc')
# plt.plot(iteracoes, tav, 'c', label='tav')
# plt.plot(iteracoes, train11, 'm', label='train11')
#
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('Cost')
plt.ylabel('Probability Density Function')

plt.title('Normal Distribution')
plt.show()
