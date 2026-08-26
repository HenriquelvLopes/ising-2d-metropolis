from random import random, randrange
from math import exp
import matplotlib.pyplot as plt

spin = []

n = int(input("digite o tamanho da rede (n x n):"))
j = float(input("digite o valor da constante (J):"))
    
Ti = float(input("digite a temperatura inicial (Ti):"))
Tf = float(input("digite a temperatura final (Tf):"))
passos = 200

deltaT = (Tf - Ti) / passos
T = Ti

energias = []
temperaturas = []
magnetizacoes = []

termalizacao = 500
amostras = 500

for x in range(n):
    spin.append([0] * n)
def aleatorio(x, y):
    t = random()

    if t < 0.5:
        spin[x][y] = 1
    else:
        spin[x][y] = -1
def energia(spin, j):
    h = 0
    for x in range(n):
        for y in range(n):
            h += energia_somada(spin, x, y, j)
    return h / 2
def lado(spin, x, y):

    cima = spin[(x-1) % n][y]
    baixo = spin[(x+1) % n][y]
    esquerda = spin[x][(y-1) % n]
    direita = spin[x][(y+1) % n]

    return cima, baixo, esquerda, direita

    ### soma de vizinhos adjacentes, ate os que ligam na outra borda. como se fosse um circulo 
def energia_somada(spin, x, y, j):
    cima, baixo, esquerda, direita = lado(spin, x, y)

    return -j * spin[x][y] * (cima + baixo + esquerda + direita)
def inverter(spin, n):

    x = randrange(n)
    y = randrange(n)

    if spin[x][y] == 1:
        spin[x][y] = -1
    else:
        spin[x][y] = 1

    return x, y
def delta_energia(spin, x, y, j):

    cima, baixo, esquerda, direita = lado(spin, x, y)

    soma_vizinhos = cima + baixo + esquerda + direita

    return 2 * j * spin[x][y] * soma_vizinhos


def magnetizacao(spin):
    m = 0

    for x in range(n):
        for y in range(n):
            m += spin[x][y]

    return m

def metropolis(spin, n, j, T):

    x = randrange(n)
    y = randrange(n)

    delta_E = delta_energia(spin, x, y, j)

    if delta_E <= 0:

        spin[x][y] *= -1

    else:

        probabilidade = exp(-delta_E/T)

        if random() < probabilidade:
            spin[x][y] *= -1
for x in range(n):
    for y in range(n):
        aleatorio(x, y)

print("Temperatura inicial:", T)
print("Estado inicial:")
print(spin)

for z in range(passos + 1):

    soma_E = 0
    soma_M = 0

    for i in range(termalizacao):
        for k in range(n*n):
            metropolis(spin, n, j, T)


    for i in range(amostras):

        for k in range(n*n):
            metropolis(spin, n, j, T)

        soma_E += energia(spin, j)
        soma_M += abs(magnetizacao(spin))

    energia_media = soma_E / amostras
    magnetizacao_media = soma_M / amostras

    energia_spin = energia_media / (n*n)
    magnetizacao_spin = magnetizacao_media / (n*n)

    energias.append(energia_spin)
    temperaturas.append(T)
    magnetizacoes.append(magnetizacao_spin)

    print(f"T = {T:.2f} | E = {energias[-1]:.4f} | M = {magnetizacoes[-1]:.4f}")

    T += deltaT


print("Estado final:")
print(spin)

print("Energia:")
print(energia(spin, j))

print("magnetização:")
print(magnetizacoes[-1])

plt.figure(1)

plt.plot(temperaturas, energias)

plt.xlabel("Temperatura (T)")
plt.ylabel("Energia por spin (E/N)")
plt.title("Energia por spin em função da temperatura")

plt.xticks([Ti + 0.5*i for i in range(int((Tf - Ti)/0.5) + 1)])
plt.grid()


plt.figure(2)

plt.plot(temperaturas, magnetizacoes)

plt.xlabel("Temperatura (T)")
plt.ylabel("Magnetização por spin |M|/N")
plt.title("Magnetização por spin em função da temperatura")

plt.ylim(0, 1)
plt.xticks([Ti + 0.5*i for i in range(int((Tf - Ti)/0.5) + 1)])
plt.grid()

plt.show()
